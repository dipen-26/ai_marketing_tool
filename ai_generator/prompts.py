import json


SYSTEM_PROMPT = """
You are an expert social media strategist and creative director.
Return only valid JSON that matches the requested schema exactly.
Do not include markdown, commentary, or extra keys.
""".strip()


def build_user_prompt(project_data: dict) -> str:
    schema = {
        "generated_posts": [
            {
                "post_topic": "Specific angle/topic for this post",
                "caption": "Platform-neutral base caption",
                "instagram_version": "Instagram-tailored caption",
                "linkedin_version": "LinkedIn-tailored caption",
                "facebook_version": "Facebook-tailored caption",
                "hashtags": ["tag1", "tag2", "tag3"],
                "cta": "Clear call-to-action",
                "image_prompt": "Prompt for image generation",
                "creative_type": "Carousel | Reel | Static Post",
                "text_overlay_suggestion": "Short visual overlay line",
                "color_theme_suggestion": "2-3 color direction",
            }
        ]
    }

    number_of_posts = int(project_data.get("number_of_posts") or 5)
    instructions = {
        "task": f"Generate exactly {number_of_posts} social media posts.",
        "requirements": [
            "Tone must match the requested tone.",
            "Each post must be unique and non-repetitive.",
            "Provide platform versions for Instagram, LinkedIn, and Facebook for every post.",
            "Hashtags should be relevant and not spammy.",
            "Each post must include post_topic, caption, instagram_version, linkedin_version, facebook_version, hashtags, cta, image_prompt, creative_type, text_overlay_suggestion, color_theme_suggestion.",
            "image_prompt should be concise and production-ready for text-to-image tools.",
            "creative_type must be one of: Carousel, Reel, Static Post.",
            "Return JSON only with key: generated_posts.",
            f"generated_posts must contain exactly {number_of_posts} objects.",
        ],
        "project_data": project_data,
        "output_schema_example": schema,
    }

    return json.dumps(instructions, indent=2)
