import logging
import random
import re
import subprocess
from copy import deepcopy
from time import sleep

from requests.sessions import Session

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

__version__ = "1.9.5"

DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Build/NPPS25.137-93-8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.137 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
]

DEFAULT_USER_AGENT = random.choice(DEFAULT_USER_AGENTS)

BUG_REPORT = """\
Cloudflare may have changed their technique, or there may be a bug in the script.

Please read https://github.com/Anorov/cloudflare-scrape#updates, then file a \
bug report at https://github.com/Anorov/cloudflare-scrape/issues."\
"""

ANSWER_ACCEPT_ERROR = """\
The challenge answer was not properly accepted by Cloudflare. This can occur if \
the target website is under heavy load, or if Cloudflare is experiencing issues. You can
potentially resolve this by increasing the challenge answer delay (default: 8 seconds). \
For example: cfscrape.create_scraper(delay=15)

If increasing the delay does not help, please open a GitHub issue at \
https://github.com/Anorov/cloudflare-scrape/issues\
"""


class CloudflareScraper(Session):
    def __init__(self, *args, **kwargs):
        self.delay = kwargs.pop("delay", 8)
        super(CloudflareScraper, self).__init__(*args, **kwargs)

        if "requests" in self.headers["User-Agent"]:
            # Set a random User-Agent if no custom User-Agent has been set
            self.headers["User-Agent"] = DEFAULT_USER_AGENT

    def is_cloudflare_challenge(self, resp):
        return (
                resp.status_code == 503
                and resp.headers.get("Server", "").startswith("cloudflare")
                and b"jschl_vc" in resp.content
                and b"jschl_answer" in resp.content
        )

    def request(self, method, url, *args, **kwargs):
        resp = super(CloudflareScraper, self).request(method, url, *args, **kwargs)

        # Check if Cloudflare anti-bot is on
        if self.is_cloudflare_challenge(resp):
            resp = self.solve_cf_challenge(resp, **kwargs)

        return resp

    def solve_cf_challenge(self, resp, **original_kwargs):
        sleep(self.delay)  # Cloudflare requires a delay before solving the challenge

        body = resp.text
        parsed_url = urlparse(resp.url)
        domain = parsed_url.netloc
        submit_url = "%s://%s/cdn-cgi/l/chk_jschl" % (parsed_url.scheme, domain)

        cloudflare_kwargs = deepcopy(original_kwargs)
        params = cloudflare_kwargs.setdefault("params", {})
        headers = cloudflare_kwargs.setdefault("headers", {})
        headers["Referer"] = resp.url

        try:
            params["jschl_vc"] = re.search(r'name="jschl_vc" value="(\w+)"', body).group(1)
            params["pass"] = re.search(r'name="pass" value="(.+?)"', body).group(1)

        except Exception as e:
            # Something is wrong with the page.
            # This may indicate Cloudflare has changed their anti-bot
            # technique. If you see this and are running the latest version,
            # please open a GitHub issue so I can update the code accordingly.
            raise ValueError("Unable to parse Cloudflare anti-bots page: %s %s" % (e.message, BUG_REPORT))

        # Solve the Javascript challenge
        params["jschl_answer"] = self.solve_challenge(body, domain)

        # Requests transforms any request into a GET after a redirect,
        # so the redirect has to be handled manually here to allow for
        # performing other types of requests even as the first request.
        method = resp.request.method
        cloudflare_kwargs["allow_redirects"] = False
        redirect = self.request(method, submit_url, **cloudflare_kwargs)

        redirect_location = urlparse(redirect.headers["Location"])
        if not redirect_location.netloc:
            redirect_url = "%s://%s%s" % (parsed_url.scheme, domain, redirect_location.path)
            return self.request(method, redirect_url, **original_kwargs)
        return self.request(method, redirect.headers["Location"], **original_kwargs)

    def solve_cf_challenge(self, resp, **original_kwargs):
        sleep(8)  # Cloudflare requires a delay before solving the challenge

        body = resp.text
        parsed_url = urlparse(resp.url)
        domain = parsed_url.netloc
        submit_url = "%s://%s/cdn-cgi/l/chk_jschl" % (parsed_url.scheme, domain)

        cloudflare_kwargs = deepcopy(original_kwargs)
        params = cloudflare_kwargs.setdefault("params", {})
        headers = cloudflare_kwargs.setdefault("headers", {})
        headers["Referer"] = resp.url

        try:
            params["jschl_vc"] = re.search(r'name="jschl_vc" value="(\w+)"', body).group(1)
            params["pass"] = re.search(r'name="pass" value="(.+?)"', body).group(1)

            # Extract the arithmetic operation
            init = re.findall('setTimeout\(function\(\){\s*var.*?.*:(.*?)}', body)[-1]
            builder = re.findall(r"challenge-form\'\);\s*(.*)a.v", body)[0]
            if '/' in init:
                init = init.split('/')
                decryptVal = self.parseJSString(init[0]) / float(self.parseJSString(init[1]))
            else:
                decryptVal = self.parseJSString(init)
            lines = builder.split(';')

            for line in lines:
                if len(line) > 0 and '=' in line:
                    sections = line.split('=')
                    if '/' in sections[1]:
                        subsecs = sections[1].split('/')
                        line_val = self.parseJSString(subsecs[0]) / float(self.parseJSString(subsecs[1]))
                    else:
                        line_val = self.parseJSString(sections[1])
                    decryptVal = float(eval(('%.16f' % decryptVal) + sections[0][-1] + ('%.16f' % line_val)))

            answer = float('%.10f' % decryptVal) + len(domain)


        except Exception as e:
            # Something is wrong with the page.
            # This may indicate Cloudflare has changed their anti-bot
            # technique. If you see this and are running the latest version,
            # please open a GitHub issue so I can update the code accordingly.
            logging.error("[!] %s Unable to parse Cloudflare anti-bots page. "
                          "Try upgrading cloudflare-scrape, or submit a bug report "
                          "if you are running the latest version. Please read "
                          "https://github.com/Anorov/cloudflare-scrape#updates "
                          "before submitting a bug report." % e)
            raise

        try:
            params["jschl_answer"] = str(answer)  # str(int(jsunfuck.cfunfuck(js)) + len(domain))
        except:
            pass

        # Requests transforms any request into a GET after a redirect,
        # so the redirect has to be handled manually here to allow for
        # performing other types of requests even as the first request.
        method = resp.request.method
        cloudflare_kwargs["allow_redirects"] = False

        redirect = self.request(method, submit_url, **cloudflare_kwargs)
        redirect_location = urlparse(redirect.headers["Location"])

        if not redirect_location.netloc:
            redirect_url = "%s://%s%s" % (parsed_url.scheme, domain, redirect_location.path)
            return self.request(method, redirect_url, **original_kwargs)
        return self.request(method, redirect.headers["Location"], **original_kwargs)

    def parseJSString(self, s):
        try:
            offset=1 if s[0]=='+' else 0
            val = int(eval(s.replace('!+[]','1').replace('!![]','1').replace('[]','0').replace('(','str(')[offset:]))
            return val
        except:
            pass

    @classmethod
    def create_scraper(cls, sess=None, **kwargs):
        """
        Convenience function for creating a ready-to-go CloudflareScraper object.
        """
        scraper = cls(**kwargs)

        if sess:
            attrs = ["auth", "cert", "cookies", "headers", "hooks", "params", "proxies", "data"]
            for attr in attrs:
                val = getattr(sess, attr, None)
                if val:
                    setattr(scraper, attr, val)

        return scraper

    ## Functions for integrating cloudflare-scrape with other applications and scripts

    @classmethod
    def get_tokens(cls, url, user_agent=None, curl_cookie_file=None, **kwargs):
        scraper = cls.create_scraper()
        if user_agent:
            scraper.headers["User-Agent"] = user_agent

        try:
            resp = scraper.get(url, **kwargs)
            resp.raise_for_status()
        except Exception as e:
            logging.error("'%s' returned an error. Could not collect tokens." % url)
            raise

        domain = urlparse(resp.url).netloc
        cookie_domain = None

        for d in scraper.cookies.list_domains():
            if d.startswith(".") and d in ("." + domain):
                cookie_domain = d
                break
        else:
            raise ValueError(
                "Unable to find Cloudflare cookies. Does the site actually have Cloudflare IUAM (\"I'm Under Attack Mode\") enabled?")

        if curl_cookie_file:
            curl_cookies = []
            for cookie in scraper.cookies:
                cookie_dict = cookie.__dict__
                if (cookie_dict['domain'] == cookie_domain):
                    # http://www.cookiecentral.com/faq/#3.5
                    curl_cookies.append('\t'.join(
                        [cookie_dict['domain'], 'TRUE', cookie_dict['path'],
                         'TRUE' if cookie_dict['secure'] else 'FALSE',
                         str(cookie_dict['expires']), cookie_dict['name'], cookie_dict['value']]
                    ))
            text_file = open(curl_cookie_file, "w")
            text_file.write('\n'.join(curl_cookies) + '\n')
            text_file.close()

        return ({
                    "__cfduid": scraper.cookies.get("__cfduid", "", domain=cookie_domain),
                    "cf_clearance": scraper.cookies.get("cf_clearance", "", domain=cookie_domain)
                },
                scraper.headers["User-Agent"]
        )

    @classmethod
    def get_cookie_string(cls, url, user_agent=None, **kwargs):
        """
        Convenience function for building a Cookie HTTP header value.
        """
        tokens, user_agent = cls.get_tokens(url, user_agent=user_agent, **kwargs)
        return "; ".join("=".join(pair) for pair in tokens.items()), user_agent


create_scraper = CloudflareScraper.create_scraper
get_tokens = CloudflareScraper.get_tokens
get_cookie_string = CloudflareScraper.get_cookie_string