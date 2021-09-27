from django.http.response import HttpResponse
from django.shortcuts import render
from streams.models import Stream, User_Stream
from firebase_admin import storage
from pathlib import Path
from datetime import datetime
import shutil
import mimetypes
from zipfile import ZipFile


def clusters_view(request):
    uss = User_Stream.objects.all()

    total_count = uss.count()
    verified_count = 0
    for us in uss:
        s = Stream.objects.get(pk=us.streamId.pk)
        if(s.verified == True):
            verified_count += 1

    return render(request, "clusters.html", {"total_count": total_count, "verified_count": verified_count})


def download_blob(source_blob_name, destination_file_name):
    bucket = storage.bucket()
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(
        "Downloaded storage object {} to local file {}.".format(
            source_blob_name, destination_file_name
        )
    )


def download_clusters(request, type):
    if(type == "verified"):
        streams = Stream.objects.filter(verified=True).order_by('-pk')
        tail = "verified"
    else:
        streams = Stream.objects.all().order_by('-pk')
        tail = "all"

    dt = datetime.now()
    file_name = "dslsl_dataset-v{}-{}".format(dt, tail)
    dir_name = "./media/tmp/{}".format(file_name)
    for s in streams:
        splited = s.pos_firebase.split("/")
        p = '{}/{}'.format(dir_name, splited[1])
        # wsconsumer.send_info()
        Path(p).mkdir(parents=True, exist_ok=True)
        download_blob(s.pos_firebase, "{}/{}".format(p, splited[2]))
    shutil.make_archive(
        "./media/archives/{}".format(file_name), 'zip', root_dir="./media/tmp", base_dir=file_name)
    zippath = "./media/archives/{}.zip".format(file_name)
    # Open the file for reading content
    with open(zippath, 'rb') as zip:
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(zippath)
        # Set the return value of the HttpResponse
        response = HttpResponse(zip, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s.zip" % file_name
        # Return the response value
        return response
