import os
from flask import Flask, render_template, request
from langchain_community.document_loaders import WebBaseLoader
from chains import ColdEmailGenerator
from utils import clean_text, load_resume, strip_html
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
email_gen = ColdEmailGenerator()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        job_url = request.form.get("job_url")
        resume_file = request.files.get("resume_file")

        if not job_url or not resume_file:
            error = "Please provide both the job URL and resume."
        else:
            try:
                # Saving resume temporarily
                temp_path = f"temp_{resume_file.filename}"
                resume_file.save(temp_path)

                # Loading and cleaning job posting
                loader = WebBaseLoader(job_url)
                page = loader.load().pop().page_content
                cleaned_job = clean_text(strip_html(page))

                # Extracing job info
                job_info = email_gen.extract_jobs(cleaned_job)
                job_info = job_info if isinstance(job_info, list) else [job_info]

                # Read resume
                resume_raw = load_resume(temp_path)

                # Generating email
                cold_email = email_gen.generate_email(job_info[0], resume_raw)
                result = cold_email

                os.remove(temp_path) 

            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
