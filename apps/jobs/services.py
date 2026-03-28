def calculate_match_score(resume_data, job_skills):
    resume_skills = resume_data.get("skills", [])

    matched = [skill for skill in job_skills if skill.lower() in resume_skills]
    missing = [skill for skill in job_skills if skill.lower() not in resume_skills]

    score = int((len(matched) / len(job_skills)) * 100) if job_skills else 0

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
    }