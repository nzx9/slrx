from django.shortcuts import render, HttpResponse
from categories.models import Category
import json
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
