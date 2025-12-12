import json
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import ABTestButtonClick, ABTestPageView, Dislike, Like, Post


class PostCreationTests(TestCase):
    """Tests for post creation functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_create_post_valid(self):
        """Test creating a post with valid data."""
        response = self.client.post(
            reverse("create_post"),
            {
                "title": "Test Post",
                "description": "This is a test description",
                "hours_procrastinated": "5.5",
            },
        )

        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Post.objects.filter(title="Test Post").exists())
        post = Post.objects.get(title="Test Post")
        self.assertEqual(post.author, self.user)
        self.assertEqual(float(post.hours_procrastinated), 5.5)

    def test_create_post_missing_title(self):
        """Test creating a post without a title."""
        response = self.client.post(
            reverse("create_post"),
            {
                "description": "This is a test description",
                "hours_procrastinated": "5.5",
            },
        )

        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        self.assertFalse(
            Post.objects.filter(description="This is a test description").exists()
        )

    def test_create_post_missing_description(self):
        """Test creating a post without a description."""
        response = self.client.post(
            reverse("create_post"),
            {"title": "Test Post", "hours_procrastinated": "5.5"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(title="Test Post").exists())

    def test_create_post_missing_hours(self):
        """Test creating a post without hours procrastinated."""
        response = self.client.post(
            reverse("create_post"),
            {"title": "Test Post", "description": "This is a test description"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(title="Test Post").exists())

    def test_create_post_negative_hours(self):
        """Test creating a post with negative hours."""
        response = self.client.post(
            reverse("create_post"),
            {
                "title": "Test Post",
                "description": "This is a test description",
                "hours_procrastinated": "-5",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(title="Test Post").exists())

    def test_create_post_invalid_hours(self):
        """Test creating a post with invalid hours format."""
        response = self.client.post(
            reverse("create_post"),
            {
                "title": "Test Post",
                "description": "This is a test description",
                "hours_procrastinated": "not_a_number",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(title="Test Post").exists())

    def test_create_post_requires_login(self):
        """Test that creating a post requires authentication."""
        self.client.logout()
        response = self.client.post(
            reverse("create_post"),
            {
                "title": "Test Post",
                "description": "This is a test description",
                "hours_procrastinated": "5.5",
            },
        )

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(title="Test Post").exists())


class LikePostTests(TestCase):
    """Tests for liking posts functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="testpass123"
        )
        self.post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            hours_procrastinated=5.5,
            author=self.user1,
        )
        self.client.login(username="user2", password="testpass123")

    def test_like_post(self):
        """Test liking a post."""
        response = self.client.post(reverse("like_post", args=[self.post.id]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["liked"])
        self.assertEqual(data["like_count"], 1)
        self.assertTrue(Like.objects.filter(user=self.user2, post=self.post).exists())

    def test_unlike_post(self):
        """Test unliking a post."""
        # First like the post
        Like.objects.create(user=self.user2, post=self.post)

        # Then unlike it
        response = self.client.post(reverse("like_post", args=[self.post.id]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data["liked"])
        self.assertEqual(data["like_count"], 0)
        self.assertFalse(Like.objects.filter(user=self.user2, post=self.post).exists())

    def test_like_post_removes_dislike(self):
        """Test that liking a post removes any existing dislike."""
        # First dislike the post
        Dislike.objects.create(user=self.user2, post=self.post)
        self.assertEqual(self.post.get_dislike_count(), 1)

        # Then like it
        response = self.client.post(reverse("like_post", args=[self.post.id]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["liked"])
        self.assertFalse(data["disliked"])
        self.assertEqual(data["dislike_count"], 0)
        self.assertTrue(Like.objects.filter(user=self.user2, post=self.post).exists())
        self.assertFalse(
            Dislike.objects.filter(user=self.user2, post=self.post).exists()
        )

    def test_multiple_users_like_post(self):
        """Test that multiple users can like the same post."""
        user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="testpass123"
        )

        # User2 likes
        self.client.post(reverse("like_post", args=[self.post.id]))

        # User3 likes
        self.client.login(username="user3", password="testpass123")
        response = self.client.post(reverse("like_post", args=[self.post.id]))

        data = json.loads(response.content)
        self.assertEqual(data["like_count"], 2)
        self.assertEqual(Like.objects.filter(post=self.post).count(), 2)

    def test_like_post_requires_login(self):
        """Test that liking a post requires authentication."""
        self.client.logout()
        response = self.client.post(reverse("like_post", args=[self.post.id]))

        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_like_post_invalid_id(self):
        """Test liking a post that doesn't exist."""
        response = self.client.post(reverse("like_post", args=[99999]))
        self.assertEqual(response.status_code, 404)


class DislikePostTests(TestCase):
    """Tests for disliking posts functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="testpass123"
        )
        self.post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            hours_procrastinated=5.5,
            author=self.user1,
        )
        self.client.login(username="user2", password="testpass123")

    def test_dislike_post(self):
        """Test disliking a post."""
        response = self.client.post(reverse("dislike_post", args=[self.post.id]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["disliked"])
        self.assertEqual(data["dislike_count"], 1)
        self.assertTrue(
            Dislike.objects.filter(user=self.user2, post=self.post).exists()
        )

    def test_undislike_post(self):
        """Test undisliking a post."""
        # First dislike the post
        Dislike.objects.create(user=self.user2, post=self.post)

        # Then undislike it
        response = self.client.post(reverse("dislike_post", args=[self.post.id]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data["disliked"])
        self.assertEqual(data["dislike_count"], 0)
        self.assertFalse(
            Dislike.objects.filter(user=self.user2, post=self.post).exists()
        )

    def test_dislike_post_removes_like(self):
        """Test that disliking a post removes any existing like."""
        # First like the post
        Like.objects.create(user=self.user2, post=self.post)
        self.assertEqual(self.post.get_like_count(), 1)

        # Then dislike it
        response = self.client.post(reverse("dislike_post", args=[self.post.id]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["disliked"])
        self.assertFalse(data["liked"])
        self.assertEqual(data["like_count"], 0)
        self.assertTrue(
            Dislike.objects.filter(user=self.user2, post=self.post).exists()
        )
        self.assertFalse(Like.objects.filter(user=self.user2, post=self.post).exists())

    def test_multiple_users_dislike_post(self):
        """Test that multiple users can dislike the same post."""
        user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="testpass123"
        )

        # User2 dislikes
        self.client.post(reverse("dislike_post", args=[self.post.id]))

        # User3 dislikes
        self.client.login(username="user3", password="testpass123")
        response = self.client.post(reverse("dislike_post", args=[self.post.id]))

        data = json.loads(response.content)
        self.assertEqual(data["dislike_count"], 2)
        self.assertEqual(Dislike.objects.filter(post=self.post).count(), 2)

    def test_dislike_post_requires_login(self):
        """Test that disliking a post requires authentication."""
        self.client.logout()
        response = self.client.post(reverse("dislike_post", args=[self.post.id]))

        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_dislike_post_invalid_id(self):
        """Test disliking a post that doesn't exist."""
        response = self.client.post(reverse("dislike_post", args=[99999]))
        self.assertEqual(response.status_code, 404)


class LeaderboardTests(TestCase):
    """Tests for leaderboard functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="testpass123"
        )
        self.client.login(username="user1", password="testpass123")

        # Create posts with different like/dislike counts
        self.post1 = Post.objects.create(
            title="Post 1",
            description="Description 1",
            hours_procrastinated=1.0,
            author=self.user1,
        )
        self.post2 = Post.objects.create(
            title="Post 2",
            description="Description 2",
            hours_procrastinated=2.0,
            author=self.user2,
        )
        self.post3 = Post.objects.create(
            title="Post 3",
            description="Description 3",
            hours_procrastinated=3.0,
            author=self.user1,
        )

        # Add likes and dislikes
        Like.objects.create(user=self.user1, post=self.post1)
        Like.objects.create(user=self.user2, post=self.post1)
        Like.objects.create(user=self.user1, post=self.post2)

        Dislike.objects.create(user=self.user2, post=self.post3)
        Dislike.objects.create(user=self.user1, post=self.post3)

    def test_leaderboard_sort_by_likes(self):
        """Test leaderboard sorted by likes (default)."""
        response = self.client.get(reverse("leaderboard"))

        self.assertEqual(response.status_code, 200)
        posts = list(response.context["posts"])
        # Post 1 has 2 likes, Post 2 has 1 like, Post 3 has 0 likes
        self.assertEqual(posts[0].id, self.post1.id)
        self.assertEqual(posts[1].id, self.post2.id)
        self.assertEqual(posts[2].id, self.post3.id)

    def test_leaderboard_sort_by_dislikes(self):
        """Test leaderboard sorted by dislikes."""
        response = self.client.get(reverse("leaderboard"), {"sort": "dislikes"})

        self.assertEqual(response.status_code, 200)
        posts = list(response.context["posts"])
        # Post 3 has 2 dislikes, others have 0
        self.assertEqual(posts[0].id, self.post3.id)

    def test_leaderboard_sort_by_time(self):
        """Test leaderboard sorted by time."""
        response = self.client.get(reverse("leaderboard"), {"sort": "time"})

        self.assertEqual(response.status_code, 200)
        posts = list(response.context["posts"])
        # Should be in reverse chronological order (newest first)
        self.assertEqual(posts[0].id, self.post3.id)
        self.assertEqual(posts[1].id, self.post2.id)
        self.assertEqual(posts[2].id, self.post1.id)


class UserLeaderboardTests(TestCase):
    """Tests for user leaderboard functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="testpass123"
        )
        self.user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="testpass123"
        )
        self.client.login(username="user1", password="testpass123")

        # Create posts with different hours
        Post.objects.create(
            title="Post 1",
            description="Description 1",
            hours_procrastinated=10.0,
            author=self.user1,
        )
        Post.objects.create(
            title="Post 2",
            description="Description 2",
            hours_procrastinated=5.0,
            author=self.user1,
        )
        Post.objects.create(
            title="Post 3",
            description="Description 3",
            hours_procrastinated=20.0,
            author=self.user2,
        )
        # User3 has no posts

    def test_user_leaderboard_ranking(self):
        """Test user leaderboard shows users ranked by total hours."""
        response = self.client.get(reverse("user_leaderboard"))

        self.assertEqual(response.status_code, 200)
        users = list(response.context["users"])

        # User2 has 20 hours, User1 has 15 hours
        self.assertEqual(users[0].username, "user2")
        self.assertEqual(users[1].username, "user1")
        # User3 should not appear (no posts)
        self.assertNotIn(self.user3, users)

    def test_user_leaderboard_total_hours(self):
        """Test that user leaderboard calculates total hours correctly."""
        response = self.client.get(reverse("user_leaderboard"))

        self.assertEqual(response.status_code, 200)
        users = list(response.context["users"])

        user1_data = next(u for u in users if u.username == "user1")
        self.assertEqual(float(user1_data.total_hours), 15.0)

        user2_data = next(u for u in users if u.username == "user2")
        self.assertEqual(float(user2_data.total_hours), 20.0)


