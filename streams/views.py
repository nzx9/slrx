from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from firebase_admin import storage
from streams.models import Stream, User_Stream
from words.models import Word
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import os
from django.core.paginator import Paginator
from .templatetags import encoders
import time
from django.contrib.auth.models import User

# Create your views here.


@login_required(login_url="/accounts/login/")
def streams_view(request):
    words = Word.objects.all().order_by("pk")
    wl = list(words)
    data = []
    # c1 = Q(userId=request.user)
    for w in wl:
        # c2 = Q(wordId=w)
        # c1 and c2
        us = User_Stream.objects.filter(userId=request.user).filter(wordId=w)
        if us.count() >= 1:
            stream_info = Stream.objects.get(pk=us[0].streamId.pk)
            data.append({"w_info": w, "s_info": stream_info, "comp": True})
        else:
            data.append(
                {
                    "w_info": w,
                    "s_info": {
                        "userId": request.user.id,
                        "wordId": w.pk,
                        "pos_server": None,
                        "pos_firebase": None,
                        "verified": None,
                        "comment": None,
                        "reason": None,
                        "created_at": None,
                        "updated_at": None,
                    },
                    "comp": False,
                }
            )
    all_count = Word.objects.all().count()
    done_count = User_Stream.objects.filter(userId=request.user.id).count()
    return render(
        request,
        "streams_home.html",
        {"data": data, "all_count": all_count, "done_count": done_count},
    )


@login_required(login_url="/accounts/login/")
def streams_rec_view(request, pk):
    curr_stream = None
    try:
        all_words = Word.objects.all()
        curr_word = all_words.get(pk=pk)
        prev_word = all_words.filter(pk__lt=curr_word.pk).last()
        next_word = all_words.filter(pk__gt=curr_word.pk).first()
        us = User_Stream.objects.filter(userId=request.user.id)
        done_count = us.count()
        all_count = all_words.count()

        current_us = User_Stream.objects.filter(userId=request.user).filter(
            wordId=curr_word
        )

        if current_us.count() > 0:
            curr_stream = Stream.objects.get(pk=current_us[0].streamId.pk)

    except ObjectDoesNotExist:
        return render(request, "404.html")
    return render(
        request,
        "streams_rec.html",
        {
            "curr_word": curr_word,
            "prev_word": prev_word,
            "next_word": next_word,
            "e_word": curr_word.in_english,
            "done_count": done_count,
            "all_count": all_count,
            "curr_stream": curr_stream,
        },
    )


@login_required(login_url="/accounts/login/")
def streams_table_home(request):
    words = Word.objects.all().order_by("pk")
    wl = list(words)
    data = []
    # c1 = Q(userId=request.user)
    for w in wl:
        # c2 = Q(wordId=w)
        # c1 and c2
        us = User_Stream.objects.filter(userId=request.user).filter(wordId=w)
        if us.count() >= 1:
            stream_info = Stream.objects.get(pk=us[0].streamId.pk)
            data.append({"w_info": w, "s_info": stream_info, "comp": True})
        else:
            data.append(
                {
                    "w_info": w,
                    "s_info": {
                        "userId": request.user.id,
                        "wordId": w.pk,
                        "pos_server": None,
                        "pos_firebase": None,
                        "verified": None,
                        "comment": None,
                        "reason": None,
                        "created_at": None,
                        "updated_at": None,
                    },
                    "comp": False,
                }
            )
    all_count = Word.objects.all().count()
    done_count = User_Stream.objects.filter(userId=request.user.id).count()
    return render(
        request,
        "streams_table_home.html",
        {"data": data, "all_count": all_count, "done_count": done_count},
    )


@login_required(login_url="/accounts/login/")
def submit(request, pk):
    bucket = storage.bucket()
    if request.method == "POST":
        try:
            body_data = request.body

            word = Word.objects.get(pk=pk)

            serverPath = "./media/dgr"
            serverFileName = os.path.join(
                serverPath, "{0}_{1}.webm".format(word.in_sinhala, request.user.id)
            )

            fireBaseFileName = "dgr/{0}/{0}_{1}.mp4".format(
                word.in_sinhala, request.user.id
            )

            mp4Path = os.path.join(
                serverPath, "{0}_{1}.mp4".format(word.in_sinhala, request.user.id)
            )
            # save file
            f = open(serverFileName, "wb")
            f.write(body_data)
            f.close()

            os.system("ffmpeg -i {0} {1} -y".format(serverFileName, mp4Path))

            os.system("rm -f {0}".format(serverFileName))

            stream_exist = Stream.objects.filter(userId=request.user).filter(
                wordId=word
            )

            if stream_exist.count() == 0:
                # upload to firebase
                blob = bucket.blob(fireBaseFileName)
                blob.upload_from_filename(mp4Path)

                stream = Stream(
                    userId=request.user,
                    wordId=word,
                    pos_server=mp4Path,
                    pos_firebase=fireBaseFileName,
                )
                stream.save()
                us = User_Stream(userId=request.user, wordId=word, streamId=stream)
                us.save()
                word.recorde_count += 1
                word.save()
                msg = "Success!, File uploaded and updated the DB"
                return HttpResponse(
                    json.dumps({"title": "success", "msg": msg}),
                    content_type="application/json",
                )
            else:
                stream = stream_exist[0]
                stream.verified = None
                stream.verified_by = None
                stream.reason = None
                stream.comment = "NEW"
                stream.save()
                msg = "Success!, New Recording uploaded and updated the DB"

                source_blob = bucket.blob(stream.pos_firebase)
                new_location = "archive/{0}/{1}_{2}.mp4".format(
                    request.user.pk, stream.wordId.in_sinhala, time.time()
                )
                bucket.copy_blob(source_blob, bucket, new_location)
                bucket.delete_blob(stream.pos_firebase)

                # upload to firebase
                blob = bucket.blob(fireBaseFileName)
                blob.upload_from_filename(mp4Path)

                return HttpResponse(
                    json.dumps({"title": "success", "msg": msg}),
                    content_type="application/json",
                )
        except:
            msg = "Error!, Something went wrong. Can't upload the file"
            return HttpResponse(
                json.dumps({"title": "error", "msg": msg}),
                content_type="application/json",
            )
    else:
        msg = "Error!, Request is not a POST request"
        return HttpResponse(
            json.dumps({"title": "error", "msg": msg}), content_type="application/json"
        )


