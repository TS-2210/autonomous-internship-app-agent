import json

sample_jobs = [
    {
        "title": "Data Analyst Intern",
        "location": "London",
        "skills": ["Python", "Statistics", "Machine Learning", "Linear Algebra"]
    },
    {
        "title": "Investment Banking Summer Analyst",
        "location": "Manchester",
        "skills": ["Excel", "Financial Modelling", "Valuation", "PowerPoint"]
    }
]

sample_skills = ["Python", "Machine Learning", "Statistics", "PowerPoint", "Linear Algebra"]

def search_jobs(query, memory):
    query_words = query.lower().split()
    results = []
    for job in sample_jobs:
        job_title_words = job["title"].lower()
        if any(word in job_title_words for word in query_words):
            results.append(job)
    for job in results:
        memory.insert_job(job)
    return results

def analyse_job(job):
    return job["skills"]

def match_skills(job_skills):
    matched = [skill for skill in job_skills if skill in sample_skills]
    missing = [skill for skill in job_skills if skill not in sample_skills]
    return {
        "matched_skills": matched,
        "missing_skills": missing
    }