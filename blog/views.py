from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost
def index(request):
    blog = Blogpost.objects.all()
    n = len(blog)
    # catprods = Blogpost.objects.values('category', 'id')
    allblogs = []
    for item in blog:
        allblogs.append(item)
    params = {'item':allblogs}
    return render(request,'blog/index.html',params)


def blogpost(request, myid):
    product = Blogpost.objects.filter(post_id=myid)
    print(product)
    return render(request,"blog/blogpost.html",{'product':product[0]})