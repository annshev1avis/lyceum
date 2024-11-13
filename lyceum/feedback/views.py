import django.conf
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from feedback.forms import FeedbackAuthorForm, FeedbackFilesForm, FeedbackForm
from feedback.models import Feedback, FeedbackAuthor, FeedbackFile


__all__ = []


def handle_feedback_form(request):
    author_form = FeedbackAuthorForm(request.POST or None)
    feedback_form = FeedbackForm(request.POST or None)
    files_form = FeedbackFilesForm((request.POST, request.FILES) or None)

    if request.method == "POST":
        if all(
            form.is_valid()
            for form in (author_form, feedback_form, files_form)
        ):

            feedback = Feedback.objects.create(
                **feedback_form.cleaned_data,
            )

            FeedbackAuthor.objects.create(
                **author_form.cleaned_data,
                feedback=feedback,
            )

            for file in request.FILES.getlist("file"):
                FeedbackFile.objects.create(
                    file=file,
                    feedback=feedback,
                )

            send_mail(
                subject="Racoon's answer",
                message=feedback.text,
                from_email=django.conf.settings.DJANGO_MAIL,
                recipient_list=[feedback.author.mail],
            )

            messages.success(request, "Форма успешно отправлена! :)")
            return redirect(reverse("feedback:feedback"))

    context = {
        "title": "Обратная связь",
        "author": author_form,
        "content": feedback_form,
        "files": files_form,
    }

    return render(request, "feedback/feedback.html", context)
