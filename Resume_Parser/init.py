import os
import requests
import logging

# Folder to store downloaded PDFs
INPUT_FOLDER = './input/'

# Configure logging
LOG_FILE = "app.log"
logging.basicConfig(
    filename=LOG_FILE,  # Log file name
    level=logging.INFO,  # Log INFO level and above
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def download_pdf(url, filename):
    try:
        # Send GET request to download the PDF (add stream=True for large files)
        response = requests.get(url, timeout=10, stream=False)
        response.raise_for_status()  # Raise an error for bad responses (status code 4xx or 5xx)

        # Ensure the input directory exists
        if not os.path.exists(INPUT_FOLDER):
            os.makedirs(INPUT_FOLDER)

        # Write the content to a PDF file with the provided filename
        file_path = os.path.join(INPUT_FOLDER, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        logging.info(f"Downloaded: {filename}")
        return file_path

    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading {filename}: {e}")
        return None

def download_resumes_and_jd():
    try:
        base_url = "http://localhost:3000"

        # Download the newest job description
        jd_response = requests.get(f"{base_url}/jd/latest", timeout=10)
        if jd_response.status_code == 404:
            logging.warning("No job description found in the database.")
        else:
            jd_response.raise_for_status()
            jd_path = download_pdf(jd_response.json()['url'], "job_description.pdf")
            if jd_path:
                logging.info("Latest job description downloaded: job_description.pdf")

        # Download all resumes
        response = requests.get(f"{base_url}/resumes", timeout=10)
        response.raise_for_status()  # Ensure a successful response

        resumes_data = response.json()

        if not resumes_data:
            logging.warning("No resumes found in the database.")
            return

        for resume in resumes_data:
            resume_url = resume['url']
            resume_filename = resume['filename']
            
            resume_path = download_pdf(resume_url, resume_filename)
            if resume_path:
                logging.info(f"Downloaded resume: {resume_filename}")
            else:
                logging.error(f"Failed to download resume: {resume_filename}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching resumes data: {e}")

# Call the function to download all files
download_resumes_and_jd()
