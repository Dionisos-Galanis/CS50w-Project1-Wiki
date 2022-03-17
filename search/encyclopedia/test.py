import re

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
    ^\s*-[ ] (?P<cont>.+)$             # Skipping leading sapces just in case
    """, re.MULTILINE | re.VERBOSE)

pLink = re.compile(r"""     # Links
    \[(?P<ltext>[^\]]+)\]           # HTML of the link
    \((?P<href>[a-zA-Z:\.\\/]+)\)    # Link itself
    """, re.MULTILINE | re.VERBOSE)

pPar = re.compile(r"""      # Regular paragraphs
    ^(?!([#]+[ ])|(\s*-[ ]))        # Exclude headings and ULs marking atthe beginning
    (?P<cont>.+)$                   # Content of the paragraph (up to newline)
    """, re.MULTILINE | re.VERBOSE)


text = "# Heading 1\n## Heading 2\nFollowing part: **is bold**. And [this is a link](http:\\\\example.com\\myfile.html)\nFurther an unordered list is coming:\n- Item 1\n- Item 2"
print(text + "\n-----------------------")

text = pPar.sub(r"<p>\g<cont></p>", text)

text = pLink.sub(r"<a href='\g<href>'>\g<ltext></a>", text)

text = pUL.sub(r"<ul><li>\g<cont></li></ul>", text)

text = pB.sub(r"<b>\g<cont></b>", text)

text = pI.sub(r"<i>\g<cont></i>", text)

text = pH1.sub(r"<h1>\g<cont></h1>", text)

text = pH2.sub(r"<h2>\g<cont></h2>", text)

text = pH3.sub(r"<h3>\g<cont></h3>", text)

print(text)