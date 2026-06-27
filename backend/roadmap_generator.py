from company_data import companies


def generate_roadmap(company_name, user_skills):

    company = companies.get(company_name)

    if not company:

        return {
            "error": "Company not found"
        }

    required_skills = company["skills"]

    missing_skills = []

    for skill in required_skills:

        found = False

        for user_skill in user_skills:

            if skill.lower() == user_skill.lower():
                found = True
                break

        if not found:
            missing_skills.append(skill)

    roadmap = []

    for index, skill in enumerate(missing_skills, start=1):

        roadmap.append(
            f"Week {index}: Learn {skill}"
        )

    return {
        "missing_skills": missing_skills,
        "roadmap": roadmap,
        "aptitude": company["aptitude"],
        "hr_questions": company["hr_questions"],
        "mock_interview": company["mock_interview"]
    }