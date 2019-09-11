__author__ = "Jack Walker"

import os
from WeeklyContentGeneratorModules import WeeklyContentGenerator

nutshell_directory = os.path.abspath(os.path.dirname(__file__))

WeeklyContentGenerator.main(nutshell_directory)
