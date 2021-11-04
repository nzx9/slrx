from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from words.models import Word
from django.contrib import messages
import json
from categories.models import Category
from streams.models import Stream
from django.db.models import Q
# Create your views here.


def words_view(request):
    query_category = request.GET.get('category')
    query_search = request.GET.get('search')
    words = []
    categories = Category.objects.all().order_by('pk')

    category_exist = Category.objects.filter(name=query_category).exists()

    if(query_category != None and query_search == None):
        if category_exist:
            category = Category.objects.get(name=query_category)
            words = Word.objects.filter(category=category).order_by('pk')
        else:
            words = []

    elif(query_search != None and query_category == None):
        words = Word.objects.filter(
            Q(in_sinhala__icontains=query_search) |
            Q(in_english__icontains=query_search) |
            Q(in_singlish__icontains=query_search) |
            Q(category__name__icontains=query_search)
        ).order_by('pk')

    elif (query_search != None and query_category != None):
        if category_exist:
            category = Category.objects.get(name=query_category)
            words = Word.objects.filter(category=category).filter(
                Q(in_sinhala__contains=query_search) |
                Q(in_english__contains=query_search) |
                Q(in_singlish__contains=query_search)).order_by('pk')
        else:
            words = []
    else:
        words = Word.objects.all().order_by('pk')

    if len(words) == 0:
        empty = True
    else:
        empty = False
    return render(request, "words.html", {"words": words, "empty": empty, "categories": categories})


@ login_required(login_url='/accounts/login/')
def add_new_words(request):
    if(request.user.is_superuser or request.user.groups.filter(name='Tester').exists()):
        if request.method == "POST":
            si = request.POST['sinhala-word']
            en = request.POST['english-word']
            se = request.POST['singlish-word']
            cat_pk = request.POST['category']
            cat = None
            try:
                cat_pk = int(cat_pk)
            except:
                pass

            if type(cat_pk) == int:
                cat = Category.objects.get(pk=cat_pk)
            if(cat == None):
                messages.warning(request, "Category set to NULL")

            if si != None and en != None and se != None:
                newWord = Word()
                newWord.in_sinhala = si
                newWord.in_english = en
                newWord.in_singlish = se
                newWord.category = cat
                newWord.created_by = request.user
                try:
                    newWord.save()
                    messages.success(request, "New Word Created")
                except Exception as e:
                    messages.error(request, f"Something went wrong: {str(e)}")
            else:
                messages.error(request, "NULL Values Provided")
        return redirect("words_view")
    else:
        return render(request, "403.html")


@ login_required(login_url='/accounts/login/')
@ permission_required('word.can_change', raise_exception=True)
def bulk_upload(request):
    file_name = None
    titles = None
    word_list = []
    error = True
    error_msg = "Not A POST Request"
    word_json = None

    if request.method == "POST":
        file_name = request.FILES.get('bulk-file').name
        byte_file = b''
        for chunk in request.FILES.get('bulk-file').chunks():
            byte_file += chunk
        word_file = byte_file.decode('utf-8')
        words_splited = word_file.split('\n')

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

        titles = word_list[0]

        word_dict = {}
        count = 0
        for word in word_list[1:]:
            word_dict[count] = {titles[0]: word[0],
                                titles[1]: word[1], titles[2]: word[2]}
            count += 1

        word_json = json.dumps(word_dict)
        lang_checked = [0, 0, 0]

        error = False
        error_msg = None

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
    return render(request, "word_bulk_upload.html", {'file_name': file_name, 'titles': titles, 'word_list': word_list[1:], 'error': error, 'error_msg': error_msg, "word_json": word_json})


