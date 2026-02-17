from datetime import timedelta

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Count
from django.views.decorators.http import require_POST

from .forms import ProjectForm
from .models import GeneratedPost, Project
from .services import generate_posts_for_project


def _render_project_results(request, project):
    posts = project.generated_posts.all().order_by("post_number")
    return render(
        request,
        "ai_generator/results.html",
        {"project": project, "posts": posts},
    )


def project_input_view(request):
    error_message = None

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()

            try:
                generated_posts = generate_posts_for_project(project)
                start_date = timezone.now().date()
                for index, item in enumerate(generated_posts, start=1):
                    GeneratedPost.objects.create(
                        project=project,
                        post_number=index,
                        post_topic=item["post_topic"],
                        caption=item["caption"],
                        linkedin_version=item["linkedin_version"],
                        instagram_version=item["instagram_version"],
                        facebook_version=item["facebook_version"],
                        hashtags=item["hashtags"],
                        cta=item["cta"],
                        image_prompt=item["image_prompt"],
                        creative_type=item["creative_type"],
                        text_overlay_suggestion=item["text_overlay_suggestion"],
                        color_theme_suggestion=item["color_theme_suggestion"],
                        publish_at=start_date + timedelta(days=index - 1),
                    )

                return _render_project_results(request, project)
            except Exception as exc:
                error_message = f"Generation failed: {exc}"
    else:
        form = ProjectForm()

    return render(
        request,
        "ai_generator/project_form.html",
        {"form": form, "error_message": error_message},
    )


def project_records_view(request):
    projects = Project.objects.annotate(post_count=Count("generated_posts")).order_by(
        "-created_at"
    )
    return render(request, "ai_generator/project_records.html", {"projects": projects})


def project_results_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return _render_project_results(request, project)


@require_POST
def delete_project_record(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    business_name = project.business_name
    project.delete()
    messages.success(request, f"Deleted record for {business_name}.")
    return redirect("project_records")


def export_project_txt(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    posts = project.generated_posts.all().order_by("post_number")
    lines = [
        f"Project: {project.business_name}",
        f"Industry: {project.industry}",
        f"Target Audience: {project.target_audience}",
        f"Location: {project.location}",
        f"Goal: {project.goal}",
        f"Tone: {project.tone}",
        "",
    ]
    for post in posts:
        lines.extend(
            [
                f"Post {post.post_number}: {post.post_topic}",
                f"Caption: {post.caption}",
                f"Instagram: {post.instagram_version}",
                f"LinkedIn: {post.linkedin_version}",
                f"Facebook: {post.facebook_version}",
                f"Hashtags: {post.hashtag_string()}",
                f"CTA: {post.cta}",
                f"Image Prompt: {post.image_prompt}",
                f"Creative Type: {post.creative_type}",
                f"Text Overlay: {post.text_overlay_suggestion}",
                f"Color Theme: {post.color_theme_suggestion}",
                f"Suggested Publish Date: {post.publish_at}",
                "",
            ]
        )
    response = HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")
    response["Content-Disposition"] = (
        f'attachment; filename="project_{project.id}_posts.txt"'
    )
    return response
