def calculate_ats_score(text):

    score = 0
    suggestions = []

    technical_skills = [
        "python",
        "java",
        "sql",
        "dbms",
        "dsa",
        "react",
        "javascript",
        "machine learning",
        "cloud computing",
        "power bi",
        "iot"
    ]

    found_skills = 0

    for skill in technical_skills:

        if skill in text.lower():
            found_skills += 1

    if found_skills >= 5:
        score += 30
    else:
        suggestions.append(
            "Add more technical skills."
        )

    if "internship" in text.lower():
        score += 20
    else:
        suggestions.append(
            "Add internship experience."
        )

    if "project" in text.lower():
        score += 20
    else:
        suggestions.append(
            "Add academic or personal projects."
        )

    if (
        "certification" in text.lower()
        or "certificate" in text.lower()
    ):
        score += 15
    else:
        suggestions.append(
            "Add certifications."
        )

    if (
        "@" in text
        and (
            "+91" in text
            or "phone" in text.lower()
            or "mobile" in text.lower()
        )
    ):
        score += 15
    else:
        suggestions.append(
            "Add proper contact details."
        )

    return {
        "score": score,
        "suggestions": suggestions
    }