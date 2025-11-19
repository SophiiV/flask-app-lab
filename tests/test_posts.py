import unittest
from datetime import datetime

from app import create_app, db
from app.posts.models import Post


class PostsCrudTestCase(unittest.TestCase):
    """Test case for CRUD operations on Post model."""

    def setUp(self):
        """Create app and database for tests."""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up database and app context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post(self):
        """Post creation via form should succeed."""
        resp = self.client.post(
            "/post/create",
            data={
                "title": "Test title",
                "content": "Test content for post",
                "enabled": "y",
                "publish_date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M"),
                "category": "news",
            },
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Test title", resp.data)
        self.assertEqual(Post.query.count(), 1)

    def test_list_posts(self):
        """List route should return created posts."""
        p = Post(title="P1", content="C1")
        db.session.add(p)
        db.session.commit()

        resp = self.client.get("/post")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"P1", resp.data)

    def test_update_post(self):
        """Update route should modify existing post."""
        p = Post(title="Old", content="Old content")
        db.session.add(p)
        db.session.commit()

        resp = self.client.post(
            f"/post/{p.id}/update",
            data={
                "title": "New",
                "content": "New content",
                "enabled": "y",
                "publish_date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M"),
                "category": "other",
            },
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"New content", resp.data)

    def test_delete_post(self):
        """Delete route should remove a post."""
        p = Post(title="To delete", content="X")
        db.session.add(p)
        db.session.commit()

        resp_get = self.client.get(f"/post/{p.id}/delete")
        self.assertEqual(resp_get.status_code, 200)

        resp_post = self.client.post(
            f"/post/{p.id}/delete",
            follow_redirects=True,
        )
        self.assertEqual(resp_post.status_code, 200)
        self.assertEqual(Post.query.count(), 0)

    def test_404_handler(self):
        """Requesting nonexistent post should return 404 page."""
        resp = self.client.get("/post/9999")
        self.assertEqual(resp.status_code, 404)
        self.assertIn(b"404", resp.data)

    def test_list_shows_only_active_posts(self):
        """Only active posts should be visible on /post."""
        p1 = Post(title="Active", content="C1", is_active=True)
        p2 = Post(title="Inactive", content="C2", is_active=False)

        db.session.add_all([p1, p2])
        db.session.commit()

        resp = self.client.get("/post")
        self.assertEqual(resp.status_code, 200)

        # Active post appears
        self.assertIn(b"Active", resp.data)

        # Inactive post must not appear
        self.assertNotIn(b"Inactive", resp.data)


if __name__ == "__main__":
    unittest.main()
