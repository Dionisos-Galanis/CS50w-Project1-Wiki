from django.shortcuts import render, redirect
from encyclopedia import util
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def search(request):
    q = str(request.GET.get('q')).lower()
    entries = util.list_entries()
    for i in range(len(entries)):
        entries[i] = entries[i].lower()

    if q in entries:
        return HttpResponseRedirect(reverse('entry:entry' , args=(q,)))
    else:
        mults = [i for i in entries if q in i]
        if not mults == []:
            return render(request, 'search/results.html', {
                "results": mults,
                "q": q
            })
        else:
            return render(request, "entry/entry404.html", {
            "entry": q.capitalize()
            })
