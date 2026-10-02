from flask import Flask, jsonify, request
from calculate_score import calculate_matching_scores
from processor import process_all_pdfs, extract_resume_info
from flask_cors import CORS
import os
import shutil
from init import download_resumes_and_jd
import warnings
import logging

# Suppress warnings
warnings.filterwarnings("ignore")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Configure logging
LOG_FILE = "app.log"
logging.basicConfig(
    filename=LOG_FILE,  # Log file name
    level=logging.INFO,  # Log INFO level and above
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Logging example: logging.info("Message")
logging.info("Application started.")

@app.route('/calculate-matching-scores', methods=['POST'])
def calculate_matching_scores_api():
    """
    Endpoint to calculate matching scores between resumes and job description.
    """
    try:
        # Start process and log
        # Start with an empty input folder
        input_folder = 'input'
        if os.path.isdir(input_folder):
            for name in os.listdir(input_folder):
                path = os.path.join(input_folder, name)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

        logging.info("Downloading resumes and job description.")
        download_resumes_and_jd()

        # Define API URL
        api_url = "http://localhost:3000/resumes"

        # Ensure input folder exists
        if not os.path.exists(input_folder):
            error_msg = f"Input folder '{input_folder}' does not exist."
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)

        # Process resumes and job description
        logging.info("Processing resumes and job description.")
        job_description_doc, resumes = process_all_pdfs(input_folder, api_url)
        job_description = extract_resume_info(job_description_doc)

        # Calculate matching scores
        logging.info("Calculating matching scores.")
        scores = calculate_matching_scores(job_description, resumes)

        # Log calculated scores and return response
        logging.info(f"Matching scores calculated successfully: {scores}")
        return jsonify(scores), 200

    except Exception as e:
        # Log error details
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Starting the server
    logging.info("Starting Flask server on port 5001.")
    app.run(host="0.0.0.0", port=5001, debug=False)
