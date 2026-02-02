import io
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

import pywwwget as wwwget


class TestPyWWWGet(unittest.TestCase):
    def test_imports_and_exports(self):
        self.assertTrue(hasattr(wwwget, "download_file_from_internet_file"))
        self.assertTrue(hasattr(wwwget, "download_file_from_internet_bytes"))
        self.assertTrue(hasattr(wwwget, "data_url_encode"))
        self.assertTrue(hasattr(wwwget, "data_url_decode"))
        self.assertTrue(hasattr(wwwget, "_parse_net_url"))
        self.assertTrue(hasattr(wwwget, "_parse_kv_headers"))
        self.assertTrue(hasattr(wwwget, "_split_bt_netloc"))

    def test_data_url_roundtrip(self):
        payload = b"hello world\n\x00\x01\x02"
        url = wwwget.data_url_encode(
            fileobj=io.BytesIO(payload),
            mime="application/octet-stream",
            is_text=False,
            base64_encode=True,
        )
        fp, mime, is_text = wwwget.data_url_decode(url)
        try:
            got = fp.read()
        finally:
            try:
                fp.close()
            except Exception:
                pass

        self.assertEqual(got, payload)
        self.assertEqual(mime, "application/octet-stream")
        self.assertFalse(is_text)

    def test_hdr_query_parsing(self):
        qs = parse_qs("hdr_x_test=123&hdr_user_agent=ua")
        headers = wwwget._parse_kv_headers(qs)
        self.assertEqual(headers.get("x-test"), "123")
        self.assertEqual(headers.get("user-agent"), "ua")

    def test_parse_net_url_defaults_udp(self):
        parts, opts = wwwget._parse_net_url("udp://127.0.0.1:9999/")
        self.assertEqual(parts.scheme, "udp")
        # UDP default mode is "seq" in this module
        self.assertEqual(opts.get("mode"), "seq")


    def test_bt_netloc_parsing(self):
        addr, ch = wwwget._split_bt_netloc("AA:BB:CC:DD:EE:FF:3")
        self.assertEqual(addr, "AA:BB:CC:DD:EE:FF")
        self.assertEqual(ch, 3)

        addr, ch = wwwget._split_bt_netloc("AA-BB-CC-DD-EE-FF:7")
        self.assertEqual(addr, "AA:BB:CC:DD:EE:FF")
        self.assertEqual(ch, 7)

        addr, ch = wwwget._split_bt_netloc("")
        self.assertEqual(addr, "00:00:00:00:00:00")
        self.assertIsNone(ch)

        # Full URL parsing should not rely on urlparse hostname/port for bt
        from urllib.parse import urlparse, parse_qs
        parts = urlparse("bt://AA:BB:CC:DD:EE:FF:5/file.bin?channel=6")
        qs = parse_qs(parts.query or "")
        host, ch = wwwget._bt_host_channel_from_url(parts, qs, {"bind": None})
        self.assertEqual(host, "AA:BB:CC:DD:EE:FF")
        # netloc channel takes precedence over query channel
        self.assertEqual(ch, 5)


    def test_local_http_download(self):
        body = b"abc123"

        class H(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, fmt, *args):
                # silence server logs in tests
                return

        httpd = ThreadingHTTPServer(("127.0.0.1", 0), H)
        port = httpd.server_address[1]
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()
        try:
            url = f"http://127.0.0.1:{port}/file"
            got = wwwget.download_file_from_internet_bytes(url, timeout=5, usehttp="urllib")
            self.assertEqual(got, body)
        finally:
            httpd.shutdown()
            httpd.server_close()
            t.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