class CheckNewPostsTests(TestCase):
    """Tests for checking new posts functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        # Create an old post
        self.old_post = Post.objects.create(
            title="Old Post",
            description="Old Description",
            hours_procrastinated=1.0,
            author=self.user,
        )
        # Manually set created_at to be older
        self.old_post.created_at = timezone.now() - timedelta(hours=2)
        self.old_post.save()

    def test_check_new_posts_with_timestamp(self):
        """Test checking for new posts since a timestamp."""
        # Create a new post
        new_post = Post.objects.create(
            title="New Post",
            description="New Description",
            hours_procrastinated=2.0,
            author=self.user,
        )

        # Get timestamp from 1 hour ago
        since = (timezone.now() - timedelta(hours=1)).isoformat()

        response = self.client.get(reverse("check_new_posts"), {"since": since})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["new_posts"][0]["id"], new_post.id)
        self.assertEqual(data["new_posts"][0]["title"], "New Post")

    def test_check_new_posts_no_new_posts(self):
        """Test checking for new posts when there are none."""
        since = (timezone.now() - timedelta(minutes=30)).isoformat()

        response = self.client.get(reverse("check_new_posts"), {"since": since})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["count"], 0)
        self.assertEqual(len(data["new_posts"]), 0)

    def test_check_new_posts_without_timestamp(self):
        """Test checking for new posts without providing a timestamp."""
        response = self.client.get(reverse("check_new_posts"))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["count"], 0)

    def test_check_new_posts_invalid_timestamp(self):
        """Test checking for new posts with invalid timestamp format."""
        response = self.client.get(
            reverse("check_new_posts"), {"since": "invalid_timestamp"}
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["count"], 0)

    def test_check_new_posts_includes_like_dislike_counts(self):
        """Test that new posts response includes like and dislike counts."""
        new_post = Post.objects.create(
            title="New Post",
            description="New Description",
            hours_procrastinated=2.0,
            author=self.user,
        )

        # Add likes and dislikes
        Like.objects.create(user=self.user, post=new_post)
        Dislike.objects.create(user=self.user, post=new_post)

        since = (timezone.now() - timedelta(hours=1)).isoformat()
        response = self.client.get(reverse("check_new_posts"), {"since": since})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["new_posts"][0]["like_count"], 1)
        self.assertEqual(data["new_posts"][0]["dislike_count"], 1)


class ABTestAnalyticsTests(TestCase):
    """Tests for A/B test analytics functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()

    def test_abtest_page_view_tracking(self):
        """Test that A/B test page views are tracked."""
        response = self.client.get(reverse("abtest"))

        self.assertEqual(response.status_code, 200)
        # Should have created a page view record
        self.assertEqual(ABTestPageView.objects.count(), 1)

        page_view = ABTestPageView.objects.first()
        self.assertIn(page_view.variant, ["A", "B"])
        self.assertIsNotNone(page_view.created_at)

    def test_abtest_button_click_tracking(self):
        """Test that A/B test button clicks are tracked."""
        response = self.client.post(
            reverse("abtest_button_click"),
            {"variant": "A"},
            HTTP_X_FORWARDED_FOR="192.168.1.1",
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["success"])

        # Should have created a button click record
        self.assertEqual(ABTestButtonClick.objects.count(), 1)
        click = ABTestButtonClick.objects.first()
        self.assertEqual(click.variant, "A")

    def test_abtest_button_click_invalid_variant(self):
        """Test that invalid variant is rejected."""
        response = self.client.post(reverse("abtest_button_click"), {"variant": "C"})

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)
        self.assertEqual(ABTestButtonClick.objects.count(), 0)

    def test_abtest_button_click_count_by_variant(self):
        """Test getting click counts by variant."""
        # Create some button clicks
        ABTestButtonClick.objects.create(variant="A", ip_address="192.168.1.1")
        ABTestButtonClick.objects.create(variant="A", ip_address="192.168.1.2")
        ABTestButtonClick.objects.create(variant="B", ip_address="192.168.1.3")

        # Click variant A
        response = self.client.post(reverse("abtest_button_click"), {"variant": "A"})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["click_count_a"], 3)  # 2 existing + 1 new
        self.assertEqual(data["click_count_b"], 1)

    def test_abtest_button_click_get_method_rejected(self):
        """Test that GET method is rejected for button click endpoint."""
        response = self.client.get(reverse("abtest_button_click"))
        self.assertEqual(response.status_code, 400)

    def test_abtest_page_view_stores_ip_address(self):
        """Test that page views store IP address."""
        response = self.client.get(
            reverse("abtest"), HTTP_X_FORWARDED_FOR="192.168.1.1"
        )

        self.assertEqual(response.status_code, 200)
        page_view = ABTestPageView.objects.first()
        self.assertEqual(page_view.ip_address, "192.168.1.1")

    def test_abtest_button_click_stores_ip_address(self):
        """Test that button clicks store IP address."""
        response = self.client.post(
            reverse("abtest_button_click"),
            {"variant": "B"},
            HTTP_X_FORWARDED_FOR="192.168.1.2",
        )

        self.assertEqual(response.status_code, 200)
        click = ABTestButtonClick.objects.first()
        self.assertEqual(click.ip_address, "192.168.1.2")
        self.assertEqual(click.variant, "B")


