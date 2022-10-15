import os
import sys
import wptools
from bs4 import BeautifulSoup


def get_cd(phrase):
    """
    Returns a definition for noun phrase
    Keyword arguments:
    phrase -- phrase (str)
    """
    so = wptools.page(phrase, silent=True).get_parse()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    a = so.data["parsetree"]
    short_desc = (
        BeautifulSoup(a, "html.parser")
        .find("title")
        .nextSibling.contents[1]
        .contents[0]
    )
    return short_desc


print(get_cd("cat"))