from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from streams.camera import WebCam

# Create your views here.


def home(request):
    return render(request, "index.html")


def frames(camera):
    while True:
        frame = camera.capture()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def videoFeed(request):
    return StreamingHttpResponse(frames(WebCam()), content_type='multipart/x-mixed-replace; boundary=frame')
