import PyPDF2
from ats_analyzer import calculate_ats_score


KNOWN_SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "DBMS",
    "DSA",
    "OOP",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "FastAPI",
    "Operating Systems",
    "Computer Networks",
    "Machine Learning",
    "Artificial Intelligence",
    "Cloud Computing",
    "System Design",
    "Power BI",
    "IoT",
    "Embedded Systems",
    "API Development"
]


def analyze_resume(file_path):

    text = ""

    with open(file_path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    found_skills = []

    for skill in KNOWN_SKILLS:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    ats_result = calculate_ats_score(text)

    return {
        "skills": found_skills,
        "score": ats_result["score"],
        "suggestions": ats_result["suggestions"]
    }