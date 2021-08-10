from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, HttpResponse, reverse
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
def streams_rec_view(request, e_word):
    try:
        all_words = Word.objects.all()
        curr_word = all_words.get(in_english=e_word)
        prev_word = all_words.filter(pk__lt=curr_word.pk).last()
        next_word = all_words.filter(pk__gt=curr_word.pk).first()
    except ObjectDoesNotExist:
        return render(request, "404.html")
    return render(request, "streams_rec.html", {"curr_word": curr_word, "prev_word": prev_word, "next_word": next_word, "e_word": e_word})


@login_required(login_url='/accounts/login/')
def submit(request, e_word):
    # bucket = storage.bucket()
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        print(body_data['nextWord'])
        # serverFileName = './media/' + \
        #     body_data['word'] + '/' + request.user.id + '.webm'
        # fireBaseFileName = './dgr/' + \
        #     body_data['word'] + '/' + request.user.id + '.webm'
        # f = open(serverFileName, 'wb')
        # f.write(body_data['blob'])
        # f.close()

        # blob = bucket.blob(serverFileName)
        # success = blob.upload_from_filename(fireBaseFileName)
        # print(success)  # remove
        # stream = Stream(userId=request.user.id, wordId=body_data['wordId'], pos_server=serverFileName,
        #                 pos_firebase=fireBaseFileName)
        # stream.save()
        # print(body_data['nextWord'])
        # reverse('streams_rec_view', args=[body_data['nextWord']])
        return HttpResponse(body_data['nextWord'])
    else:
        return HttpResponse("Not a post request")
