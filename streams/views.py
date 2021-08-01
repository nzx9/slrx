from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from firebase_admin import storage
from streams.models import Stream
import json
from django.contrib import messages
# Create your views here.


@login_required(login_url='/accounts/login/')
def streams_view(request):
    return render(request, "streams.html")


@login_required(login_url='/accounts/login/')
def sub(request):
    bucket = storage.bucket()
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        serverFileName = './media/' + \
            body_data['word'] + '/' + request.user.id + '.webm'
        fireBaseFileName = './dgr/' + + \
            body_data['word'] + '/' + request.user.id + '.webm'
        f = open(serverFileName, 'wb')
        f.write(body_data['blob'])
        f.close()

        blob = bucket.blob(serverFileName)
        success = blob.upload_from_filename(fireBaseFileName)
        print(success)  # remove
        stream = Stream(userId=request.user.id, wordId=body_data['wordId'], pos_server=serverFileName,
                        pos_firebase=fireBaseFileName)
        stream.save()
        messages.success(request, "Please login to access to the site")
        return HttpResponse('File updated successfully')
    else:
        return HttpResponse("Not a post request")
