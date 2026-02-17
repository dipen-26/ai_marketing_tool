from django.db import models


class Project(models.Model):
    business_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    target_audience = models.TextField()
    location = models.CharField(max_length=255, default="")
    goal = models.CharField(max_length=50, default="Engagement")
    tone = models.CharField(max_length=50, default="Professional")
    number_of_posts = models.PositiveIntegerField(default=5)
    temperature = models.DecimalField(max_digits=3, decimal_places=2, default=0.30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name} ({self.industry})"


class GeneratedPost(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="generated_posts"
    )
    post_number = models.PositiveIntegerField(default=1)
    post_topic = models.CharField(max_length=255, default="General Post")
    caption = models.TextField()
    linkedin_version = models.TextField(default="")
    instagram_version = models.TextField(default="")
    facebook_version = models.TextField(default="")
    hashtags = models.JSONField(default=list, blank=True)
    cta = models.CharField(max_length=500)
    image_prompt = models.TextField()
    creative_type = models.CharField(max_length=100, default="Static Post")
    text_overlay_suggestion = models.CharField(max_length=255, default="")
    color_theme_suggestion = models.CharField(max_length=255, default="")
    publish_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def hashtag_string(self):
        tags = []
        for tag in self.hashtags:
            tag = str(tag).strip()
            if tag and not tag.startswith("#"):
                tag = f"#{tag}"
            if tag:
                tags.append(tag)
        return " ".join(tags)

    def __str__(self):
        return f"Post {self.post_number} for Project #{self.project_id}"
