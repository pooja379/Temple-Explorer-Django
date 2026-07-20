from django import forms
from .models import Temple, Review


class TempleForm(forms.ModelForm):

    class Meta:
        model = Temple
        fields = "__all__"


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            "username",
            "rating",
            "review"
        ]

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border rounded-lg",
                    "placeholder": "Your Name"
                }
            ),

            "rating": forms.Select(
                choices=[
                    (5, "⭐⭐⭐⭐⭐ Excellent"),
                    (4, "⭐⭐⭐⭐ Very Good"),
                    (3, "⭐⭐⭐ Good"),
                    (2, "⭐⭐ Fair"),
                    (1, "⭐ Poor"),
                ],
                attrs={
                    "class": "w-full p-3 border rounded-lg"
                }
            ),

            "review": forms.Textarea(
                attrs={
                    "class": "w-full p-3 border rounded-lg",
                    "rows": 5,
                    "placeholder": "Write your review..."
                }
            )

        }