@ login_required(login_url='/accounts/login/')
@ permission_required('word.can_change', raise_exception=True)
def add_bulk_words_to_db(request):
    title = "METHOD not recognized..."
    msg = ""
    if(request.method == "POST"):
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            for e in body_data:
                if body_data[e]["sinhala"] != None and body_data[e]["sinhala"].strip() != "" and body_data[e]["english"] != None and body_data[e]["english"].strip() != "":
                    newWord = Word()
                    newWord.in_sinhala = body_data[e]["sinhala"].strip(
                    ).lower()
                    newWord.in_english = body_data[e]["english"].strip(
                    ).lower()
                    newWord.in_singlish = body_data[e]["singlish"].strip(
                    ).lower()
                    newWord.created_by = request.user.id
                    try:
                        newWord.save()
                        title = "All done..."
                        msg += "<p><i class='check circle green icon'></i>'({0},{1})' added to the database </p>".format(body_data[e]["sinhala"].strip(
                        ).lower(), body_data[e]["english"].strip(
                        ).lower())
                    except Exception as e:
                        title = "Completed with errors..."
                        msg += "<p><i class='times circle red icon'></i> {}</p>".format(
                            str(e))
                else:
                    title = "Completed with errors..."
                    msg += "<p><i class='times circle red icon'></i> '({},{})' sinhala or english field recived the 'None', sinhala and english fields can't be NULL</p>".format(
                        body_data[e]["sinhala"], body_data[e]["english"])
        except:
            title = "Not valid JSON..."
            msg += "<p><i class='times circle red icon'></i> JSON can't parse recived data</p>"
    else:
        msg += "<p><i class='times circle red icon'></i> Only POST requests are accepted</p>"
    return HttpResponse(json.dumps({"title": title, "msg": msg}), content_type='application/json')


def detailed_word_view(request, word_pk):
    word_exists = Word.objects.filter(pk=word_pk).exists()
    if not word_exists:
        return render(request, "404.html")

    word = Word.objects.get(pk=word_pk)
    categories = Category.objects.all().order_by('pk')
    streams = Stream.objects.filter(wordId=word).order_by('pk')
    empty = True if len(streams) == 0 else False
    return render(request, "detailed_view.html", {"word": word, "categories": categories, "streams": streams, "empty": empty})


@login_required(login_url='/accounts/login/')
def update_word(request, pk):
    edited = False
    cat_ok = False
    if(request.user.is_superuser or request.user.groups.filter(name='Tester').exists()):
        if request.method == "UPDATE":
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            si = body['si']
            en = body['en']
            se = body['se']
            category = body['category']
            try:
                word = Word.objects.get(pk=pk)
                if(category != None and Category.objects.filter(pk=category).exists()):
                    category = Category.objects.get(pk=category)
                    cat_ok = True
                if(word.in_sinhala != si):
                    word.in_sinhala = si
                    edited = True
                if(word.in_english != en):
                    word.in_english = en
                    edited = True
                if(word.in_singlish != se):
                    word.in_singlish = se
                    edited = True
                if(cat_ok and word.category != category):
                    word.category = category
                    edited = True
                elif(category == None and word.category != None):
                    word.category = None
                    edited = True
                if(edited):
                    word.last_edit_by = request.user
                    word.save()
                    return HttpResponse(json.dumps({"msg": "Word '{} ({})' Updated".format(si, en), "type": "success"}))
                else:
                    return HttpResponse(json.dumps({"msg": "Nothing to Update in {} ({}) word".format(si, en), "type": "warning"}))
            except:
                return HttpResponse(json.dumps({"msg": "Something went wrong", "type": "error"}))
        else:
            return HttpResponse(json.dumps({"msg": "Not a POST request", "type": "error"}))
    else:
        return HttpResponse(json.dumps({"msg": "No permission to perfrom action", "type": "error"}))


@login_required(login_url='/accounts/login/')
def delete_word(request, pk):
    if request.user.is_superuser:
        if(Word.objects.filter(pk=pk).exists()):
            word = Word.objects.get(pk=pk)
            word.delete()
        return redirect('words_view')
    else:
        return render(request, "403.html")
