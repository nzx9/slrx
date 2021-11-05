from django.shortcuts import render, HttpResponse, redirect
from categories.models import Category
from words.models import Word
import json
from django.contrib.auth.decorators import login_required
# Create your views here.


def fetchData():
    categories = Category.objects.all().order_by('pk')

    if not categories:
        empty = True
    else:
        empty = False
    return categories, empty


def category_view(request):
    categories, empty = fetchData()
    return render(request, 'category_view.html', {"empty": empty, "categories": categories})


@login_required(login_url='/accounts/login/')
def create_category(request):
    if(request.user.is_superuser or request.user.groups.filter(name='Tester').exists()):
        if request.method == "POST":
            try:
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                name = body['name']
                desc = body['desc']
                category = Category()
                category.name = name
                category.description = desc
                category.created_by = request.user
                category.save()
                return HttpResponse(json.dumps({"msg": "New Category '{}' Created".format(name), "type": "success"}))
            except:
                return HttpResponse(json.dumps({"msg": "Something went wrong", "type": "error"}))
        else:
            return HttpResponse(json.dumps({"msg": "Not a POST request", "type": "error"}))
    return HttpResponse(json.dumps({"msg": "No permission to perfrom action", "type": "error"}))


def category_each_view(request, category):
    if not Category.objects.filter(name=category).exists():
        return render(request, '404.html')
        
    cat_data = Category.objects.get(name=category)

    words = Word.objects.filter(category=cat_data)
    empty = (len(words)) == 0 if True else False
    return render(request, 'category_each.html', {"cat_data": cat_data, "words": words, "empty": empty})


@login_required(login_url='/accounts/login/')
def update_category(request, pk):
    edited = False
    if(request.user.is_superuser or request.user.groups.filter(name='Tester').exists()):
        if request.method == "PUT":
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            name = body['name']
            desc = body['desc']
            try:
                category = Category.objects.get(pk=pk)
                if(category.name != name):
                    category.name = name
                    edited = True
                if(category.description != desc):
                    category.description = desc
                    edited = True
                if(edited):
                    category.last_edit_by = request.user
                    category.save()
                    return HttpResponse(json.dumps({"msg": "Category '{}' Updated".format(name), "type": "success"}))
                else:
                    return HttpResponse(json.dumps({"msg": "Nothing to Update".format(name), "type": "warning"}))
            except:
                return HttpResponse(json.dumps({"msg": "Something went wrong", "type": "error"}))
        else:
            return HttpResponse(json.dumps({"msg": "Not a PUT request", "type": "error"}))
    else:
        return HttpResponse(json.dumps({"msg": "No permission to perfrom action", "type": "error"}))


@login_required(login_url='/accounts/login/')
def delete_category(request, pk):
    if request.user.is_superuser:
        category = Category.objects.get(pk=pk)
        category.delete()
        return redirect('category_view')
    else:
        return render(request, "403.html")
