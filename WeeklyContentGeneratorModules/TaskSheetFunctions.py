from bs4 import BeautifulSoup
from dominate.tags import div, img, h5, a


def replace_in_output(templateTaskSheet, element_type, id, value):
    templateTaskSheet.find(element_type, {"id": id}).string = value


def add_to_output(templateTaskSheet, id_name, content):
    target = templateTaskSheet.find(id=id_name)
    target.insert(0, BeautifulSoup(content, features="html.parser"))


def code_to_information(code):
    switcher = {
        "bbc": {
            "name": "BBC Bitesize",
            "videos": False,
            "notes": True,
            "exercises": True,
            "image": "https://i.imgur.com/KOyk56f.png"
        },
        "y": {
            "name": "YouTube",
            "videos": True,
            "notes": False,
            "exercises": False,
            "image": "https://i.imgur.com/pQsp9HW.png"
        },
        "ka": {
            "name": "Khan Academy",
            "videos": True,
            "notes": True,
            "exercises": True,
            "image": "https://i.imgur.com/SiWC5fP.png"
        },
        "n5w": {
            "name": "National5Maths.co.uk",
            "videos": False,
            "notes": False,
            "exercises": True,
            "image": "https://i.imgur.com/cZTX9Vi.png"
        }
    }
    return switcher.get(code, "nothing")


def generate_resource_html(template_task_sheet, topic, image_url, header_text, p_text, resource_link, resource_type, row=1):
    resource_html = div(_class="learning-resource-container")
    with resource_html.add(div(_class="learning-resource")):
        img(id="learningResourceIcon", src=image_url)
    with resource_html.add(div(_class="learning-resource-text-container")):
        h5(header_text, id="learningResourceName")
        div(_class="learning-resource-types", id="learningResourceTypes").add(p_text)

    button_html = a(
        h5("Go ➔"),
        target="_blank",
        _class="learning-resource-link button",
        href=resource_link,
        id="learningResourceLink"
    )

    if resource_type == "exercise":
        add_to_output(template_task_sheet, resource_type + "-" + str(row) + "-resources-container margin-top", str(resource_html))
        add_to_output(template_task_sheet, resource_type + "-" + str(row) + "-resources-buttons-container", str(button_html))
    else:
        add_to_output(template_task_sheet, resource_type + "-resources-container", str(resource_html))
        add_to_output(template_task_sheet, resource_type + "-resources-buttons-container", str(button_html))
        if resource_type == "test":
            replace_in_output(template_task_sheet, "span", "test-paragraph", topic)

    return {"body": resource_html, "button": button_html}