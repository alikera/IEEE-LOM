import json
import os
from process_slide import *

# Get all files in the directory
copy_assets()
directory = "assets"
files = os.listdir(directory)
images = []
others = []
my_slides = []
for file in files:
    extension = os.path.splitext(file)[1]
    if extension == '.pptx':
        my_slides.append(file)
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
    insert_slide_initial_metadata(lom, 'slide', 'Expositive')
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

new_dir = "metadatas"
counter = 0
for slide in my_slides:
    filename = os.path.splitext(slide)[0] + '.json'
    filedir = os.path.join(new_dir,filename)
    with open(filedir, 'w') as fp:
        json.dump(LOMs[counter], fp, indent=4)
    counter += 1

