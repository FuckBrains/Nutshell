__author__ = "Jack Walker"

import os
import re
from PIL import Image, ImageDraw, ImageFont
from pick import pick


def get_inputs(individual_question):

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

    # Get first question number from regex validated input
    while True:
        try:
            if individual_question:

                first_question_number = str(input("Question Number:\n"))
            else:
                first_question_number = str(input("Enter first question number:\n"))

            if re.match('^[1-9]$|^[1-3][0-9]$', first_question_number):
                break
            else:
                raise TypeError
        except TypeError:
            print("Enter question number between 1 and 39:\n")
            continue

    # Get Last question number from regex validated input
    while True:
        try:
            if individual_question:
                last_question_number = first_question_number
            else:
                last_question_number = str(input("Enter last question number:\n"))
                if first_question_number > last_question_number:
                    raise TypeError

            if re.match('^[1-9]$|^[1-3][0-9]$', last_question_number):
                break
            else:
                raise TypeError
        except TypeError:
            print("Enter question number between " + str(first_question_number) + " and 39:\n")
            continue

    return {
        "year": year,
        "paper_type": paper_type,
        "first_question_number": first_question_number,
        "last_question_number": last_question_number
    }


# Generates a portrait and landscape image for a SQA question(s)
def generate_sqa_questions(nutshell_directory, individual_question, header1, header2, orientations):

    inputs = get_inputs(individual_question)

    # Generate paths to files
    image_locations = {}
    output_directory = os.path.join(nutshell_directory, "VideoContent", "GeneratedContent")

    for orientation in orientations:
        image_locations[orientation] = os.path.join(
            nutshell_directory, 
            "VideoContent", "Template Backgrounds", "Blue" + str(orientation) + ".png"
        )

    # For all question numbers in range, generate background images and save
    for question_num in range(int(inputs["first_question_number"]), int(inputs["last_question_number"]) + 1):

        # Generate New images
        images = {}
        draws = {}

        relative_path = os.path.join(output_directory, "SQAPastPaper", inputs["year"], inputs["paper_type"],
                                     str(question_num))

        # Repeat for all orientations
        for orientation in orientations:

            relative_path_with_orientation = os.path.join(relative_path, orientation)
            if not os.path.exists(relative_path_with_orientation):
                os.makedirs(relative_path_with_orientation)

            background_directory = os.path.join(relative_path_with_orientation, "background.png")

            images[orientation] = Image.open(image_locations[orientation])
            draws[orientation] = ImageDraw.Draw(images[orientation])

            display_text = ["SQA Past Paper", inputs["year"] + " " + inputs["paper_type"], "Question " + str(question_num)]
    
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
            w[0], h[0] = draws[orientation].textsize(display_text[0], font=header1)
            for i in range(1, 3):
                w[i], h[i] = draws[orientation].textsize(display_text[i], font=header2)

            for i in range(0, 3):

                font = header1 if i == 0 else header2

                draws[orientation].text(
                    (pixels[0] + (((pixels[1] - pixels[2]) - w[i]) / 2), pixels[i+3]),
                    display_text[i],
                    font=font,
                    fill=(4, 21, 31)
                )

            images[orientation].save(background_directory, "PNG")

        return {
            "question_type": "SQAPastPaper",
            "year": inputs["year"],
            "paper_type": inputs["paper_type"],
            "question_num": question_num,
            "background_path": {
              "landscape": os.path.join(relative_path, "landscape"),
              "portrait":  os.path.join(relative_path, "portrait")
            },
            "relative_path": relative_path
        }

# # Generates a portrait and landscape image for a question related to a topic
# def generatetopicquestion():
#     # Get Text from user
#     print("Source:\n")
#     source = input()
#
#     print("Topic:\n")
#     topic = input()
#
#     text = [source, topic]
#
#     # Generate New images
#     landscapeImage = Image.open(LANDSCAPEIMAGELOCATION)
#     portraitImage = Image.open(PORTAITIMAGELOCATION)
#     drawLandscape = ImageDraw.Draw(landscapeImage)
#     drawPortrait = ImageDraw.Draw(portraitImage)
#
#     # Used to calculate text size and re-calculate position accordingly.
#     w = [None] * 2
#     h = [None] * 2
#
#     # Add text to Landscape image
#     w[0], h[0] = drawLandscape.textsize(text[0], font=header1)
#     w[1], h[1] = drawLandscape.textsize(text[1], font=header2)
#
#     drawLandscape.text((2998 + (((3834 - 3003) - w[0]) / 2), 1000), text[0], font=header1, fill=(4, 21, 31))
#     drawLandscape.text((2998 + (((3834 - 3003) - w[1]) / 2), 1150), text[1], font=header2, fill=(4, 21, 31))
#
#     # Add text to Portrait image
#     drawPortrait.text((0 + (((2158 - 0) - w[0]) / 2), 3300), text[0], font=header1, fill=(4, 21, 31))
#     drawPortrait.text((0 + (((2158 - 0) - w[1]) / 2), 3450), text[1], font=header2, fill=(4, 21, 31))
#
#     # TODO: Update and Test
#     directory = OUPUTDIRECTORY + "Topic Questions/" + source + "/" + topic
#     filename = text[0] + "-" + text[1]
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#
#     landscapeImage.save(directory + "/" + filename + "landscape/ background.png", "PNG")
#     print(filename + " portrait.png" + " saved successfully")
#     portraitImage.save(directory + "/" + filename + "portrait/ background.png", "PNG")
#     print(filename + " portrait.png" + " saved successfully")
#
#     return ["Topic Question", source, topic, filename]


def main(nutshell_directory, orientations):
    # Get headers for background file
    bold_font_filepath = os.path.join(nutshell_directory, 'Branding/Fonts/Montserrat/Montserrat-Bold.ttf')
    light_font_filepath = os.path.join(nutshell_directory, 'Branding/Fonts/Montserrat/Montserrat-Light.ttf')
    header1 = ImageFont.truetype(bold_font_filepath, 80)
    header2 = ImageFont.truetype(light_font_filepath, 80)

    # Get type of background from user and generate accordingly
    question_type_question = 'Please choose question type'
    question_type_options = ['SQA Question', 'SQA Questions', 'Topic Question']
    question_type, question_type_index = pick(question_type_options, question_type_question)

    if question_type == "SQA Question":
        details_of_video = generate_sqa_questions(nutshell_directory, True, header1, header2, orientations)
    # elif question_type == "SQA Questions":
    #     details_of_video = generatesqaquestions(False)
    # elif question_type == "Topic Question":
    #     details_of_video = generatetopicquestion()
    else:
        print("Functionality not currently available")

    return details_of_video
