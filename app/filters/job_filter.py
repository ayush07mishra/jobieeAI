import json
import re


class JobFilter:

    def __init__(self, preferences_file):

        with open(
            preferences_file,
            "r",
            encoding="utf-8"
        ) as file:
            self.preferences = json.load(file)

    # -------------------------
    # COMPANY
    # -------------------------

    def company_matches(self, job):
        companies = self.preferences["companies"]
        allowed_companies = [
            company["name"].lower()
            for company in companies
            ]
        return job.company.lower() in allowed_companies

    # -------------------------
    # ROLE
    # -------------------------

    def role_matches(self, job):

        roles = self.preferences["roles"]

        title = job.title.lower()

        for role in roles:

            if role.lower() in title:
                return True

        return False

    # -------------------------
    # LOCATION
    # -------------------------

    def location_matches(self, job):

        locations = self.preferences["locations"]

        job_location = job.location.lower()

        for location in locations:

            if location.lower() in job_location:
                return True

        return False

    # -------------------------
    # EXPERIENCE
    # -------------------------

    def experience_matches(self, job):

        max_experience = self.preferences[
            "experience_max"
        ]

        text = ""

        if job.experience:
            text += job.experience.lower()

        if job.description:
            text += " " + job.description.lower()

        # Freshers / entry level
        fresher_keywords = [
            "fresher",
            "freshers",
            "entry level",
            "entry-level",
            "no experience required",
            "recent graduate",
            "recent graduates",
            "graduate role",
            "new graduate"
        ]

        for keyword in fresher_keywords:

            if keyword in text:
                return True

        # Examples:
        # 0-1 years
        # 0 - 2 years
        # 1+ years
        # 2 years experience

        ranges = re.findall(
            r"(\d+(?:\.\d+)?)\s*[-to]+\s*(\d+(?:\.\d+)?)\s*years?",
            text
        )

        for minimum, maximum in ranges:

            minimum = float(minimum)
            maximum = float(maximum)

            if minimum <= max_experience:
                return True

        # Example:
        # "1+ years"
        plus_years = re.findall(
            r"(\d+(?:\.\d+)?)\s*\+\s*years?",
            text
        )

        for years in plus_years:

            years = float(years)

            if years <= max_experience:
                return True

        # Example:
        # "2 years of experience"
        single_years = re.findall(
            r"(\d+(?:\.\d+)?)\s+years?\s+(?:of\s+)?experience",
            text
        )

        for years in single_years:

            years = float(years)

            if years <= max_experience:
                return True

        # If no experience information is available,
        # let the AI make the final decision.
        return True

    # -------------------------
    # SKILLS
    # -------------------------

    def skills_match(self, job):

        skills = self.preferences["skills"]

        text = (
            f"{job.title} "
            f"{job.description or ''}"
        ).lower()

        matched_skills = []

        for skill in skills:

            if skill.lower() in text:
                matched_skills.append(skill)

        return matched_skills

    # -------------------------
    # FINAL FILTER
    # -------------------------

    def filter_job(self, job):

        if not self.company_matches(job):
            return False

        if not self.role_matches(job):
            return False

        if not self.location_matches(job):
            return False

        if not self.experience_matches(job):
            return False

        return True