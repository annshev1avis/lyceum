from django.contrib import admin

import feedback.models


__all__ = []


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = [
        "name",
        "text",
        "created_on",
        "mail",
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            return

        status_from = feedback.models.Feedback.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        log = feedback.models.StatusLog(
            user=request.user,
            status_from=status_from,
            status_to=obj.status,
        )
        log.save()
