from django.db import models
from authentication.models import User
from api.models.post_model import Post
from api.models.company_model import Company
from api.models.product_model import Product
from api.models.service_model import Service

class FollowingRelationships(models.Model):
    user_follower = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="following", null=True
    )
    user_following = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="followers", null=True
    )
    company_follower = models.ForeignKey(
        Company, on_delete=models.SET_NULL, related_name="following", null=True
    )
    company_following = models.ForeignKey(
        Company, on_delete=models.SET_NULL, related_name="followers", null=True
    )
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user_follower", "user_following")

    def __str__(self):
        follower = self.user_follower or self.company_follower
        following = self.user_following or self.company_following
        return f"{follower} follows {following}"

class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", null=True, blank=True
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="comments", null=True, blank=True
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-commented_at"]

    def __str__(self):
        author = self.user or self.company
        return f"Comment by {author} at {self.commented_at}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="likes")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, related_name="likes")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="likes")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together =  [["user", "post"], 
                            ["user", "product"], 
                            ["user", "service"]
                        ]
        ordering = ["-liked_at"]

    def __str__(self):
        return f"Like by {self.user} at {self.liked_at}"