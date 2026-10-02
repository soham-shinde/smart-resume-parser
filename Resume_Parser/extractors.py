import spacy
import nltk
import csv
import re

# Download required NLTK data
nltk.download('punkt')

# Load SpaCy models
nlp = spacy.load('en_core_web_sm')
nlp_skills = spacy.load('TrainedModel/Model1')

# Function to load keywords from a CSV
def load_keywords(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return set(row[0] for row in reader)

# Extraction functions
def extract_name(doc):
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            names = ent.text.split()
            if len(names) >= 2 and names[0].istitle() and names[1].istitle():
                return names[0], ' '.join(names[1:])
    return "", ""

def extract_email(doc):
    matcher = spacy.matcher.Matcher(nlp.vocab)
    email_pattern = [{'LIKE_EMAIL': True}]
    matcher.add('EMAIL', [email_pattern])

    matches = matcher(doc)
    for match_id, start, end in matches:
        if match_id == nlp.vocab.strings['EMAIL']:
            return doc[start:end].text
    return ""

def extract_contact_number_from_resume(doc):
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, doc.text)
    return match.group() if match else None

def extract_education_from_resume(doc):
    universities = []
    for entity in doc.ents:
        if entity.label_ == "ORG" and any(keyword in entity.text.lower() for keyword in ["university", "college", "institute"]):
            universities.append(entity.text)
    return universities

def extract_skills_from_csv(doc):
    skills_keywords = load_keywords('data/newSkills.csv')
    return {keyword for keyword in skills_keywords if keyword.lower() in doc.text.lower()}

def extract_skills_from_ner(doc):
    skills = {ent.text for ent in nlp_skills(doc.text).ents if ent.label_ == 'SKILL'}
    return {skill for skill in skills if len(skill) > 1 and not any(char.isdigit() for char in skill)}

def extract_skills(doc):
    return list(extract_skills_from_csv(doc) | extract_skills_from_ner(doc))

def extract_experience(doc):
    verbs = [token.lemma_ for token in doc if token.pos_ == 'VERB']
    if any(verb in verbs for verb in ['lead', 'manage', 'direct']):
        return "Senior"
    if any(verb in verbs for verb in ['develop', 'design', 'analyze']):
        return "Mid-Senior"
    if any(verb in verbs for verb in ['assist', 'support', 'collaborate']):
        return "Mid-Junior"
    return "Entry Level"
