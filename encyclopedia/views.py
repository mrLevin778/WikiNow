from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import util

class NewPageForm(forms.Form):
    pagetitle = forms.CharField(max_length=50, label="")
    pagecontent = forms.CharField(max_length=9000, label="", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, pagetitle):
    return render(request, "encyclopedia/wiki.html", {
        "page": util.get_entry(pagetitle)
    })

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
