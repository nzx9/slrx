import streams
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
import os
# Create your views here.


@login_required(login_url='/accounts/login/')
def streams_view(request):
    words = Word.objects.all().order_by('pk')
    wl = list(words)
    data = []
    # c1 = Q(userId=request.user)
    for w in wl:
        # c2 = Q(wordId=w)
        # c1 and c2
        us = User_Stream.objects.filter(userId=request.user).filter(wordId=w)
        if(us.count() >= 1):
            stream_info = Stream.objects.get(pk=us[0].streamId.pk)
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
    all_count = Word.objects.all().count()
    done_count = User_Stream.objects.filter(userId=request.user.id).count()
    return render(request, "streams_home.html", {"data": data, "all_count": all_count, "done_count": done_count})


@ login_required(login_url='/accounts/login/')
def streams_rec_view(request, e_word):
    curr_stream = None
    try:
        all_words = Word.objects.all()
        curr_word = all_words.get(in_english=e_word)
        prev_word = all_words.filter(pk__lt=curr_word.pk).last()
        next_word = all_words.filter(pk__gt=curr_word.pk).first()
        us = User_Stream.objects.filter(userId=request.user.id)
        done_count = us.count()
        all_count = all_words.count()

        current_us = User_Stream.objects.filter(
            userId=request.user).filter(wordId=curr_word)

        if(current_us.count() > 0):
            curr_stream = Stream.objects.get(pk=us[0].streamId.pk)

    except ObjectDoesNotExist:
        return render(request, "404.html")
    return render(request, "streams_rec.html", {"curr_word": curr_word, "prev_word": prev_word, "next_word": next_word, "e_word": e_word, "done_count": done_count, "all_count": all_count, "curr_stream": curr_stream})


@ login_required(login_url='/accounts/login/')
def submit(request, e_word):
    bucket = storage.bucket()
    if request.method == "POST":
        try:
            body_data = request.body

            word = Word.objects.get(in_english=e_word)

            serverPath = "./media/dgr"
            serverFileName = os.path.join(
                serverPath, "{0}_{1}.webm".format(word.in_sinhala, request.user.id))

            fireBaseFileName = "dgr/{0}/{0}_{1}.mp4".format(
                word.in_sinhala, request.user.id)

            mp4Path = os.path.join(serverPath, "{0}_{1}.mp4".format(
                word.in_sinhala, request.user.id))
            # save file
            f = open(serverFileName, 'wb')
            f.write(body_data)
            f.close()

            os.system(
                "ffmpeg -i {0} {1} -y".format(serverFileName, mp4Path))

            os.system("rm -f {0}".format(serverFileName))
            # upload to firebase
            blob = bucket.blob(fireBaseFileName)
            blob.upload_from_filename(mp4Path)

            stream_exist = Stream.objects.filter(
                userId=request.user).filter(wordId=word)

            if(stream_exist.count() == 0):
                stream = Stream(userId=request.user, wordId=word, pos_server=mp4Path,
                                pos_firebase=fireBaseFileName)
                stream.save()
                us = User_Stream(userId=request.user,
                                 wordId=word, streamId=stream)
                us.save()
                word.recorde_count += 1
                word.save()
                msg = "Success!, File uploaded and updated the DB"
                return HttpResponse(json.dumps(
                    {"title": "success", "msg": msg}), content_type='application/json')
            msg = "Success!, File uploaded to Firebase"
            return HttpResponse(json.dumps(
                {"title": "success", "msg": msg}), content_type='application/json')
        except:
            msg = "Error!, Something went wrong. Can't upload the file"
            return HttpResponse(json.dumps(
                {"title": "error", "msg": msg}), content_type='application/json')
    else:
        msg = "Error!, Request is not a POST request"
        return HttpResponse(json.dumps({"title": "error", "msg": msg}), content_type='application/json')
