from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from words.models import Word
# Create your views here.


@login_required(login_url='/accounts/login/')
def words_view(request):
    words = Word.objects.all()

    if not words:
        empty = True
    else:
        empty = False

    return render(request, "words.html", {'words': words, "empty": empty})


@login_required(login_url='/accounts/login/')
def submit_new_word(request):
    if request.method == "POST":
        newWord = Word()
        newWord.in_sinhala = request.POST['sinhala-word']
        newWord.in_english = request.POST['english-word']
        newWord.in_singlish = request.POST['singlish-word']
        newWord.created_by = request.user.id
        newWord.save()
        return HttpResponse('File updated successfully')
    else:
        return HttpResponse("Not a post request")
