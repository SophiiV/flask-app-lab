import unittest
from app import app

class FlaskProductsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_list(self):
        resp = self.client.get("/products/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Products List", resp.data)

    def test_product_detail_ok(self):
        resp = self.client.get("/products/1")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Product #1", resp.data)

    def test_product_detail_404(self):
        resp = self.client.get("/products/999")
        self.assertEqual(resp.status_code, 404)

if __name__ == "__main__":
    unittest.main()
