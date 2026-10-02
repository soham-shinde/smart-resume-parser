import os
import spacy
import random
from spacy.training.example import Example
from spacy.training import offsets_to_biluo_tags
nlp = spacy.blank("en")  # or you can use spacy.load("en_core_web_sm")

# Updated training data with phrases and skill-related keywords
UPDATED_TRAIN_DATA = [
    ("Proficient in Python, Java, and C++", {"entities": [(14, 20, "SKILL"), (22, 26, "SKILL"), (32, 35, "SKILL")]}),
    ("Experience with machine learning algorithms", {"entities": [(16, 32, "SKILL")]}),
    ("Familiar with TensorFlow and PyTorch", {"entities": [(14, 24, "SKILL"), (29, 36, "SKILL")]}),
    ("Strong understanding of HTML, CSS, and JavaScript", {"entities": [(24, 28, "SKILL"), (30, 33, "SKILL"), (39, 49, "SKILL")]}),
    ("Expertise in data analysis and visualization using Tableau", {"entities": [(13, 26, "SKILL"), (51, 58, "SKILL")]}),
    ("Skilled in SQL database management", {"entities": [(11, 14, "SKILL"), (15, 34, "SKILL")]}),
    ("Knowledge of React and Angular frameworks", {"entities": [(13, 18, "SKILL"), (23, 30, "SKILL")]}),
    ("Proficiency in MATLAB for numerical computing", {"entities": [(15, 21, "SKILL"), (26, 45, "SKILL")]}),
    ("Experience with cloud technologies like AWS and Azure", {"entities": [(40, 43, "SKILL"), (48, 53, "SKILL")]}),
    ("Expertise in natural language processing and NLP techniques", {"entities": [(13, 40, "SKILL"), (45, 48, "SKILL")]}),
    ("Familiarity with Git version control system", {"entities": [(17, 20, "SKILL"), (21, 36, "SKILL")]}),
    ("Knowledgeable in DevOps practices and CI/CD pipelines", {"entities": [(17, 23, "SKILL"), (38, 53, "SKILL")]}),
    ("Proficient in Java Spring and Hibernate frameworks", {"entities": [(14, 25, "SKILL"), (30, 39, "SKILL")]}),
    ("Expert in Linux kernel and system administration", {"entities": [(10, 15, "SKILL"), (16, 22, "SKILL"), (27, 48, "SKILL")]}),
    ("Advanced networking skills - configuring routers, switches, firewalls", {"entities": [(9, 26, "SKILL")]}), 
    ("Experience setting up Kubernetes clusters on AWS and GCP", {"entities": [(22, 32, "SKILL"), (45, 48, "SKILL"), (53, 56, "SKILL")]}),
    ("Skilled software developer with 5 years building scalable web apps", {"entities": [(40, 66, "SKILL")]}),
    ("Proficiency in Java, Python, C++, JavaScript, and Golang", {"entities": [(15, 19, "SKILL"), (21, 27, "SKILL"), (29, 32, "SKILL"), (34, 44, "SKILL"), (50, 56, "SKILL")]}),
    ("Expertise in full stack development using MongoDB, Express, React, Node.js", {"entities": [(13, 35, "SKILL"), (42, 49, "SKILL"), (51, 58, "SKILL"), (60, 65, "SKILL"), (67, 74, "SKILL")]}),
    ("Experience with machine learning libraries PyTorch, TensorFlow, Keras", {"entities": [(16, 32, "SKILL"), (43, 50, "SKILL"), (52, 62, "SKILL"), (64, 69, "SKILL")]}),
    ("Skilled in CI/CD pipelines, GitLab, Jenkins, Bamboo, CircleCI", {"entities": [[11, 26, "SKILL"], [28, 34, "SKILL"], [36, 43, "SKILL"], [45, 51, "SKILL"], [53, 61, "SKILL"]]}),
    ("SQL", {"entities": [(0, 3, "SKILL")]}),
    ("JavaScript", {"entities": [(0, 10, "SKILL")]}),
    ("Machine Learning", {"entities": [(0, 16, "SKILL")]}),
    ("Data Analysis", {"entities": [(0, 13, "SKILL")]}),
    ("React.js", {"entities": [(0, 8, "SKILL")]}),
    ("AngularJS", {"entities": [(0, 9, "SKILL")]}),
    ("Node.js", {"entities": [(0, 7, "SKILL")]}),
    ("MongoDB", {"entities": [(0, 7, "SKILL")]}),
    ("AWS Cloud", {"entities": [(0, 9, "SKILL")]}),
    ("Azure Cloud", {"entities": [(0, 11, "SKILL")]}),
    ("Statistical Modeling", {"entities": [(0, 20, "SKILL")]}),
    ("Linux operating system", {"entities": [(0, 5, "SKILL")]}),
    ("Windows Server administration", {"entities": [(0, 29, "SKILL")]}),
    ("Network configuration and Network troubleshooting", {"entities": [(0, 21, "SKILL"), (26, 49, "SKILL")]}),
    ("TCP/IP, OSI model", {"entities": [(0, 6, "SKILL"), (8, 11, "SKILL")]}), 
    ("Routing protocols like OSPF, BGP", {"entities": [(0, 17, "SKILL"), (23, 27, "SKILL"), (29, 32, "SKILL")]}),
    ("Cisco switching and routing", {"entities": [(0, 5, "SKILL")]}),
    ("Firewall administration", {"entities": [(0, 8, "SKILL")]}),
    ("Network security", {"entities": [(0, 16, "SKILL")]}),
    ("Penetration testing", {"entities": [(0, 19, "SKILL")]}),
    ("Burp Suite", {"entities": [(0, 10, "SKILL")]}),
    ("Wireshark network analysis", {"entities": [(0, 9, "SKILL"), (10, 26, "SKILL")]}),
    ("Docker containerization", {"entities": [(0, 6, "SKILL"), (7, 23, "SKILL")]}),
    ("Kubernetes", {"entities": [(0, 10, "SKILL")]}),
    ("Jenkins CI/CD pipelines", {"entities": [(0, 7, "SKILL"), (8, 23, "SKILL")]}), 
    ("Ansible automation", {"entities": [(0, 7, "SKILL")]}),
    ("Azure administration", {"entities": [(0, 5, "SKILL")]}),
    ("AWS cloud architecture", {"entities": [(0, 3, "SKILL"), (4, 22, "SKILL")]}),
    ("Google Cloud Platform", {"entities": [(0, 21, "SKILL")]}),
    ("DevOps culture and practices ", {"entities": [(0, 6, "SKILL")]}),
    ("Agile development methodologies", {"entities": [(0, 5, "SKILL")]}),
    ("Waterfall SDLC", {"entities": [(0, 9, "SKILL"), (10, 14, "SKILL")]}),
    ("Object-oriented analysis and design", {"entities": [(0, 24, "SKILL")]}), 
    ("SQL database programming", {"entities": [(0, 3, "SKILL"), (4, 24, "SKILL")]}),
    ("Oracle database administration", {"entities": [(0, 6, "SKILL"), (7, 30, "SKILL")]}),
    ("MongoDB NoSQL databases", {"entities": [(0, 7, "SKILL"), (8, 23, "SKILL")]}),
    ("Redis in-memory caching", {"entities": [(0, 5, "SKILL")]}),
    ("Data modeling and Data warehousing", {"entities": [(0, 13, "SKILL"), (18, 34, "SKILL")]}), 
    ("Hadoop cluster configuration", {"entities": [(0, 6, "SKILL"), (7, 28, "SKILL")]}),
    ("Spark big data processing", {"entities": [(0, 5, "SKILL"), (6, 14, "SKILL")]}),
    ("Tableau data visualization", {"entities": [(0, 7, "SKILL"), (8, 26, "SKILL")]}), 
    ("Power BI business analytics", {"entities": [(0, 8, "SKILL"), (9, 27, "SKILL")]}),
    ("Python programming", {"entities": [(0, 6, "SKILL"), (7, 18, "SKILL")]}), 
    ("Java Spring Boot framework", {"entities": [(0, 4, "SKILL"), (5, 16, "SKILL")]}),  
    ("PHP web application development", {"entities": [(0, 3, "SKILL"), (4, 31, "SKILL")]}),
    ("Ruby on Rails web framework", {"entities": [(0, 4, "SKILL"), (8, 13, "SKILL")]}),
    ("JavaScript front-end development", {"entities": [(0, 10, "SKILL"), (11, 32, "SKILL")]}),
    ("React web applications", {"entities": [(0, 5, "SKILL")]}),
    ("Angular single page applications", {"entities": [(0, 7, "SKILL"), (8, 32, "SKILL")]}),
    ("Node.js back-end services", {"entities": [(0, 7, "SKILL"), (8, 25, "SKILL")]}),
    ("REST API design and development", {"entities": [(0, 8, "SKILL")]}),
    ("GraphQL API development", {"entities": [(0, 7, "SKILL"), (8, 23, "SKILL")]}),
    ("Unit testing frameworks like JUnit", {"entities": [(0, 12, "SKILL"), (29, 34, "SKILL")]}),
    ("UX design and usability", {"entities": [(0, 9, "SKILL")]}),
    ("Git version control system", {"entities": [(0, 3, "SKILL"), (4, 26, "SKILL")]}),
    ("Continuous integration and delivery", {"entities": [(0, 35, "SKILL")]}), 
    ("R language data analysis", {"entities": [(0, 1, "SKILL")]}), 
    ("MATLAB numerical computing", {"entities": [(0, 6, "SKILL")]}),
    ("C++ high performance programming", {"entities": [(0, 3, "SKILL")]}),
    ("Multithreading and concurrency", {"entities": [(0, 14, "SKILL")]}),
    ("Cryptography and encryption algorithms", {"entities": [(0, 12, "SKILL"), (17, 38, "SKILL")]}),
    ("Cybersecurity awareness ", {"entities": [(0, 13, "SKILL")]}),
    ("Penetration testing and ethical hacking", {"entities": [(0, 19, "SKILL"), (24, 39, "SKILL")]}),
    ("Artificial intelligence and machine learning", {"entities": [(0, 23, "SKILL"), (28, 44, "SKILL")]}),
    ("AI and ML", {"entities": [(0, 2, "SKILL"), (7, 9, "SKILL")]}),
    ("Neural networks and deep learning", {"entities": [(0, 15, "SKILL"), (20, 33, "SKILL")]}), 
    ("Computer vision with OpenCV", {"entities": [(0, 15, "SKILL"), (21, 27, "SKILL")]}),
    ("Natural language processing techniques", {"entities": [(0, 27, "SKILL")]}),
    ("Python", {"entities": [(0, 6, "SKILL")]}),
    ("Java", {"entities": [(0, 4, "SKILL")]}),
    ("JavaScript", {"entities": [(0, 10, "SKILL")]}),
    ("TypeScript", {"entities": [(0, 10, "SKILL")]}),
    ("C++", {"entities": [(0, 3, "SKILL")]}),
    ("C#", {"entities": [(0, 2, "SKILL")]}),
    ("Go", {"entities": [(0, 2, "SKILL")]}),
    ("Ruby", {"entities": [(0, 4, "SKILL")]}),
    ("PHP", {"entities": [(0, 3, "SKILL")]}),
    ("Swift", {"entities": [(0, 5, "SKILL")]}),
    ("Rust", {"entities": [(0, 4, "SKILL")]}),
    ("Dart", {"entities": [(0, 4, "SKILL")]}),
    ("Kotlin", {"entities": [(0, 6, "SKILL")]}),
    ("SQL", {"entities": [(0, 3, "SKILL")]}),
    ("NoSQL", {"entities": [(0, 5, "SKILL")]}),
    ("C", {"entities": [(0, 1, "SKILL")]}),
    ("Scala", {"entities": [(0, 5, "SKILL")]}),
    ("Perl", {"entities": [(0, 4, "SKILL")]}),
    ("Haskell", {"entities": [(0, 7, "SKILL")]}),
    ("Bash", {"entities": [(0, 4, "SKILL")]}),
    ("Shell", {"entities": [(0, 5, "SKILL")]}),
    ("Cobol", {"entities": [(0,5, "SKILL")]}),
    ("Fortran", {"entities": [(0,7, "SKILL")]}),
    ("Visual Basic", {"entities": [(0,12, "SKILL")]}),
    ("Assembly", {"entities": [(0,8, "SKILL")]}),
    ("Pascal", {"entities": [(0,6, "SKILL")]}),
    ("Ada", {"entities": [(0,3, "SKILL")]}),
    ("ABAP", {"entities": [(0,4, "SKILL")]}), 
    ("RPG", {"entities": [(0,3, "SKILL")]}),
    ("Lisp", {"entities": [(0,4, "SKILL")]}),
    ("Prolog", {"entities": [(0,6, "SKILL")]}),
    ("F#", {"entities": [(0,2, "SKILL")]}),
    ("Lua", {"entities": [(0,3, "SKILL")]}),
    ("MATLAB", {"entities": [(0,6, "SKILL")]}),
    ("SAS", {"entities": [(0,3, "SKILL")]}),
    ("SPSS", {"entities": [(0,4, "SKILL")]}),
    ("R", {"entities": [(0,1, "SKILL")]}),
    ("Julia", {"entities": [(0,5, "SKILL")]}),
    ("Mahout", {"entities": [(0,6, "SKILL")]}), 
    ("Solr", {"entities": [(0,4, "SKILL")]}),
    ("Lucene", {"entities": [(0,6, "SKILL")]}),
    ("Cassandra", {"entities": [(0,9, "SKILL")]}), 
    ("Neo4j", {"entities": [(0,5, "SKILL")]}),
    ("Unix", {"entities": [(0,4, "SKILL")]}),
    ("Linux", {"entities": [(0,5, "SKILL")]}),
    ("Windows", {"entities": [(0,7, "SKILL")]}),
    ("MacOS", {"entities": [(0,5, "SKILL")]}),
    ("Android", {"entities": [(0,7, "SKILL")]}),
]


