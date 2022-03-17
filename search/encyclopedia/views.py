from django.shortcuts import render
import markdown2
from django import forms
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random

from . import util

# Form class for creating of a new article
class NewArtForm(forms.Form):
    art_title = forms.CharField(label='Article title:', widget=forms.TextInput(attrs={"class":"ArtTitleInp"}))
    art_body = forms.CharField(label='Article body:', widget=forms.Textarea(attrs={"class":"ArtBodyInp"}))


def orig_cap(entry_name):
    """
    Restore entry_name original capitalization
    """
    entries = util.list_entries()
    for i in range(len(entries)):
        if entry_name.lower() == entries[i].lower():
            return entries[i]

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    content = util.get_entry(entry_name)
    if not content == None: # Entry found
        # Convert from MD to HTML
        # contentHttp = markdown2.markdown(content) # Lib func
        contentHttp = util.md2html(content) # My func
        # Restore entry_name original capitalization
        entry_name = orig_cap(entry_name)
        # Render
        return render(request, "encyclopedia/entry.html",{
            "entry": entry_name,
            "content": contentHttp
        })
    else:
        # Entry not found
        return render(request, "encyclopedia/entry404.html", {
            "entry": entry_name.capitalize()
        })


def search(request):
    q = str(request.GET.get('q')).lower()
    entries = util.list_entries()
    for i in range(len(entries)): # Convert all enties names to lowercase
        entries[i] = entries[i].lower()

    if q in entries:
        # On exact match - open an entry page
        return HttpResponseRedirect(reverse('entry' , args=(q,)))
    else:
        # Try to find a query as a substring
        mults = [i for i in entries if q in i]
        if not mults == []:
            # Restore original capitalization
            for k in range(len(mults)):
                mults[k] = orig_cap(mults[k])

            # Render a results list
            return render(request, 'encyclopedia/results.html', {
                "results": mults,
                "q": q
            })
        else:
            # Render a Not Found error
            return render(request, "encyclopedia/entry404.html", {
            "entry": q.capitalize()
            })

def new(request):
    if request.method == "POST":
        # Create a form obj and populate it with data
        form = NewArtForm(request.POST)
        if form.is_valid():
            # Get an all-entries list
            entries = util.list_entries()
            if not form.cleaned_data["art_title"] in entries:
                # Save a new entry and take to the created entry page
                util.save_entry(form.cleaned_data["art_title"], form.cleaned_data["art_body"])
                return HttpResponseRedirect("wiki/" + form.cleaned_data["art_title"])
            else:
                # Render error - already exists
                return render(request, "encyclopedia/entryexists.html", {
                    "entry": form.cleaned_data["art_title"]
                })
        else:
            # Return back to form
            form = NewArtForm()
            return render(request, "encyclopedia/add.html", {"form": form})
    else:
        # method GET - so just render the form
        form = NewArtForm()
        return render(request, "encyclopedia/add.html", {"form": form})


def edit(request, title):

    art_body = util.get_entry(title)
    if request.method == "GET":
        # Validate title just in case
        if not art_body == None:
            # Title valid: Let's edit the article
            
            # Create and populate the form
            form = NewArtForm(initial={"art_title": title, "art_body": art_body})

            # render the edit page, sending there the form with data
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "title": title
            })
        else:
            # Title invalid - render error
            return render(request, "encyclopedia/entry404.html", {
                "entry": title
            })
    else: # Request method is POST
        # Save a new entry and take to the created entry page
        util.save_entry(request.POST["title"], request.POST["art_body"])
        return HttpResponseRedirect("/wiki/" + request.POST["title"])
            

def randp(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect("/wiki/" + entry)