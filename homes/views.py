from django.shortcuts import render
from streams.models import Stream, User_Stream
from words.models import Word

# Create your views here.


def home_view(request):
    if request.user.is_authenticated:
        word_count = Word.objects.all().count()
        uss = User_Stream.objects.filter(userId=request.user)

        accept_count = 0
        reject_count = 0
        to_verify_count = 0

        for us in uss:
            if us.streamId.verified == True:
                accept_count += 1
            elif us.streamId.verified == False:
                reject_count += 1
            else:
                to_verify_count += 1

        done_count = uss.count() - reject_count
        not_done_count = word_count - done_count

        if word_count > 0:
            percent = int((accept_count / word_count) * 100)
        else:
            percent = 0
        return render(
            request,
            "home.html",
            {
                "done_count": done_count,
                "not_done_count": not_done_count,
                "percent": percent,
                "accept_count": accept_count,
                "reject_count": reject_count,
                "to_verify_count": to_verify_count,
            },
        )
    else:
        return render(request, "home.html")


def terms_view(request):
    return render(request, "terms.html")
