from VideoCreationModules.UserInput import get_input

__author__ = "Jack Walker"

import os
from PIL import Image, ImageDraw, ImageFont


# Generates a portrait and landscape image for a SQA question(s)
def generate_background(nutshell_directory, header1, header2, orientations, inputs):

    # Generate paths to files
    image_locations = {}

    for orientation in orientations:
        image_locations[orientation] = os.path.join(
            nutshell_directory, 
            "VideoContent", "Template Backgrounds", "Blue" + str(orientation) + ".png"
        )

    # Generate New images
    images = {}
    draws = {}

    # Repeat for all orientations
    for orientation in orientations:

        relative_path_with_orientation = os.path.join(inputs["relative_path"], orientation)
        if not os.path.exists(relative_path_with_orientation):
            os.makedirs(relative_path_with_orientation)

        background_directory = os.path.join(relative_path_with_orientation, "background.png")

        images[orientation] = Image.open(image_locations[orientation])
        draws[orientation] = ImageDraw.Draw(images[orientation])

        lines_of_text = len(inputs["display_text"][orientation])

        # Used to calculate text size and re-calculate position accordingly.
        w = [None] * lines_of_text
        h = [None] * lines_of_text

        if orientation == "landscape":
            pixels = [2998, 3834, 3003, 900, 1050]
            for l in range(0, lines_of_text-2):
                pixels = pixels + [pixels[4+l] + 100]
        elif orientation == "portrait":
            pixels = [0, 2158, 0, 3200, 3350]
            for l in range(0, lines_of_text - 2):
                pixels = pixels + [pixels[4 + l] + 100]
        else:
            print("Orientation not supported")

        # Add text to Landscape image
        w[0], h[0] = draws[orientation].textsize(inputs["display_text"][orientation][0], font=header1)
        for i in range(1, lines_of_text):
            w[i], h[i] = draws[orientation].textsize(inputs["display_text"][orientation][i], font=header2)

        for i in range(0, lines_of_text):

            font = header1 if i == 0 else header2

            draws[orientation].text(
                (pixels[0] + (((pixels[1] - pixels[2]) - w[i]) / 2), pixels[i+3]),
                inputs["display_text"][orientation][i],
                font=font,
                fill=(4, 21, 31)
            )

        images[orientation].save(background_directory, "PNG")
        images[orientation].close()

    inputs["background_path"] = {
          "landscape": os.path.join(inputs["relative_path"], "landscape"),
          "portrait":  os.path.join(inputs["relative_path"], "portrait")
        }
    return inputs


def main(nutshell_directory, orientations, inputs):
    # Get headers for background file
    bold_font_filepath = os.path.join(nutshell_directory, 'Branding/Fonts/Montserrat/Montserrat-Bold.ttf')
    light_font_filepath = os.path.join(nutshell_directory, 'Branding/Fonts/Montserrat/Montserrat-Light.ttf')
    header1 = ImageFont.truetype(bold_font_filepath, 80)
    header2 = ImageFont.truetype(light_font_filepath, 80)

    details_of_video = generate_background(nutshell_directory, header1, header2, orientations, inputs)

    return details_of_video
