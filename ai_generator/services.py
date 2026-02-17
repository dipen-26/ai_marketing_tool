import json
import os
import re
from typing import Any, Dict, List

from .prompts import SYSTEM_PROMPT, build_user_prompt


def _is_quota_error(exc: Exception) -> bool:
    message = str(exc).lower()
    status_code = getattr(exc, "status_code", None)
    return (
        status_code == 429
        or "insufficient_quota" in message
        or "quota exceeded" in message
        or "rate limit" in message
        or "too many requests" in message
        or " 429 " in f" {message} "
        or message.startswith("429")
    )


def _is_model_not_found_error(exc: Exception) -> bool:
    message = str(exc).lower()
    status_code = getattr(exc, "status_code", None)
    return (
        status_code == 404
        or "not found" in message
        or "not supported for generatecontent" in message
    )


def _build_gemini_model_candidates() -> List[str]:
    configured = os.getenv("GEMINI_MODEL", "").strip()
    # Ordered fallbacks with lower-cost models first for free-tier usage.
    defaults = [
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
    ]
    candidates: List[str] = []
    for name in [configured, *defaults]:
        if name and name not in candidates:
            candidates.append(name)
    return candidates


def _offline_fallback_posts(project_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    business = project_data.get("business_name", "Your Business")
    industry = project_data.get("industry", "your industry")
    audience = project_data.get("target_audience", "your audience")
    tone = project_data.get("tone", "Professional")
    goal = project_data.get("goal", "Engagement")
    count = int(project_data.get("number_of_posts") or 5)
    posts: List[Dict[str, Any]] = []
    for idx in range(1, count + 1):
        topic = f"{industry} Value Angle {idx}"
        caption = (
            f"{business} helps {audience} in {industry}. "
            f"This {tone.lower()} post focuses on {goal.lower()} outcomes."
        )
        posts.append(
            {
                "post_topic": topic,
                "caption": caption,
                "instagram_version": f"{caption} Save this for your next purchase decision.",
                "linkedin_version": f"{caption} Built for measurable business value.",
                "facebook_version": f"{caption} Share with someone who needs this.",
                "hashtags": [
                    industry.replace(" ", ""),
                    business.replace(" ", ""),
                    "Marketing",
                    "Growth",
                ],
                "cta": "Message us to get started today.",
                "image_prompt": f"{business} {industry} premium marketing visual",
                "creative_type": "Static Post",
                "text_overlay_suggestion": f"{business}: {topic}",
                "color_theme_suggestion": "Gold, Ivory, Deep Maroon",
            }
        )
    return posts


def _extract_json(text: str) -> Dict[str, Any]:
    cleaned = text.strip()
    cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def _normalize_posts(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    posts = payload.get("generated_posts", [])
    normalized = []
    for post in posts:
        normalized.append(
            {
                "post_topic": post.get("post_topic", "").strip(),
                "caption": post.get("caption", "").strip(),
                "instagram_version": post.get("instagram_version", "").strip(),
                "linkedin_version": post.get("linkedin_version", "").strip(),
                "facebook_version": post.get("facebook_version", "").strip(),
                "hashtags": post.get("hashtags", []),
                "cta": post.get("cta", "").strip(),
                "image_prompt": post.get("image_prompt", "").strip(),
                "creative_type": post.get("creative_type", "").strip(),
                "text_overlay_suggestion": post.get("text_overlay_suggestion", "").strip(),
                "color_theme_suggestion": post.get("color_theme_suggestion", "").strip(),
            }
        )
    return normalized


def _generate_with_gemini(
    user_prompt: str, *, temperature: float, max_output_tokens: int
) -> Dict[str, Any]:
    from google import genai
    from google.genai import types

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing GEMINI_API_KEY. Set it in your environment or .env file."
        )

    client = genai.Client(api_key=api_key)
    tried_models: List[str] = []
    last_exc: Exception | None = None

    for model_name in _build_gemini_model_candidates():
        tried_models.append(model_name)
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[f"{SYSTEM_PROMPT}\n\n{user_prompt}"],
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                ),
            )
            text = getattr(response, "text", None)
            if not text and getattr(response, "parts", None):
                text = "\n".join(
                    part.text for part in response.parts if getattr(part, "text", None)
                )
            text = text or "{}"
            return _extract_json(text)
        except Exception as exc:
            last_exc = exc
            if _is_model_not_found_error(exc):
                continue
            raise

    raise ValueError(
        "No supported Gemini model found for generateContent. "
        f"Tried: {', '.join(tried_models)}"
    ) from last_exc


def generate_posts_for_project(project) -> List[Dict[str, Any]]:
    count = int(project.number_of_posts or 5)
    project_data = {
        "business_name": project.business_name,
        "industry": project.industry,
        "target_audience": project.target_audience,
        "location": project.location,
        "goal": project.goal,
        "tone": project.tone,
        "number_of_posts": count,
    }
    user_prompt = build_user_prompt(project_data)
    temperature = max(0.0, min(float(project.temperature), 1.0))
    max_output_tokens = min(2200, max(800, count * 350))

    try:
        payload = _generate_with_gemini(
            user_prompt,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )
    except Exception as exc:
        if _is_quota_error(exc):
            raise ValueError(
                "Gemini API quota/rate-limit exceeded. Check billing, active project, and key restrictions."
            ) from exc
        payload = {"generated_posts": _offline_fallback_posts(project_data)}

    posts = _normalize_posts(payload)[:count]
    if len(posts) < count:
        posts.extend(_offline_fallback_posts(project_data)[len(posts) : count])

    if not posts:
        raise ValueError("AI provider returned no posts.")

    return posts[:count]
