from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import util

class NewPageTitleForm(forms.Form):
    pagetitle = forms.CharField(max_length=50, label="")

class NewPageContentForm(forms.Form):
    pagecontent = forms.CharField(max_length=9000, label="", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, pagetitle):
    return render(request, "encyclopedia/wiki.html", {
        "page": util.get_entry(pagetitle)
    })

def create(request):
    if request.method == "POST":
        formtitle = NewPageTitleForm(request.POST)
        formcontent = NewPageContentForm(request.POST)
        if formtitle.is_valid() and formcontent.is_valid():
            title = formtitle.cleaned_data["pagetitle"]
            content = formcontent.cleaned_data["pagecontent"]
            return HttpResponseRedirect(reverse("encyclopedia:index"), {
                "save": util.save_entry(title, content)
            })
        else:
            return render(request, "encyclopedia/create.html", {
                "formtitle": formtitle,
                "formcontent": formcontent
            })
    return render(request, "encyclopedia/create.html", {
        "title": NewPageTitleForm(),
        "content": NewPageContentForm()
    })
