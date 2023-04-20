from process_all import *
import os
import zipfile
import shutil
import collections 
import collections.abc
from pptx import Presentation
import pptx
import statistics
import spacy

import textstat
# https://pypi.org/project/textstat/
# https://py-readability-metrics.readthedocs.io/en/latest/

from readability import Readability


import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector


def insert_initial_metadata(lom, resource_type, interactivity):
    lom['learningResourceType'] = resource_type
    lom['interactivityType'] = interactivity


def count_voices_in_slide(power):
    print('Extracting...')
    audio_extensions = ('.aiff', '.au', '.mid', '.midi', '.mp3', '.m4a', '.mp4', '.wav', '.wma')
    init_dir = os.getcwd()

    if not power.endswith('.zip') and not power.endswith('.pptx') or power == 'base_library.zip':
        print("here")
        return

    base = os.path.splitext(power)[0]
    new_zip = 'assets/temp/' + base + '.zip'
    os.rename('assets/temp/'+power, new_zip)
    with zipfile.ZipFile(new_zip) as myzip:
        if myzip.testzip() is not None:
            print("Some of your media files are corrupted")
        else:
            for file in myzip.namelist():
                if file.endswith(audio_extensions):
                    myzip.extract(file)

    myzip.close()

    try:
        os.chdir(init_dir + '/ppt/media')
        count = (len([name for name in os.listdir('.') if os.path.isfile(name)]))
        os.chdir(init_dir)
        shutil.rmtree(init_dir + '/ppt')
        return count
    except FileNotFoundError:
        return 0

def count_interactions_in_slide(power):
    ppt = Presentation("assets/"+power)
    print(power)
    num_videos = 0
    num_forms = 0
    num_clicks = 0
    num_hyperlinks = 0
    num_voices = 0
    counter = -1
    for slide in ppt.slides:
        counter += 1
        # print("slide:                  ",counter)
        for shape in slide.shapes:
            # if(type(shape) is pptx.shapes.autoshape.Shape):
                # print(type(shape), shape.shape_type)
            if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.MEDIA:
                num_videos += 1
                
            if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.FORM_CONTROL:
                num_forms += 1
            
            if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.AUTO_SHAPE:
                if(shape.click_action.target_slide is not None):
                    num_clicks += 1
                # print(shape.click_action._hlink)
                if(shape.click_action.hyperlink is not None):
                    num_hyperlinks += 1

    num_voices = count_voices_in_slide(power)

    points = 0
    if(num_videos > 0):
        points += 1
    if(num_voices > len(ppt.slides) /20):
        points += 1
    if(num_forms > 0):
        points += 1
    if(num_clicks > len(ppt.slides)/2):
        points += 1
    if(num_hyperlinks > len(ppt.slides) /10):
        points += 1
    


    # print("Number of videos:", num_videos)
    # print("Number of voices:", num_voices)

    # print("Number of forms:", num_forms)
    # print("Number of clicks:", num_clicks)
    # print("Number of hyperlinks:", num_hyperlinks)

    return points


def insert_interactivity_level(lom,count):
    lom["interactivityLevel"] = count


def process_slide_interactivity_level_tag(lom, slide):
    count = count_interactions_in_slide(slide)
    insert_interactivity_level(lom, count + 1)

def calculate_slide_semantic_density(curr_slide):
    slide_text = ""
    each_slide_text = ""
    densities = []
    ppt = Presentation("assets/"+curr_slide)
    for slide in ppt.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    slide_text += " " + run.text
                    each_slide_text += " " + run.text
        
        curr_density = calculate_unique_words_density(each_slide_text)
        if curr_density is not None:
            densities.append(curr_density)
        each_slide_text = ""
    
    each_slide_density = (statistics.median(densities) +statistics.mean(densities))/2
    # semantic_density = (calculate_unique_words_density(slide_text) + each_slide_density )/2
    semantic_density = calculate_unique_words_density(slide_text)
    return get_semantic_density_level(semantic_density)
    

    # print(calculate_unique_words_density(slide_text))
    # print(statistics.median(densities))
    # print(statistics.mean(densities))

