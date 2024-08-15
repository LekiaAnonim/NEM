from django.db import models
# from wagtail.fields import RichTextField
from api.models.company_model import Company
from django.utils import timezone
# Below the other imports:
from django_comments_xtd.moderation import moderator, SpamModerator
from api.badwords import badwords



class PostManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(status="PUB",
                                          publish__lte=timezone.now())

class Post(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
    )
    body = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES,
                              default="DRAFT")
    
    objects = PostManager()

    class Meta:
        ordering = ('-date_created',)
    


class PostCommentModerator(SpamModerator):
    email_notification = True
    removal_suggestion_notification = True
    def moderate(self, comment, content_object, request):
        # Make a dictionary where the keys are the words of the message
        # and the values are their relative position in the message.
        def clean(word):
            ret = word
            if word.startswith('.') or word.startswith(','):
                ret = word[1:]
            if word.endswith('.') or word.endswith(','):
                ret = word[:-1]
            return ret

        lowcase_comment = comment.comment.lower()
        msg = dict([
            (clean(w), i)
            for i, w in enumerate(lowcase_comment.split())
        ])

        for badword in badwords:
            if isinstance(badword, str):
                if lowcase_comment.find(badword) > -1:
                    return True
            else:
                lastindex = -1
                for subword in badword:
                    if subword in msg:
                        if lastindex > -1:
                            if msg[subword] == (lastindex + 1):
                                lastindex = msg[subword]
                        else:
                            lastindex = msg[subword]
                    else:
                        break
                if msg.get(badword[-1]) and msg[badword[-1]] == lastindex:
                    return True

        return super(PostCommentModerator, self).moderate(
            comment, content_object, request
        )

moderator.register(Post, PostCommentModerator)
