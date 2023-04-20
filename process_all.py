import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import string
import textstat

import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

def calculate_unique_words_density(text):
    # Initialize lemmatizer
    lemmatizer = WordNetLemmatizer()

    text_without_punctuations = text.translate(str.maketrans("", "", string.punctuation))

    # Tokenize the text into words
    words = nltk.word_tokenize(text_without_punctuations)

    # Remove stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    words = [word for word in words if word.lower() not in stopwords]

    # Lemmatize the words
    lemmatized_words = []
    for word in words:
        # Get the part of speech (pos) tag for the word
        pos_tag = nltk.pos_tag([word])[0][1][0].lower()
        
        # Map the pos tag to the WordNet pos tags
        if pos_tag == 'j':
            pos_tag = wordnet.ADJ
        elif pos_tag == 'v':
            pos_tag = wordnet.VERB
        elif pos_tag == 'n':
            pos_tag = wordnet.NOUN
        elif pos_tag == 'r':
            pos_tag = wordnet.ADV
        else:
            pos_tag = None
        
        if pos_tag:
            # Lemmatize the word using the WordNet pos tag
            lemma = lemmatizer.lemmatize(word, pos=pos_tag)
        else:
            lemma = lemmatizer.lemmatize(word)
            
        lemmatized_words.append(lemma)

    # Remove duplicates
    unique_words = list(set(lemmatized_words))
    num_unique_words = len(unique_words)
    num_words = len(lemmatized_words)
    if num_words == 0:
        return None
    semantic_density = num_unique_words / num_words
    # Print the unique words after lemmatization and removing duplicates
    return semantic_density
    # print(semantic_density)

def get_semantic_density_level(semantic_density):
    if(semantic_density <= 0.2):
        return 1
    if(semantic_density > 0.2 and semantic_density <= 0.4):
        return 2
    if(semantic_density > 0.4 and semantic_density <= 0.60):
        return 3
    if(semantic_density > 0.60 and semantic_density <= 0.8):
        return 4
    if(semantic_density > 0.8):
        return 5

def get_difficulty_level(linsear_score):
    if(linsear_score < 5):
        return 1
    if(linsear_score >= 5 and linsear_score < 10):
        return 2
    if(linsear_score >= 10 and linsear_score < 15):
        return 3
    if(linsear_score >= 15 and linsear_score < 20):
        return 4
    if(linsear_score >= 20):
        return 5


def convert_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

def get_lang_detector(nlp, name):
    return LanguageDetector()

def detect_text_language(text):
    nlp = spacy.load("en_core_web_sm")
    Language.factory("language_detector", func=get_lang_detector)
    nlp.add_pipe('language_detector', last=True)
    doc = nlp(text)

    detect_language = doc._.language #4

    return detect_language['language']