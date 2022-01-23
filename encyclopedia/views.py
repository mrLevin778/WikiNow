from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from . import util


class NewPageForm(forms.Form):
    pagetitle = forms.CharField(max_length=50, label="Article name: ")
    pagecontent = forms.CharField(max_length=9000, label="Article content: ", widget=forms.Textarea)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, label="Search Encyclopedia")


def search_page(request):
    if request.method == "POST":
        searchform = SearchForm(request.POST)
        if searchform.is_valid():
            title = searchform.cleaned_data["search"]
            return HttpResponseRedirect("encyclopedia/wiki.html", {
                "article": util.get_entry(title)
            })
        else:
            return HttpResponse("Not Found!")
    return render(request, "encyclopedia/create.html", {
        "searchform": SearchForm(),
    })


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()

    })


def article(request, title):
    return render(request, "encyclopedia/wiki.html", {
        "article": util.get_entry(title),
        "title": title
    })


def randompage(request):

    return render(request, "encyclopedia/wiki.html")


def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["pagetitle"]
            content = form.cleaned_data["pagecontent"]
            return HttpResponseRedirect(reverse("encyclopedia:index"), {
                "save": util.save_entry(title, content)
            })
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": NewPageForm(),
    })
