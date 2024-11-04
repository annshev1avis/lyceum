from django.http import FileResponse


__all__ = []


def download_media_file(request, path):
    return FileResponse(open(f".{path}", "rb"), as_attachment=True)
