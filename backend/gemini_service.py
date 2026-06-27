import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("models/gemini-2.5-flash")


def generate_ai_roadmap(company, skills):

    prompt = f"""
Generate a PROFESSIONAL placement preparation report for {company}.

Student Skills:
{skills}

STRICT INSTRUCTIONS:

• Use a clean, professional report format.

• Use ONLY Roman numerals for major sections:
I, II, III, IV, V, VI

• Use bullet points (•) for subtopics.

• Use numbering:
1), 2), 3) for questions.

• DO NOT use:
#, ##, ###, *, **, Markdown tables.

• Keep explanations concise.

• Avoid long paragraphs.

• Maximum output length:
3–4 PDF pages.

• Avoid unnecessary repetition.

• Make the report suitable for direct PDF generation.

------------------------------------------------------------

I. Four-Week Preparation Roadmap

Generate a concise roadmap.

Week I – Fundamentals

Include:

• Technical Preparation
• Aptitude Preparation
• HR Preparation
• Daily Goals

Week II – Problem Solving

Include:

• Coding Practice
• DSA Problems
• Aptitude Practice
• Communication Skills

Week III – Projects and Revision

Include:

• Technical Revision
• Mini Projects
• Interview Preparation

Week IV – Final Preparation

Include:

• Mock Interviews
• HR Revision
• Final Technical Revision

Keep each week within 4–5 bullet points only.

------------------------------------------------------------

II. Technical Topics to Master

Based on:

{skills}

For each important skill provide:

• Important Concepts
• Interview Focus Areas
• Practice Suggestions

Keep explanations short.

Maximum:
5 technologies only.

------------------------------------------------------------

III. Beginner-Friendly Projects

Generate ONLY TWO projects.

For each project:

Project I

• Title
• Objective
• Technologies Used
• Key Features
• Skills Demonstrated
• Relevance to {company}

Project II

• Title
• Objective
• Technologies Used
• Key Features
• Skills Demonstrated
• Relevance to {company}

Keep each project within 6 bullet points.

------------------------------------------------------------

IV. Aptitude Preparation

Generate EXACTLY 10 aptitude questions.

Format:

1)

Question:

Answer:

Short Explanation:

Keep explanations within 2 lines.

------------------------------------------------------------

V. HR Interview Preparation

First provide:

Professional HR Tips

Generate ONLY 5 tips.

Then generate EXACTLY 10 HR interview questions.

Format:

1)

Question:

Sample Answer:

Sample answers should be suitable for freshers.

Maximum 4 lines per answer.

------------------------------------------------------------

VI. Mock Technical Interview Questions

Generate EXACTLY 10 technical questions.

Questions must be based on:

{skills}

Format:

1)

Question:

Answer:

Short Explanation:

Keep explanations short.

------------------------------------------------------------

FINAL RULES:

• Professional language only.

• Roman numerals only.

• Bullet points only.

• No Markdown symbols.

• No duplicate headings.

• No extra sections.

• No large paragraphs.

• PDF-friendly formatting.

• Concise and placement-oriented content only.
"""

    response = model.generate_content(prompt)

    return response.text