import os
from bs4 import BeautifulSoup


def getweekrow(file, week_num):
    table_body = file.find('tbody')
    rows = table_body.find_all('tr')
    row = rows[week_num]

    return row.find_all("td")


def getmatchedrow(file, columnNumber, term):
    table_body = file.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cells = row.find_all("td")
        cellValue = cells[columnNumber].get_text()
        if cellValue == term:
            return row.find_all("td")
    return


def get_file_path(nutshell_directory, code):
    switcher = {
        "APPS": "APPS - App & Tips.html",
        "bbc": "BBC - BBC Bitesize.html",
        "SOW": "SOW - Scheme of Work Overview.html",
        "NUTS": "NUTS - Nuts Learning.html",
        "y": "Y -YouTube.html",
        "MG": "MG - Mr Graham Maths.html",
        "IXL": "IXL - IXL Learning.html",
        "ka": "KA - Khan Academy.html",
        "N5W": "N5W - National5maths.co.uk.html"
    }
    return os.path.join(nutshell_directory, "TaskSheetContent", "PremadeContent", "SchemeOfWork", switcher.get(code, "nothing"))


def gettext(row, column):
    return row[column].get_text()


def gettexts(row, startCol, endCol):
    texts = []
    for item in range(startCol, endCol):
        text = row[item].get_text()
        if text != "":
            texts.extend([text])
    return texts


def getlink(nutshell_directory, code, term):
    file = openfile(get_file_path(nutshell_directory, code))
    row = getmatchedrow(file, 2, term)

    return row[3].get_text()


def getlinks(nutshell_directory, code, terms):
    if code == "N5W":
        matchTitleRow = 4
        linkRow = 5
    else:
        matchTitleRow = 2
        linkRow = 3
    file = openfile(get_file_path(nutshell_directory, code))

    links = []
    for term in terms:
        row = getmatchedrow(file, matchTitleRow, term)
        text = row[linkRow].get_text()
        if text != "":
            links.extend([text])

    return links


def openfile(path):
    with open(path, 'r', encoding="utf8") as f:
        file = f.read()
    return BeautifulSoup(file, 'html.parser')
