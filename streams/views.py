from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from firebase_admin import storage
from streams.models import Stream, User_Stream
from django.contrib import messages
from words.models import Word
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
# Create your views here.


@login_required(login_url='/accounts/login/')
def streams_view(request):
    words = Word.objects.all()
    wl = list(words)
    data = []
    c1 = Q(userId=request.user.id)
    for w in wl:
        c2 = Q(wordId=w.pk)
        us = User_Stream.objects.filter(c1 & c2)
        if(us.count() >= 1):
            stream_info = Stream.get(pk=us.steamId)
            data.append({
                "w_info": w,
                "s_info": stream_info,
                "comp": True
            })
        else:
            data.append({
                "w_info": w,
                "s_info": {
                    "userId": request.user.id,
                    "wordId": w.pk,
                    "pos_server": None,
                    "pos_firebase": None,
                    "verified": None,
                    "created_at": None,
                    "updated_at": None
                },
                "comp": False
            })
    return render(request, "streams_home.html", {"data": data})


@login_required(login_url='/accounts/login/')
def streams_rec_view(request, pk):
    curr_word = None
    try:
        curr_word = Word.objects.get(pk=pk)
        print(curr_word.in_sinhala)
    except ObjectDoesNotExist:
        print("Does not found")
    return render(request, "streams.html", {"curr_word": curr_word, "pk": pk})


@login_required(login_url='/accounts/login/')
def sub(request):
    bucket = storage.bucket()
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        serverFileName = './media/' + \
            body_data['word'] + '/' + request.user.id + '.webm'
        fireBaseFileName = './dgr/' + \
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
