import json
import ollama


class JobMatchingAgent:

    def __init__(self, model="llama3.2"):
        self.model = model

    def match_job(self, job, preferences):

        prompt = f"""
You are a job matching AI agent.

Your task is to determine whether a job matches the user's requirements.

USER REQUIREMENTS:
{json.dumps(preferences, indent=2)}

JOB:
Title: {job.title}
Company: {job.company}
Location: {job.location}
Experience: {job.experience}
Description:
{job.description}

Return ONLY valid JSON in this format:

{{
    "match": true,
    "confidence": 0.0,
    "reason": "short explanation"
}}

Rules:

1. match must be true or false.
2. confidence must be between 0 and 1.
3. Consider job title, responsibilities, skills, experience and location.
4. Do not match a job only because one keyword is present.
5. Be conservative when the job clearly does not match.
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response["message"]["content"]

        try:
            result = json.loads(content)

        except json.JSONDecodeError:
            return {
                "match": False,
                "confidence": 0,
                "reason": "AI returned invalid JSON"
            }

        return result