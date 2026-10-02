import logging
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from processor import process_all_pdfs, extract_resume_info

# Configure logging
LOG_FILE = "app.log"
logging.basicConfig(
    filename=LOG_FILE,  # Log file name
    level=logging.INFO,  # Log INFO level and above
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Function to calculate skill score between resume and job description skills
def calculate_skill_score(resume_skills, jd_skills):
    try:
        vectorizer = CountVectorizer().fit_transform([" ".join(resume_skills), " ".join(jd_skills)])
        vectors = vectorizer.toarray()
        score = cosine_similarity(vectors)[0][1] * 100  # Percentage score
        logging.info(f"Calculated skill match score: {score}")
        return score
    except Exception as e:
        logging.error(f"Error calculating skill score: {str(e)}")
        raise

# Function to calculate matching scores between resumes and job description
def calculate_matching_scores(job_description, resumes):
    try:
        jd_skills = job_description['skills']
        results = []

        logging.info("Starting matching score calculation...")

        for resume in resumes:
            resume_skills = resume['resume_info']['skills']
            score = calculate_skill_score(resume_skills, jd_skills)
            results.append({
                'filename': resume['filename'],
                'matching_score': round(score, 2),
                'skills_matched': list(set(resume_skills) & set(jd_skills)),
                'reference_id': resume['document_id'],  # Add reference
                'url': resume.get('url', 'URL not available'),
            })

            logging.info(f"Processed resume: {resume['filename']} - Score: {score}")

        return results
    except Exception as e:
        logging.error(f"Error calculating matching scores: {str(e)}")
        raise


if __name__ == "__main__":
    input_folder = 'input'
    api_url = "http://localhost:3000/resumes"

    try:
        # Extract resumes and job description using process_all_pdfs from processor.py
        logging.info("Extracting resumes and job description...")
        job_description_doc, resumes = process_all_pdfs(input_folder, api_url)

        # Convert job description document to structured data
        job_description = extract_resume_info(job_description_doc)

        # Calculate matching scores
        logging.info("Calculating matching scores...")
        scores = calculate_matching_scores(job_description, resumes)
        logging.info(f"Matching scores calculated: {scores}")
    except Exception as e:
        logging.error(f"Error during score calculation: {str(e)}")
