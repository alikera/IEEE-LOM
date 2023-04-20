from process_all import *
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import PyPDF2


def extract_text_from_pdf(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def count_hyperlinks_in_exercise(exercise):
    PDFFile = open("assets/" + exercise,'rb')
    PDF = PyPDF2.PdfReader(PDFFile)
    pages = len(PDF.pages)
    key = '/Annots'
    uri = '/URI'
    ank = '/A'
    counter = 0
    for page in range(pages):
        # print("Current Page: {}".format(page))
        pageSliced = PDF.pages[page]
        pageObject = pageSliced.get_object()
        if key in pageObject.keys():
            ann = pageObject[key]
            for a in ann:
                u = a.get_object()
                if uri in u[ank].keys():
                    counter += 1
    return counter

def count_interactions_in_exercise(exercise):
    count_hyperlinks = count_hyperlinks_in_exercise(exercise)
    if(count_hyperlinks > 0):
        return 2
    else:
        return 1

def process_exercise_interactivity_level_tag(lom, exercise):
    count = count_interactions_in_exercise(exercise)
    lom["interactivityLevel"] = count




def calculate_semantic_density_in_exercise(exercise):
    text = extract_text_from_pdf("assets/"+exercise)
    semantic_density = calculate_unique_words_density(text)
    return get_semantic_density_level(semantic_density)
    

def process_exercise_semantic_density_tag(lom, exercise):
    semantic_density_score = calculate_semantic_density_in_exercise(exercise)
    lom["semanticDensity"] = semantic_density_score
# print(convert_pdf_to_txt("assets/exercise4.pdf"))
# count_interactions_in_exercise("assets/exercise4.pdf")

def process_exercise_intended_end_user_role_tag(lom, exercise):
    lom['intendedEndUserRole'] = 'learner'


def process_exercise_context_tag(lom, exercise):
    age = calculate_exercise_age_range(exercise)
    if(age+1 >= 18):
        lom['context'] = 'higher education'
    elif(age+1 < 18):
        lom['context'] = 'school'

def calculate_exercise_difficulty(exercise):
    # Open the PowerPoint presentation
    text = extract_text_from_pdf("assets/"+exercise)
    linsear_score = textstat.linsear_write_formula(text)
    # Print the text and the readability scores
    return get_difficulty_level(linsear_score)
    
def process_exercise_difficulty_tag(lom, exercise):
    difficulty = calculate_exercise_difficulty(exercise)
    lom['difficulty'] = difficulty

def calculate_exercise_age_estimation(exercise):
    text = extract_text_from_pdf("assets/"+exercise)
    # print("Exxxxxx", exercise)
    # print(textstat.text_standard(text, float_output=True), textstat.linsear_write_formula(text))
    return (textstat.text_standard(text, float_output=True) + textstat.linsear_write_formula(text))/2

def calculate_exercise_age_range(exercise):
    age_estimated = calculate_exercise_age_estimation(exercise)
    difficulty = calculate_exercise_difficulty(exercise)
    # age_mid = int((age_estimated + difficulty)/2)
    age_mid = round(age_estimated)
    return age_mid + 7

def process_exercise_typical_age_range_tag(lom, exercise):
    age = calculate_exercise_age_range(exercise)
    lom['typicalAgeRange'] = str(age-1) + "-" + str(age+1)


def calculate_exercise_learning_time(lom, exercise):
    text = extract_text_from_pdf("assets/"+exercise)
    
    char_read_time = (((100 / lom['difficulty'])) / 60) * 5
    reading_time = textstat.reading_time(text, ms_per_char=1000/char_read_time)
    # print(1000/char_read_time,reading_time)
    hours, minutes, seconds = convert_seconds(reading_time)

    return "PT" + str(int(hours)) + "H" + str(int(minutes)) + "M" + str(int(seconds)) + "S"


def process_exercise_typical_learning_time(lom, exercise):
    reading_time = calculate_exercise_learning_time(lom, exercise)
    lom['typicalLearningTime'] = reading_time

def process_exercise_description_tag(lom, exercise):
    lom['description'] = ""

def detect_exercise_language(exercise):
    text = extract_text_from_pdf("assets/"+exercise)
    return detect_text_language(text)

def process_exercise_language_tag(lom, exercise):
    language = detect_exercise_language(exercise)
    lom['language'] = language