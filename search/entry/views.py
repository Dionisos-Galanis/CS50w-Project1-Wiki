from django.shortcuts import render

from encyclopedia import util

import markdown2

# Create your views here.
def entry(request, entry_name):
    content = util.get_entry(entry_name)
    if not content == None:
        contentHttp = markdown2.markdown(content)
        return render(request, "entry/entry.html",{
            "entry": entry_name.capitalize(),
            "content": contentHttp
        })
    else:
        return render(request, "entry/entry404.html", {
            "entry": entry_name.capitalize()
        })
