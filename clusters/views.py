from django.shortcuts import render
from django.core.paginator import Paginator
from streams.models import Stream, User_Stream
from django.contrib.auth.decorators import permission_required
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


@permission_required('clusters.can_edit', raise_exception=True)
def cluster_verify(request):
    filter = request.GET.get('filter')
    if(filter == "verified"):
        s = Stream.objects.filter(verified=True).order_by('-pk')
    elif(filter == "not-verified"):
        s = Stream.objects.filter(verified=False).order_by('-pk')
    else:
        s = Stream.objects.all().order_by('-pk')
        filter = "ALL"

    p = Paginator(s, 5)

    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    page_obj = p.get_page(page_number)
    return render(request, "verify_streams.html", {"page_obj": page_obj, "filter": filter, "count": s.count()})
