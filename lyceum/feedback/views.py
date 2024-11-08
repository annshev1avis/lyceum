import django.conf
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from feedback.forms import FeedbackForm


__all__ = []


def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST or None)
        if form.is_valid():
            send_mail(
                subject=form.cleaned_data["name"],
                message=form.cleaned_data["text"],
                from_email=django.conf.settings.DJANGO_MAIL,
                recipient_list=[form.cleaned_data["mail"]],
            )

            messages.success(request, "Форма успешно отправлена! :)")
            return redirect(reverse("feedback:feedback"))
    else:
        form = FeedbackForm()

    context = {"title": "Обратная связь", "form": form}

    return render(request, "feedback/feedback.html", context)
