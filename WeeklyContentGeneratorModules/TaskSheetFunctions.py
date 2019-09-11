from bs4 import BeautifulSoup


def insert_into_output(templateTaskSheet, element_type, id, value):
    templateTaskSheet.find(element_type, {"id": id}).string = value


def add_to_output(templateTaskSheet, class_name, content):
    target = templateTaskSheet.find(class_=class_name)
    target.insert(0, BeautifulSoup(content, features="html.parser"))