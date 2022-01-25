from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import markdown2

from . import util


class NewPageForm(forms.Form):
    pagetitle = forms.CharField(max_length=50, label="Article name: ")
    pagecontent = forms.CharField(max_length=9000, label="Article content: ", widget=forms.Textarea)


def search_page(request):
    if request.method == "GET":
        query = request.GET.get("query")
        lst_entr = util.list_entries()
        matches = []
        for i in lst_entr:
            if query in i.lower() or query in i:
                matches.append(i)
                return render(request, "encyclopedia/index.html", {
                    "tab_title": "Search",
                    "title": "Matches for " + query,
                    "entries": matches
                })
        else:
            return render(request, "encyclopedia/wiki.html", {
                "title": query,
                "article": "Article with name " + query + " is not exist!"
            })


def index(request):
    return render(request, "encyclopedia/index.html", {
        "tab_title": "Encyclopedia",
        "title": "All pages",
        "entries": util.list_entries()
    })


def article(request, title):
    return render(request, "encyclopedia/wiki.html", {
        "article": markdown2.markdown(util.get_entry(title)),
        "title": title
    })


def randompage(request):
    lenght = len(util.list_entries())
    r_entry, title = util.random_entry(lenght)
    return render(request, "encyclopedia/wiki.html", {
        "article": r_entry,
        "title": title
    })


def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["pagetitle"]
            content = form.cleaned_data["pagecontent"]
            for a in util.list_entries():
                if a == title:
                    return render(request, "encyclopedia/create.html", {
                        "form": form
                    })
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