# Function to train the NER model with updated data
def train_spacy_ner_updated(data, iterations=20):
    nlp = spacy.blank("en")  # Create a blank 'en' model

    # Create a Named Entity Recognition (NER) pipeline
    ner = nlp.add_pipe("ner", name="ner", last=True)
    ner.add_label("SKILL")  # Add the label for skills recognition

    # Begin training
    nlp.begin_training()

    # Iterate through training data
    for itn in range(iterations):
        random.shuffle(data)
        losses = {}
        # Create examples and update the model
        for text, annotations in data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.5, losses=losses)

        print("Iteration:", itn+1, "Loss:", losses)

    return nlp

# Train the NER model with the updated data
trained_nlp_skills_updated = train_spacy_ner_updated(UPDATED_TRAIN_DATA)

# Test the trained model with a sample text
text_to_test = "Proficiency in Python and machine learning is required."
doc_test = trained_nlp_skills_updated(text_to_test)
for ent in doc_test.ents:
    if ent.label_ == "SKILL":
        print(f"Skill: {ent.text}")

# Save the trained model to disk
output_dir = 'TrainedModel/Model1'
os.makedirs(output_dir, exist_ok=True)  # This will create the directory if it doesn't exist

trained_nlp_skills_updated.to_disk(output_dir)
print("Model saved to:", output_dir)
