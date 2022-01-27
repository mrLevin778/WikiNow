from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
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
        while len(lst_entr) != 0:
            for i in lst_entr:
                if query == i or query == i.lower():
                    return render(request, "encyclopedia/wiki.html", {
                        "title": query,
                        "article": markdown2.markdown(util.get_entry(i))
                    })
                if query in i.lower() or query in i:
                    matches.append(i)
                    lst_entr.remove(i)
                    for a in lst_entr:
                        if a not in matches and query in a.lower():
                            matches.append(a)
                    print(matches)
                    print(lst_entr)
                    print(i)
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
    print(util.list_entries())
    return render(request, "encyclopedia/index.html", {
        "tab_title": "Encyclopedia",
        "title": "All pages",
        "entries": util.list_entries(),
        "wiki_path": "wiki/"
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
