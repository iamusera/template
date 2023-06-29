import unittest
from application import app


class MyTestCase(unittest.TestCase):
    def test_something(self):
        client = app.test_client()
        resp = client.get("/test")
        self.assertEqual(resp.status_code, 200)  # add assertion here


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
    unittest.main()
