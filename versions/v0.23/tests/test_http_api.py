"""AxiomFlow v0.20: real loopback HTTP and web/API end-to-end tests."""
from decimal import Decimal, ROUND_HALF_EVEN
from http.client import HTTPConnection
import json
import random
import threading
import unittest

from axiomflow.api import calculate, create_server
from axiomflow.language import AxiomError


class CalculationTests(unittest.TestCase):
    def test_real_typed_function(self):
        self.assertEqual(calculate({"price": "125.50", "rate": "0.075"}),
                         {"total": "134.91 USD", "currency": "USD"})

    def test_halfeven_boundaries(self):
        self.assertEqual(calculate({"price": "1.00", "rate": "0.125"})["total"],
                         "1.12 USD")
        self.assertEqual(calculate({"price": "1.00", "rate": "0.135"})["total"],
                         "1.14 USD")

    def test_reject_wrong_value_types(self):
        for value in (125.50, 125, None, True, [], {}):
            with self.subTest(value=str(value)), self.assertRaises(AxiomError):
                calculate({"price": value, "rate": "0.075"})

    def test_reject_invalid_payload(self):
        for obj in ({}, [], {"price": "1.00"}, {"price": "1.00", "rate": "0.1", "foo": 1}):
            with self.subTest(obj=str(obj)), self.assertRaises(AxiomError):
                calculate(obj)

    def test_reject_malformed_decimal_and_bounds(self):
        cases = [
            {"price": "-1.00", "rate": "0.1"},
            {"price": "1.005", "rate": "0.1"},
            {"price": "1000000.01", "rate": "0.1"},
            {"price": "1.00", "rate": "1.0001"},
            {"price": "1.00", "rate": "NaN"},
            {"price": "1.00", "rate": "0.10000"},
            {"price": "1e3", "rate": "0.1"},
        ]
        for item in cases:
            with self.subTest(item=item), self.assertRaises(AxiomError):
                calculate(item)

    def test_seeded_python_decimal_oracle_300(self):
        rng = random.Random(20261020)
        for index in range(300):
            cents = rng.randrange(0, 100000000)
            rate_digits = rng.randrange(0, 10001)
            price = Decimal(cents) / 100
            rate = Decimal(rate_digits) / 10000
            observed = calculate({"price": f"{price:.2f}", "rate": f"{rate:.4f}"})
            expected = (price * (1 + rate)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_EVEN
            )
            with self.subTest(index=index):
                self.assertEqual(observed["total"], f"{expected:.2f} USD")


class HttpApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(port=0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def request(self, method, path, body=None, headers=None):
        connection = HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            content = response.read()
            return response.status, dict(response.getheaders()), content
        finally:
            connection.close()

    def post(self, payload):
        return self.request("POST", "/api/v1/landed-cost",
                            json.dumps(payload).encode(),
                            {"Content-Type": "application/json"})

    def test_health_endpoint(self):
        status, headers, body = self.request("GET", "/health")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["status"], "ok")

    def test_html_javascript_and_css(self):
        for path, mime, sample in [
            ("/", "text/html", b"AxiomFlow"),
            ("/app.js", "text/javascript", b"/api/v1/landed-cost"),
            ("/style.css", "text/css", b"background"),
        ]:
            with self.subTest(path=path):
                status, headers, body = self.request("GET", path)
                self.assertEqual(status, 200)
                self.assertIn(mime, headers["Content-Type"])
                self.assertIn(sample, body)
                self.assertIn("default-src 'none'", headers["Content-Security-Policy"])

    def test_http_typed_calculation(self):
        status, headers, body = self.post({"price": "125.50", "rate": "0.075"})
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {"currency": "USD", "total": "134.91 USD"})
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")

    def test_http_bad_json(self):
        status, _, body = self.request(
            "POST", "/api/v1/landed-cost", b'{"price":',
            {"Content-Type": "application/json"}
        )
        self.assertEqual(status, 400)
        self.assertIn(b"invalid", body)

    def test_http_duplicate_json_keys(self):
        status, _, _ = self.request(
            "POST", "/api/v1/landed-cost",
            b'{"price":"1.00","rate":"0.1","price":"2.00"}',
            {"Content-Type": "application/json"}
        )
        self.assertEqual(status, 400)

    def test_http_content_type_enforced(self):
        status, _, _ = self.request(
            "POST", "/api/v1/landed-cost", b"{}",
            {"Content-Type": "text/plain"}
        )
        self.assertEqual(status, 415)

    def test_http_payload_limit(self):
        status, _, _ = self.request(
            "POST", "/api/v1/landed-cost", b"x" * 2049,
            {"Content-Type": "application/json"}
        )
        self.assertEqual(status, 413)

    def test_http_reject_unexpected_route(self):
        status, _, _ = self.request("GET", "/etc/passwd")
        self.assertEqual(status, 404)
        status, _, _ = self.post({"price": "1.00", "rate": "0.1", "extra": "no"})
        self.assertEqual(status, 400)

    def test_non_loopback_rejected(self):
        with self.assertRaisesRegex(ValueError, "loopback"):
            create_server(host="0.0.0.0", port=0)

    def test_multi_request_isolation(self):
        first = json.loads(self.post({"price": "1.00", "rate": "0.1"})[2])
        second = json.loads(self.post({"price": "2.00", "rate": "0.2"})[2])
        self.assertEqual(first["total"], "1.10 USD")
        self.assertEqual(second["total"], "2.40 USD")


if __name__ == "__main__":
    unittest.main()
