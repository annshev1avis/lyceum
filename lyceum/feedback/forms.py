from django import forms

from feedback.models import Feedback


__all__ = []


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Feedback
        fields = [
            "name",
            "text",
            "mail",
        ]
        # TODO: сделать красивое отображение полей формы
