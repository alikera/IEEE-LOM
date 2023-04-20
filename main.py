import json
import os
import filetype
from process_slide import *
from process_pdf import *

def output_metadatas_as_file(file, counter):
    filename = os.path.splitext(file)[0] + '.json'
    filedir = os.path.join(new_dir,filename)
    with open(filedir, 'w') as fp:
        json.dump(LOMs[counter], fp, indent=4)
    counter += 1

# Get all files in the directory
copy_assets()
directory = "assets"
files = os.listdir(directory)
images = []
others = []
my_slides = []
my_exercises = []
my_assets = []
for file in files:
    extension = os.path.splitext(file)[1]
    if extension == '.pptx':
        my_slides.append(file)
        my_assets.append(file)
    elif extension == '.pdf':
        my_exercises.append(file)
        my_assets.append(file)
    elif os.path.splitext(file)[0] == 'temp':
        continue
    elif extension == '.Identifier':
        continue
    elif extension == '.zip':
        continue
    elif filetype.is_image(file) is not None:
        images.append(file)

LOMs = []
for slide in my_slides:
    lom = dict()
    insert_initial_metadata(lom, 'slide', 'Expositive')
    process_slide_interactivity_level_tag(lom, slide)
    process_slide_semantic_density_tag(lom, slide)
    process_slide_intended_end_user_role_tag(lom, slide)
    process_slide_context_tag(lom, slide)
    process_slide_typical_age_range_tag(lom, slide)
    process_slide_difficulty_tag(lom, slide)
    process_slide_typical_learning_time(lom, slide)
    process_slide_description_tag(lom, slide)
    process_slide_language_tag(lom, slide)
    LOMs.append(lom)

for exercise in my_exercises:
    lom = dict()
    insert_initial_metadata(lom, 'exercise', 'active')
    process_exercise_interactivity_level_tag(lom, exercise)
    process_exercise_semantic_density_tag(lom, exercise)
    process_exercise_intended_end_user_role_tag(lom, exercise)
    process_exercise_context_tag(lom, exercise)
    process_exercise_typical_age_range_tag(lom, exercise)
    process_exercise_difficulty_tag(lom, exercise)
    process_exercise_typical_learning_time(lom, exercise)
    process_exercise_description_tag(lom, exercise)
    process_exercise_language_tag(lom, exercise)
    LOMs.append(lom)

new_dir = "metadatas"
counter = 0
for slide in my_slides:
    output_metadatas_as_file(slide, counter)
    counter += 1

for exercise in my_exercises:
    output_metadatas_as_file(exercise, counter)
    counter += 1
