import unittest
from application import app


class MyTestCase(unittest.TestCase):
    def test_wind_db(self):
        client = app.test_client()
        resp = client.get("/test/wind_db")
        self.assertEqual(resp.status_code, 200)  # add assertion here

    def test_rps_db(self):
        client = app.test_client()
        resp = client.get("/test/rps_db")
        self.assertEqual(resp.status_code, 200)  # add assertion here

    def test_ck_db(self):
        client = app.test_client()
        resp = client.get("/test/ck_db")
        self.assertEqual(resp.status_code, 200)  # add assertion here


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
    unittest.main()
