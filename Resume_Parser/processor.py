import os
import spacy
import pymupdf as fitz
import requests
import logging
from init import download_resumes_and_jd
from extractors import (
    extract_name,
    extract_email,
    extract_contact_number_from_resume,
    extract_education_from_resume,
    extract_skills,
    extract_experience
)

# Configure logging
LOG_FILE = "app.log"
logging.basicConfig(
    filename=LOG_FILE,  # Log file name
    level=logging.INFO,  # Log INFO level and above
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Log application startup
logging.info("Processor.py script started.")

# Execute the init function to download resumes and job description
def download_data():
    try:
        logging.info("Starting download of resumes and job description...")
        download_resumes_and_jd()
        logging.info("Download complete.")
    except Exception as e:
        logging.error(f"Error during download: {str(e)}")
        raise

# Load the SpaCy model at the beginning
try:
    nlp = spacy.load('en_core_web_sm')
    logging.info("SpaCy model 'en_core_web_sm' loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load SpaCy model: {str(e)}")
    raise

# Function to call Node.js API and fetch resumes collection
def fetch_resumes_collection(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for HTTP codes like 4xx/5xx
        logging.info(f"Resumes collection fetched successfully from {api_url}.")
        return response.json()  # Return the JSON response as Python dictionary/list
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching resumes collection from API: {e}")
        raise Exception(f"Error fetching resumes collection: {e}")

def extract_resume_info_from_pdf(uploaded_file):
    """
    Extract text information from a PDF file.
    """
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        logging.info("Text extracted successfully from resume PDF.")
        return nlp(text)
    except Exception as e:
        logging.error(f"Error extracting information from PDF: {str(e)}")
        raise

def extract_resume_info(doc):
    """
    Extract detailed information from resume document.
    """
    try:
        first_name, last_name = extract_name(doc)
        email = extract_email(doc)
        contact_number = extract_contact_number_from_resume(doc)
        education = extract_education_from_resume(doc)
        skills = extract_skills(doc)
        experience = extract_experience(doc)
        logging.info("Resume information extracted successfully.")
        return {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'contact_number': contact_number,
            'education': education,
            'skills': skills,
            'experience': experience
        }
    except Exception as e:
        logging.error(f"Error extracting resume details: {str(e)}")
        raise

def process_all_pdfs(input_folder, api_url):
    """
    Process all PDFs in the input folder, extract details and return job description and resumes.
    """
    try:
        # Fetch resumes collection from the API
        resumes_collection = fetch_resumes_collection(api_url)
        logging.info(f"Resumes collection fetched: {len(resumes_collection)} documents found.")

        job_description_file = os.path.join(input_folder, 'job_description.pdf')

        # Load Job Description
        logging.info(f"Loading job description from {job_description_file}.")
        with open(job_description_file, 'rb') as f:
            job_description_doc = extract_resume_info_from_pdf(f)

        resumes = []
        for file_name in os.listdir(input_folder):
            if file_name.endswith('.pdf') and file_name != 'job_description.pdf':
                resume_file_path = os.path.join(input_folder, file_name)
                logging.info(f"Processing resume: {file_name}")
                with open(resume_file_path, 'rb') as f:
                    resume_doc = extract_resume_info_from_pdf(f)
                    resume_info = extract_resume_info(resume_doc)

                    # Retrieve the matching document from the API response
                    existing_document = next(
                        (doc for doc in resumes_collection if doc['filename'] == file_name), None
                    )

                    if existing_document:
                        document_id = str(existing_document['_id'])
                        resume_url = existing_document.get('url', None)
                    else:
                        raise Exception(f"No existing document found for {file_name}")

                    resumes.append({
                        'filename': file_name,
                        'resume_info': resume_info,
                        'document_id': document_id,
                        'url': resume_url  # Add URL to resume data
                    })
                    logging.info(f"Processed resume: {file_name}")

        return job_description_doc, resumes
    except Exception as e:
        logging.error(f"Error processing PDFs: {str(e)}")
        raise