def calculate_slide_semantic_density2(curr_slide):
    nlp = spacy.load('en_core_web_sm')
    slide_text = ""
    each_slide_text = ""
    ppt = Presentation("assets/"+curr_slide)
    for slide in ppt.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    slide_text += " " + run.text
                    each_slide_text += " " + run.text

    doc = nlp(slide_text)
    similarity_scores = []
    for token1 in doc:
        similarity = 0
        for token2 in doc:
            if token1 != token2:
                similarity += token1.similarity(token2)
        similarity_scores.append(similarity)
    
    semantic_density = sum(similarity_scores) / len(similarity_scores)
    print(semantic_density)


def process_slide_semantic_density_tag(lom, slide):
    semantic_density_score = calculate_slide_semantic_density(slide)
    lom["semanticDensity"] = semantic_density_score


def process_slide_intended_end_user_role_tag(lom, slide):
    lom['intendedEndUserRole'] = 'learner'

def process_slide_context_tag(lom, slide):
    age = calculate_slide_age_range(slide)
    if(age+1 >= 18):
        lom['context'] = 'higher education'
    elif(age+1 < 18):
        lom['context'] = 'school'
    

def extract_text_from_slide(ppt):
    text = ""
    # Iterate over each slide
    for slide in ppt.slides:
        # Iterate over each shape in the slide
        for shape in slide.shapes:
            # Check if the shape contains text
            if shape.has_text_frame:
                # Extract the text from the shape
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        text += "\n" + run.text
    
    return text

def calculate_slide_difficulty(curr_slide):
    # Open the PowerPoint presentation
    ppt = pptx.Presentation("assets/"+curr_slide)
    text = extract_text_from_slide(ppt)
    linsear_score = textstat.linsear_write_formula(text)
    # Print the text and the readability scores
    return get_difficulty_level(linsear_score)


def process_slide_difficulty_tag(lom, slide):
    difficulty = calculate_slide_difficulty(slide)
    lom['difficulty'] = difficulty
    

def calculate_slide_age_estimation(curr_slide):
    ppt = pptx.Presentation("assets/"+curr_slide)
    text = extract_text_from_slide(ppt)

    return (textstat.text_standard(text, float_output=True) + textstat.linsear_write_formula(text))/2


def calculate_slide_age_range(slide):
    age_estimated = calculate_slide_age_estimation(slide)
    difficulty = calculate_slide_difficulty(slide)
    # age_mid = int((age_estimated + difficulty)/2)
    age_mid = round(age_estimated)
    return age_mid + 7

def process_slide_typical_age_range_tag(lom, slide):
    age = calculate_slide_age_range(slide)
    lom['typicalAgeRange'] = str(age-1) + "-" + str(age+1)


def calculate_slide_learning_time(lom, curr_slide):
    ppt = pptx.Presentation("assets/"+curr_slide)
    text = extract_text_from_slide(ppt)
    new_dir = "extracted_context"
    filename = os.path.splitext(curr_slide)[0] + '.txt'
    filedir = os.path.join(new_dir, filename)
    with open(filedir, "w") as f:
        f.write(text)
    
    char_read_time = (((300 / lom['difficulty'])) / 60) * 5
    reading_time = textstat.reading_time(text, ms_per_char=1000/char_read_time)
    # print(1000/char_read_time,reading_time)
    hours, minutes, seconds = convert_seconds(reading_time)

    return "PT" + str(int(hours)) + "H" + str(int(minutes)) + "M" + str(int(seconds)) + "S"


def process_slide_typical_learning_time(lom, slide):
    reading_time = calculate_slide_learning_time(lom, slide)
    lom['typicalLearningTime'] = reading_time


def process_slide_description_tag(lom, slide):
    lom['description'] = ""

def detect_slide_language(curr_slide):
    ppt = pptx.Presentation("assets/"+curr_slide)
    text = extract_text_from_slide(ppt)
    return detect_text_language(text)

def process_slide_language_tag(lom, slide):
    language = detect_slide_language(slide)
    lom['language'] = language

def copy_assets():
    init_dir = os.getcwd()

    origin = init_dir + '/assets/'
    target = origin + '/temp/'

    # Fetching the list of all the files
    files = os.listdir(origin)

    # Fetching all the files to directory
    for file_name in files:
        if file_name == 'temp':
            continue
        shutil.copy(origin+file_name, target+file_name)


