from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)


UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


os.makedirs(UPLOAD_FOLDER, exist_ok=True)


required_skills = [
    "python",
    "c++",
    "java",
    "html",
    "css",
    "javascript",
    "sql",
    "git",
    "flask",
    "data structures"
]



def extract_text(pdf_path):
    text = ""

    try:
        reader = PdfReader(pdf_path)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text.lower()

    except Exception as e:
        print("PDF Error:", e)

    return text


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        
        if "resume" not in request.files:
            return "No file uploaded"

        file = request.files["resume"]

        if file.filename == "":
            return "Please select a PDF file"

     
        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        print("File saved successfully")

        resume_text = extract_text(filepath)

        print("Text extracted successfully")

        found_skills = []
        missing_skills = []

        for skill in required_skills:
            if skill.lower() in resume_text:
                found_skills.append(skill)
            else:
                missing_skills.append(skill)

     
        score = round(
            (len(found_skills) / len(required_skills)) * 100
        )

       
        return render_template(
            "result.html",
            score=score,
            found_skills=found_skills,
            missing_skills=missing_skills
        )

    except Exception as e:
        return f"<h2>Error:</h2><p>{str(e)}</p>"


if __name__ == "__main__":
    app.run(debug=True, port=5001)