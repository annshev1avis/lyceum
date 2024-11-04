from django.http import FileResponse


def download_media_file(request, path):
    return FileResponse(open(f".{path}", "rb"), as_attachment=True)