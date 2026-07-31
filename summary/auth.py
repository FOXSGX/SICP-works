import http.server
import requests
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qsl

TIMEOUT = 10
# LOGIN_ENDPOINT = '/auth/login'
REFRESH_ENDPOINT = "/auth/refresh"
GITLAB_ENDPOINT_1 = "/auth/gitlab/login"
GITLAB_ENDPOINT_2 = "/auth/gitlab/login/callback"
GITLAB_ENDPOINT_3 = "/auth/gitlab/login/success"


class OkException(Exception):
    """Base exception class for OK."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AuthenticationException(OkException):
    """Exceptions related to authentication."""


class OAuthException(AuthenticationException):
    def __init__(self, error="", error_description=""):
        super().__init__()
        self.error = error
        self.error_description = error_description


def post(server, endpoint, json, headers):
    """Try getting an access token from the server. If successful, returns the
    JSON response. If unsuccessful, raises an OAuthException.
    """
    if headers is None:
        headers = {}
    if "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"
    if "User-Agent" not in headers:
        headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        )
    try:
        response = requests.post(
            server + endpoint, json=json, headers=headers, timeout=TIMEOUT
        )
        if response.status_code in {403, 404}:
            raise CustomHttpError(
                f"HTTP Error {response.status_code}: {response.reason}"
            )
        # Check for non-JSON responses
        if "application/json" not in response.headers.get("Content-Type", ""):
            raise ValueError("Response is not JSON")
        # Parse JSON body
        body = response.json()
    except Exception as e:
        raise OAuthException(error="Authentication Failed", error_description=str(e))
    if "error" in body:
        raise OAuthException(
            error=body.get("error", "Unknown Error"),
            error_description=body.get("error_description", ""),
        )
    return body


def make_code_post_via_gitlab(server, code):
    json = {"code": code, "state": "ok", "platform": "ok-{}".format("114514")}
    return post(server, GITLAB_ENDPOINT_2, json, None)


def auth():
    server = "https://sicp.pascal-lab.net/api"
    code_response = None
    oauth_exception = None

    class CodeHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            """Respond to the GET request made by the OAuth"""
            nonlocal code_response, oauth_exception
            path = urlparse(self.path)
            qs = {k: v for k, v in parse_qsl(path.query)}
            code = qs.get("code")
            if code:
                try:
                    code_response = make_code_post_via_gitlab(server, code)
                except OAuthException as e:
                    oauth_exception = e
            else:
                oauth_exception = OAuthException(
                    error=qs.get("error", "Unknown Error"),
                    error_description=qs.get("error_description", ""),
                )

            if oauth_exception:
                print(
                    "{}\n{}".format(
                        oauth_exception.error, server, server, urlencode(code)
                    )
                )
            else:
                self.send_response(302)
                self.send_header("Location", "{}{}".format(server, GITLAB_ENDPOINT_3))
                self.end_headers()

    host_name = "localhost"
    port_number = 2830  # SICP
    server_address = (host_name, port_number)

    assert webbrowser.open_new("{}/auth/gitlab/login?state=ok".format(server))
    try:
        httpd = http.server.HTTPServer(server_address, CodeHandler)
        httpd.handle_request()
    except OSError as e:
        raise

    if oauth_exception:
        raise oauth_exception
    return code_response
