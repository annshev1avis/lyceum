from django import forms

import feedback.models


__all__ = []


class BootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class FeedbackAuthorForm(BootstrapForm):
    class Meta:
        model = feedback.models.FeedbackAuthor
        exclude = ["feedback"]


class FeedbackForm(BootstrapForm):
    class Meta:
        model = feedback.models.Feedback
        exclude = ["status", "created_on"]


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class FeedbackFilesForm(BootstrapForm):
    class Meta:
        model = feedback.models.FeedbackFile
        fields = ["file"]
        help_texts = {"file": "Если необходимо, загрузите файлы"}
        widgets = {
            "file": MultipleFileInput(
                attrs={
                    "class": "form-control",
                    "type": "file",
                    "multiple": True,
                },
            ),
        }
