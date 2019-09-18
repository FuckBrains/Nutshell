__author__ = "Jack Walker"

import os
import re
from PIL import Image, ImageDraw, ImageFont
from pick import pick


def get_sqa_input():

    # Get past paper year from regex validated input
    while True:
        try:
            year = str(input("Year of paper:\n"))
            if re.match('^[1-2][0-9]{3}$', year):
                break
            else:
                raise TypeError
        except TypeError:
            print("Enter year in format yyyy:\n")
            continue

    # Get past paper type from selection
    paper_type_question = 'Please choose paper type'
    paper_type_options = ['Calculator', 'Non-Calculator']
    paper_type, paper_typeindex = pick(paper_type_options, paper_type_question)

    # Get question number from regex validated input
    while True:
        try:
            question_number = str(input("Question Number:\n"))

            if re.match('^[1-9]$|^[1-3][0-9]$', question_number):
                break
            else:
                raise TypeError
        except TypeError:
            print("Enter question number between 1 and 39:\n")
            continue

    return {
        "type": "sqa",
        "year": year,
        "paper_type": paper_type,
        "question_number": question_number,
        "display_text": ["SQA Past Paper", year + " " + paper_type, "Question " + str(question_number)]
    }


def get_input(code):
    switcher = {
        "sqa": get_sqa_input(),
        # "n5w": get_n5w_input()
    }
    return switcher.get(code)


# Generates a portrait and landscape image for a SQA question(s)
def generate_background(nutshell_directory, header1, header2, orientations, inputs):

    # Generate paths to files
    image_locations = {}
    output_directory = os.path.join(nutshell_directory, "VideoContent", "GeneratedContent")

    for orientation in orientations:
        image_locations[orientation] = os.path.join(
            nutshell_directory, 
            "VideoContent", "Template Backgrounds", "Blue" + str(orientation) + ".png"
        )

    # Generate New images
    images = {}
    draws = {}

    relative_path = os.path.join(output_directory, "SQAPastPaper", inputs["year"], inputs["paper_type"],
                                 str(inputs["question_number"]))

    # Repeat for all orientations
    for orientation in orientations:

        relative_path_with_orientation = os.path.join(relative_path, orientation)
        if not os.path.exists(relative_path_with_orientation):
            os.makedirs(relative_path_with_orientation)

        background_directory = os.path.join(relative_path_with_orientation, "background.png")

        images[orientation] = Image.open(image_locations[orientation])
        draws[orientation] = ImageDraw.Draw(images[orientation])

        # Used to calculate text size and re-calculate position accordingly.
        w = [None] * 3
        h = [None] * 3

        if orientation == "landscape":
            pixels = [2998, 3834, 3003, 900, 1050, 1150]
        elif orientation == "portrait":
            pixels = [0, 2158, 0, 3200, 3350, 3450]
        else:
            print("Orientation not supported")

        # Add text to Landscape image
        w[0], h[0] = draws[orientation].textsize(inputs["display_text"][0], font=header1)
        for i in range(1, 3):
            w[i], h[i] = draws[orientation].textsize(inputs["display_text"][i], font=header2)

        for i in range(0, 3):

            font = header1 if i == 0 else header2

            draws[orientation].text(
                (pixels[0] + (((pixels[1] - pixels[2]) - w[i]) / 2), pixels[i+3]),
                inputs["display_text"][i],
                font=font,
                fill=(4, 21, 31)
            )

        images[orientation].save(background_directory, "PNG")
        images[orientation].close()

    return {
        "question_type": "SQAPastPaper",
        "year": inputs["year"],
        "paper_type": inputs["paper_type"],
        "question_num": inputs["question_number"],
        "background_path": {
          "landscape": os.path.join(relative_path, "landscape"),
          "portrait":  os.path.join(relative_path, "portrait")
        },
        "relative_path": relative_path
    }


def main(nutshell_directory, orientations):
    # Get headers for background file
    bold_font_filepath = os.path.join(nutshell_directory, 'Branding/Fonts/Montserrat/Montserrat-Bold.ttf')
    light_font_filepath = os.path.join(nutshell_directory, 'Branding/Fonts/Montserrat/Montserrat-Light.ttf')
    header1 = ImageFont.truetype(bold_font_filepath, 80)
    header2 = ImageFont.truetype(light_font_filepath, 80)

    # Get type of background from user and generate accordingly
    question_type_question = 'Please choose question type'
    question_type_options = ['sqa', 'n5w']
    code, code_index = pick(question_type_options, question_type_question)

    inputs = get_input(code)
    details_of_video = generate_background(nutshell_directory, header1, header2, orientations, inputs)

    return details_of_video
