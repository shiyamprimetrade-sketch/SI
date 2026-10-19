"""AxiomFlow v0.20 demo HTTP API: loopback-only by default.

Standard library HTTP server, not a hardened public-network deployment.
Request JSON values are validated before dispatching to the typed language.
"""
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import re
from urllib.parse import urlsplit

from .language import AxiomError
from .typed import evaluate_typed

MAX_BODY = 2048
MAX_PRICE = Decimal("1000000.00")
MAX_RATE = Decimal("1.0000")
DECIMAL_PRICE = re.compile(r"(?:0|[1-9][0-9]{0,6})\.[0-9]{2}\Z")
DECIMAL_RATE = re.compile(r"(?:0|1)\.[0-9]{1,4}\Z")
FUNCTION_SOURCE = "fn tax(price: USD, rate: scalar) -> USD = price * (1 + rate)\n"
PAGE = Path(__file__).resolve().parent.parent / "web" / "index.html"


def calculate(payload):
    if type(payload) is not dict or set(payload) != {"price", "rate"}:
        raise AxiomError("expected exactly price and rate")
    price, rate = payload["price"], payload["rate"]
    if (type(price) is not str or type(rate) is not str or
            not DECIMAL_PRICE.fullmatch(price) or
            not DECIMAL_RATE.fullmatch(rate)):
        raise AxiomError("invalid money or rate decimal syntax")
    if Decimal(price) > MAX_PRICE or Decimal(rate) > MAX_RATE:
        raise AxiomError("value outside supported bounds")
    source = FUNCTION_SOURCE + f"emit tax({price} USD, {rate})"
    output = evaluate_typed(source)
    if len(output) != 1:
        raise AxiomError("unexpected AxiomFlow output")
    return {"total": output[0], "currency": "USD"}


class Handler(BaseHTTPRequestHandler):
    server_version = "AxiomFlowDemo/0.20"
    sys_version = ""

    def _send(self, code, body, mime="application/json; charset=utf-8"):
        if isinstance(body, dict):
            body = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy",
                         "default-src 'none'; script-src 'self'; style-src 'self'; "
                         "connect-src 'self'; base-uri 'none'; form-action 'none'")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/health":
            return self._send(200, {"status": "ok", "engine": "AxiomFlow"})
        if path == "/":
            return self._send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
        if path == "/app.js":
            return self._send(200, (PAGE.parent / "app.js").read_bytes(),
                              "text/javascript; charset=utf-8")
        if path == "/style.css":
            return self._send(200, (PAGE.parent / "style.css").read_bytes(),
                              "text/css; charset=utf-8")
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if urlsplit(self.path).path != "/api/v1/landed-cost":
            return self._send(404, {"error": "not found"})
        typ = self.headers.get("Content-Type", "")
        if typ.split(";", 1)[0].strip().lower() != "application/json":
            return self._send(415, {"error": "Content-Type must be application/json"})
        length = self.headers.get("Content-Length", "")
        if not length.isascii() or not length.isdecimal():
            return self._send(411, {"error": "Content-Length required"})
        if len(length) > 8 or int(length) > MAX_BODY:
            return self._send(413, {"error": "request too large"})
        if int(length) == 0:
            return self._send(400, {"error": "empty request"})
        try:
            raw = self.rfile.read(int(length))
            def no_duplicates(pairs):
                obj = {}
                for key, value in pairs:
                    if key in obj:
                        raise ValueError("duplicate JSON field")
                    obj[key] = value
                return obj
            payload = json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicates)
            result = calculate(payload)
        except (ValueError, UnicodeError, AxiomError):
            return self._send(400, {"error": "invalid calculation request"})
        return self._send(200, result)

    def log_message(self, fmt, *args):
        return


def create_server(host="127.0.0.1", port=8000):
    if host not in ("127.0.0.1", "localhost", "::1"):
        raise ValueError("demo server only permits loopback binding")
    if type(port) is not int or port < 0 or port > 65535:
        raise ValueError("invalid port")
    return ThreadingHTTPServer((host, port), Handler)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AxiomFlow local-only demo server")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    with create_server(port=args.port) as server:
        print(f"AxiomFlow demo at http://127.0.0.1:{server.server_port}/", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
