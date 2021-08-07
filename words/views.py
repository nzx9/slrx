from django.db.models.query_utils import PathInfo
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from words.models import Word
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


@login_required(login_url='/accounts/login/')
def words_view(request):
    words = Word.objects.all()
    # user = User.objects.get(pk=words.create)
    wl = list(words)
    for w in wl:
        username = User.objects.get(pk=w.created_by)
        w.created_by = username

    if not words:
        empty = True
    else:
        empty = False

    return render(request, "words.html", {'words': words, "empty": empty})


@login_required(login_url='/accounts/login/')
def add_new_words(request):
    if request.method == "POST":
        newWord = Word()
        newWord.in_sinhala = request.POST['sinhala-word']
        newWord.in_english = request.POST['english-word']
        newWord.in_singlish = request.POST['singlish-word']
        newWord.created_by = request.user.id
        try:
            newWord.save()
            messages.success(request, "New Word Created")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
    return render(request, "add_words.html")


@login_required(login_url='/accounts/login/')
def delete_word(request, pk):
    word = Word.objects.get(id=pk)
    word.delete()
    return redirect('words_view')
