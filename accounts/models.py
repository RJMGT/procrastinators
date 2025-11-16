from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    """Model for procrastination posts."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    hours_procrastinated = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def get_like_count(self):
        """Get the total number of likes for this post."""
        return self.likes.count()
    
    def get_dislike_count(self):
        """Get the total number of dislikes for this post."""
        return self.dislikes.count()


class Like(models.Model):
    """Model to track which users liked which posts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']  # Prevent duplicate likes
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"


class Dislike(models.Model):
    """Model to track which users disliked which posts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']  # Prevent duplicate dislikes
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} disliked {self.post.title}"

