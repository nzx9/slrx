from django.contrib.messages.api import success
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


@login_required(login_url='/accounts/login/')
def bulk_upload(request):
    if request.method == "POST":
        # form = UploadFileForm(request.POST, request.FILES)
        # request.POST[]
        byte_file = b''
        for chunk in request.FILES.get('bulk-file').chunks():
            byte_file += chunk
        word_file = byte_file.decode('utf-8')
        words_splited = word_file.split('\n')
        word_list = []
        for word in words_splited:
            x = word.split(",")
            if len(x) == 3 and len(x[0].strip()) > 0 and len(x[1].strip()) > 0 and len(x[2].strip()) > 0:
                word_list.append(
                    (x[0].strip().lower(), x[1].strip().lower(), x[2].strip().lower()))
            elif len(x) == 2 and len(x[0].strip()) > 0 and len(x[1].strip()) > 0:
                word_list.append(
                    (x[0].strip().lower(), x[1].strip().lower(), None))
            elif len(x) == 1 and len(x[0].strip()) > 0:
                word_list.append((x[0].strip().lower(), None, None))
            else:
                continue

        file_name = request.FILES.get('bulk-file').name
        titles = word_list[0]

        lang_checked = [0, 0, 0]

        error = False
        error_msg = None
        success = False  # TODO
        success_msg = None  # TODO

        for i in range(3):
            if titles[i] != None:
                if titles[i] == "sinhala":
                    lang_checked[0] += 1
                elif titles[i] == "english":
                    lang_checked[1] += 1
                elif titles[i] == "singlish":
                    lang_checked[2] += 1
                else:
                    error = True
                    error_msg = "'{0}' cann't recognized in {1}. First line of the {1} can only have comma seperated 'sinhala', 'english' or singlish only (CASE DOESN'T MATTER)".format(
                        titles[i], file_name)
            else:
                error = True
                error_msg = "First line of the {0} can only have comma seperated 'sinhala', 'english' or singlish only (CASE DOESN'T MATTER). 'NULL' Provided".format(
                    file_name)
        if lang_checked[0] != 1 or lang_checked[1] != 1 or lang_checked[2] != 1:
            error = True
            error_msg = "First line of the {0} can only have comma seperated 'sinhala', 'english' or singlish only (CASE DOESN'T MATTER). ONE OR MORE LANGUAGES ARE MISSING and ONE USED MORE THAN ONCE".format(
                file_name)

    return render(request, "word_bulk_upload.html", {'file_name': file_name, 'titles': titles, 'word_list': word_list[1:], 'error': error, 'error_msg': error_msg})