class PostModelTests(TestCase):
    """Tests for Post model methods."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            hours_procrastinated=5.5,
            author=self.user,
        )

    def test_get_like_count(self):
        """Test get_like_count method."""
        self.assertEqual(self.post.get_like_count(), 0)

        Like.objects.create(user=self.user, post=self.post)
        self.assertEqual(self.post.get_like_count(), 1)

        user2 = User.objects.create_user(username="user2", password="testpass123")
        Like.objects.create(user=user2, post=self.post)
        self.assertEqual(self.post.get_like_count(), 2)

    def test_get_dislike_count(self):
        """Test get_dislike_count method."""
        self.assertEqual(self.post.get_dislike_count(), 0)

        Dislike.objects.create(user=self.user, post=self.post)
        self.assertEqual(self.post.get_dislike_count(), 1)

        user2 = User.objects.create_user(username="user2", password="testpass123")
        Dislike.objects.create(user=user2, post=self.post)
        self.assertEqual(self.post.get_dislike_count(), 2)

    def test_post_str_representation(self):
        """Test Post string representation."""
        self.assertEqual(str(self.post), f"Test Post by {self.user.username}")


class HomeViewTests(TestCase):
    """Tests for home view functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_home_view_requires_login(self):
        """Test that home view requires authentication."""
        self.client.logout()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_home_view_shows_posts(self):
        """Test that home view displays posts."""
        post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            hours_procrastinated=5.5,
            author=self.user,
        )

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(post, response.context["posts"])

    def test_home_view_shows_user_liked_posts(self):
        """Test that home view tracks which posts user has liked."""
        post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            hours_procrastinated=5.5,
            author=self.user,
        )
        Like.objects.create(user=self.user, post=post)

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(post.id, response.context["user_liked_posts"])

    def test_home_view_shows_user_disliked_posts(self):
        """Test that home view tracks which posts user has disliked."""
        post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            hours_procrastinated=5.5,
            author=self.user,
        )
        Dislike.objects.create(user=self.user, post=post)

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(post.id, response.context["user_disliked_posts"])
