from django.shortcuts import render

from . import util

import markdown2

from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    content = util.get_entry(entry_name)
    if not content == None:
        contentHttp = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html",{
            "entry": entry_name.capitalize(),
            "content": contentHttp
        })
    else:
        return render(request, "encyclopedia/entry404.html", {
            "entry": entry_name.capitalize()
        })


def search(request):
    q = str(request.GET.get('q')).lower()
    entries = util.list_entries()
    for i in range(len(entries)):
        entries[i] = entries[i].lower()

    if q in entries:
        return HttpResponseRedirect(reverse('entry' , args=(q,)))
    else:
        mults = [i for i in entries if q in i]
        if not mults == []:
            return render(request, 'encyclopedia/results.html', {
                "results": mults,
                "q": q
            })
        else:
            return render(request, "encyclopedia/entry404.html", {
            "entry": q.capitalize()
            })