from django.contrib import admin

import feedback.models


__all__ = []


class FeedbackAuthorInline(admin.TabularInline):
    model = feedback.models.FeedbackAuthor
    fields = [
        "name",
        "mail",
    ]
    can_delete = False


class FeedbackFilesInline(admin.TabularInline):
    model = feedback.models.FeedbackFile
    fields = ["file"]


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [
        "text",
        "status",
    ]
    inlines = [
        FeedbackAuthorInline,
        FeedbackFilesInline,
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
