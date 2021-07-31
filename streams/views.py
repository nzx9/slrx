from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from streams.forms import StreamUploadForm
from firebase_admin import storage

# Create your views here.


@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, "index.html")


def uploadStreams(request):
    if request.method == "POST":
        form = StreamUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Uploaded")
    else:
        form = StreamUploadForm()
        contex = {
            'form': form
        }
    return render(request, "index.html", contex)


def sub(request):
    bucket = storage.bucket()
    if request.method == "POST":
        print(request.body)
        f = open('./media/file.webm', 'wb')
        f.write(request.body)
        f.close()
        destination_blob_name = "new/first_upload.webm"
        source_file_name = "./media/file.webm"
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )
        return HttpResponse('audio received')
    else:
        print("not post")
