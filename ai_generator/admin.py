from django.contrib import admin
from .models import Project, GeneratedPost


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "business_name",
        "industry",
        "location",
        "goal",
        "tone",
        "number_of_posts",
        "created_at",
    )
    search_fields = ("business_name", "industry", "target_audience", "location")
    list_filter = ("goal", "tone", "created_at")


@admin.register(GeneratedPost)
class GeneratedPostAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "post_number", "post_topic", "creative_type", "publish_at")
    search_fields = ("caption", "cta", "post_topic")
    list_filter = ("creative_type", "publish_at", "created_at")
