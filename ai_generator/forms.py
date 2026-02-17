from django import forms
from .models import Project

GOAL_CHOICES = [
    ("Leads", "Leads"),
    ("Branding", "Branding"),
    ("Sales", "Sales"),
    ("Engagement", "Engagement"),
]

TONE_CHOICES = [
    ("Professional", "Professional"),
    ("Friendly", "Friendly"),
    ("Bold", "Bold"),
    ("Educational", "Educational"),
]


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["number_of_posts"].initial = 5
        self.fields["temperature"].initial = 0.3

    class Meta:
        model = Project
        fields = [
            "business_name",
            "industry",
            "target_audience",
            "location",
            "goal",
            "tone",
            "number_of_posts",
            "temperature",
        ]
        widgets = {
            "target_audience": forms.Textarea(attrs={"rows": 3}),
            "goal": forms.Select(choices=GOAL_CHOICES),
            "tone": forms.Select(choices=TONE_CHOICES),
            "number_of_posts": forms.NumberInput(attrs={"min": 1, "max": 10}),
            "temperature": forms.NumberInput(
                attrs={"min": 0, "max": 1, "step": 0.1}
            ),
        }

    def clean_number_of_posts(self):
        count = self.cleaned_data["number_of_posts"]
        if count < 1 or count > 10:
            raise forms.ValidationError("Number of posts must be between 1 and 10.")
        return count
