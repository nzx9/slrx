from django.shortcuts import render
from streams.models import Stream, User_Stream

# Create your views here.


def clusters_view(request):
    uss = User_Stream.objects.all()

    total_count = uss.count()
    verified_count = 0
    for us in uss:
        s = Stream.objects.get(pk=us.streamId.pk)
        if(s.verified == True):
            verified_count += 1

    return render(request, "clusters.html", {"total_count": total_count, "verified_count": verified_count})
