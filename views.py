import random
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
from markdown2 import Markdown

markdowner = Markdown()


class SearchForm(forms.Form):
    item = forms.CharField(label="",
                           widget=forms.TextInput(attrs={'placeholder': 'Wiki title',
                                                         'style': 'width:100%'}))

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class EditEntryForm(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')

def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries: 
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdowner.convert(page)
                    return render(request, "encyclopedia/entry.html", {"page": page_converted, "title": item, "form": SearchForm()})
                if item.lower() in i.lower():
                    searched.append(i)
            return render(request, "encyclopedia/search.html", {"searched": searched, "form": SearchForm()})

        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form": SearchForm()
            })

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdowner.convert(page)
        return render(request, "encyclopedia/entry.html", {"page": page_converted, "title": title, "form": SearchForm()})
    else:
        return render(request, "encyclopedia/error.html", {"form": SearchForm(), "error": "Entry not found, please try again." })

def create(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {"form": SearchForm(), "error": "Entry in use"})
            else:
                util.save_entry(title, textarea)
                page = util.get_entry(title)
                page_converted = markdowner.convert(page)
                return render(request, "encyclopledia/entry.html", {"form": SearchForm(), "page": page_converted, "title": title})
    else:
        return render(request, "encyclopedia/create.html", {"form": SearchForm(), "NewEntryForm": NewEntryForm()})


def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"form": SearchForm(), "EditEntryForm": EditEntryForm(initial={'textarea': page}), 'title': title})
    else:
        form = EditEntryForm(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title, textarea)
            page = util.get_entry(title)
            page_converted = markdowner.convert(page)
            return render(request, "encyclopedia/entry.html", {"form": SearchForm(), "page": page_converted, "title": title})

def randomPage(request):
    if request.method == 'GET':
        entries = util.list_entries()
        num = random.randint(0, len(entries) - 1)
        page_random = entries[num]
        page = util.get_entry(page_random)
        page_converted = markdowner.convert(page)

        return render(request, "encyclopedia/entry.html", {"form": SearchForm(), "page": page_converted, "title": page_random})