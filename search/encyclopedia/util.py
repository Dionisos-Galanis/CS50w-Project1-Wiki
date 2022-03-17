import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def md2html(mdText):
    """
    Converts Markdown text into HTML text

    Keyword arguments:
    mdText -- string with the markdown formatted text
    Return: string with HTML formatted text
    """
    

    pH1 = re.compile(r"""       # Heading 1
        ^[#]{1}[ ] (?P<cont>.+)$
        """, re.MULTILINE | re.VERBOSE)

    pH2 = re.compile(r"""       # Heading 2
        ^[#]{2}[ ] (?P<cont>.+)$
        """, re.MULTILINE | re.VERBOSE)

    pH3 = re.compile(r"""       # Heading 3
        ^[#]{3}[ ] (?P<cont>.+)$
        """, re.MULTILINE | re.VERBOSE)

    pB = re.compile(r"""        # Bold
        \*\*(?P<cont>\b.+?\b)\*\*
        """, re.MULTILINE | re.VERBOSE)

    pI = re.compile(r"""        # Italic
        \*(?P<cont>\b.+?\b)\*
        """, re.MULTILINE | re.VERBOSE)

    pUL = re.compile(r"""       # Unordered lists, namely list items
        [*+-][ ] (?P<cont>.+)$
        """, re.MULTILINE | re.VERBOSE)

    pLink = re.compile(r"""     # Links
        \[(?P<ltext>[^\]]+)\]            # HTML of the link
        \((?P<href>[a-zA-Z:\.\\/]+)\)    # Link itself
        """, re.MULTILINE | re.VERBOSE)

    pPar = re.compile(r"""      # Regular paragraphs
        ^(?!([#]+[ ])|(\s*-[ ]))        # Exclude headings and ULs marking atthe beginning
        (?P<cont>.+)$                   # Content of the paragraph (up to newline)
        """, re.MULTILINE | re.VERBOSE)

    # Making replacements according to above queries

    print(mdText)

    mdText = pPar.sub(r"<p>\g<cont></p>", mdText)

    mdText = pLink.sub(r"<a href='\g<href>'>\g<ltext></a>", mdText)

    mdText = pB.sub(r"<b>\g<cont></b>", mdText)

    mdText = pI.sub(r"<i>\g<cont></i>", mdText)

    mdText = pUL.sub(r"<ul><li>\g<cont></li></ul>", mdText)

    mdText = pH1.sub(r"<h1>\g<cont></h1>", mdText)

    mdText = pH2.sub(r"<h2>\g<cont></h2>", mdText)

    mdText = pH3.sub(r"<h3>\g<cont></h3>", mdText)

    return mdText