def streams_verification(request):
    if (
        request.user.is_superuser
        or request.user.groups.filter(name="Validator").exists()
    ):
        filter = request.GET.get("filter")
        if filter == "verified":
            s = Stream.objects.all().exclude(verified=None).order_by("-pk")
        elif filter == "verified:accepted":
            s = Stream.objects.filter(verified=True).order_by("-pk")
        elif filter == "verified:rejected":
            s = Stream.objects.filter(verified=False).order_by("-pk")
        elif filter == "not-verified":
            s = Stream.objects.filter(verified=None).order_by("-pk")
        else:
            s = Stream.objects.all().order_by("-pk")
            filter = "ALL"

        p = Paginator(s, 5)

        page_number = request.GET.get("page")
        if page_number == None:
            page_number = 1
        page_obj = p.get_page(page_number)
        return render(
            request,
            "streams_verification.html",
            {"page_obj": page_obj, "filter": filter, "count": s.count()},
        )
    else:
        return render(request, "403.html")


def get_stream(request, pk):
    if (
        request.user.is_superuser
        or request.user.groups.filter(name="Validator").exists()
    ):
        try:
            stream = Stream.objects.get(pk=pk)
            resp = json.dumps(
                {
                    "success": True,
                    "msg": None,
                    "data": {
                        "pk": stream.pk,
                        "user": {
                            "pk": stream.userId.pk,
                            "name": stream.userId.username,
                        },
                        "word": {
                            "pk": stream.wordId.pk,
                            "sin": stream.wordId.in_sinhala
                            if stream.wordId.in_sinhala != None
                            else None,
                            "eng": stream.wordId.in_english
                            if stream.wordId.in_english != None
                            else None,
                            "sie": stream.wordId.in_singlish
                            if stream.wordId.in_singlish != None
                            else None,
                        },
                        "src": "https://firebasestorage.googleapis.com/v0/b/slrx-pro.appspot.com/o/{}?alt=media&".format(
                            encoders.uriencode(stream.pos_firebase)
                        ),
                        "verification": {
                            "verified": stream.verified,
                            "verified_by": {
                                "pk": stream.verified_by.pk
                                if stream.verified_by != None
                                else None,
                                "name": stream.verified_by.username
                                if stream.verified_by != None
                                else None,
                            },
                            "reason": stream.reason,
                        },
                        "comment": stream.comment,
                        "ts": {
                            "created": str(stream.created_at),
                            "updated": str(stream.updated_at),
                        },
                    },
                }
            )
            return HttpResponse(resp, content_type="application/json")
        except ObjectDoesNotExist:
            resp = json.dumps(
                {"success": False, "msg": "Stream Not Found", "data": None}
            )
            return HttpResponse(resp, content_type="application/json")
    else:
        resp = json.dumps({"success": False, "msg": "Forbidden", "data": None})
        return HttpResponse(resp, content_type="application/json")


def verify_stream(request, pk):
    if (
        request.user.is_superuser
        or request.user.groups.filter(name="Validator").exists()
    ):
        try:
            stream = Stream.objects.get(pk=pk)
            body_data = json.loads(request.body)
            if body_data["verify"] == "accepted":
                stream.verified = True
                stream.reason = None
            elif body_data["verify"] == "rejected":
                if body_data["reason"] == None:
                    return HttpResponse(
                        json.dumps({"success": False, "msg": "Reason is required"}),
                        content_type="application/json",
                    )
                else:
                    stream.verified = False
                    stream.reason = body_data["reason"]
            else:
                return HttpResponse(
                    json.dumps({"success": False, "msg": "Verify status is required"}),
                    content_type="application/json",
                )

            stream.comment = (
                None if body_data["comment"] == "" else body_data["comment"]
            )
            stream.verified_by = request.user
            stream.save()
            resp = json.dumps({"success": True, "msg": "Updated Successfully"})
        except:
            resp = json.dumps({"success": False, "msg": "Stream not found"})
            return HttpResponse(resp, content_type="application/json")
    else:
        resp = json.dumps(
            {
                "success": False,
                "msg": "No Permission to perform action",
            }
        )
    return HttpResponse(resp, content_type="application/json")


def streams_from_users(request, pk):
    if (
        request.user.is_superuser
        or request.user.groups.filter(name="Validator").exists()
    ):
        user_id = request.GET.get("user_id")
        if user_id == None:
            return HttpResponse(
                json.dumps({"success": False, "msg": "User ID is required"}),
                content_type="application/json",
            )

        user = User.objects.get(pk=user_id)
        user_stream_data = Stream.objects.filter(userId=user).order_by("-pk")

        p = Paginator(user_stream_data, 10)

        page_number = request.GET.get("page")
        if page_number == None:
            page_number = 1
        page_obj = p.get_page(page_number)
        return render(
            request,
            "streams_from_users.html",
            {"page_obj": page_obj, "filter": filter, "count": user_stream_data.count()},
        )
    else:
        return render(request, "403.html")
