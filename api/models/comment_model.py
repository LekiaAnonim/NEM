from django.db import models
from authentication.models import User

class FollowingRelationships(models.Model):
    user_follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    user_following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    company_follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    company_following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower} follows {self.following}"

class Comment(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-commented_at"]

    def __str__(self):
        return f"Comment by {self.author} at {self.commented_at}"


class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("profile", "post")
        ordering = ["-liked_at"]

    def __str__(self):
        return f"Like by {self.profile} at {self.liked_at}"