import json
import re


class JobFilter:
    def __init__(self, preferences_file):
        with open(preferences_file, "r", encoding="utf-8") as file:
            self.preferences = json.load(file)

    # ---------------------------------------------------------
    # COMPANY FILTER
    # ---------------------------------------------------------
    def company_matches(self, job):
        companies = self.preferences["companies"]

        allowed_companies = [
            company["name"].lower()
            for company in companies
        ]

        return job.company.lower() in allowed_companies

    # ---------------------------------------------------------
    # ROLE FILTER
    # ---------------------------------------------------------
    def role_matches(self, job):
        title = job.title.lower().strip()

        # Explicit senior / leadership roles to reject
        senior_keywords = [
            "senior",
            "sr.",
            "sr ",
            "staff",
            "principal",
            "lead",
            "manager",
            "director",
            "head of",
            "architect",
            "vice president",
            "vp "
        ]

        for keyword in senior_keywords:
            if keyword in title:
                return False

        # Roles we want
        allowed_role_keywords = [
            # AI / ML
            "ai engineer",
            "ai/ml engineer",
            "artificial intelligence engineer",
            "machine learning engineer",
            "ml engineer",
            "applied ai engineer",
            "generative ai engineer",
            "genai engineer",
            "nlp engineer",
            "natural language processing engineer",
            "computer vision engineer",

            # Data
            "data scientist",
            "data science engineer",

            # Software Engineering
            "software engineer",
            "software development engineer",
            "swe",

            # Junior / Graduate
            "junior engineer",
            "associate engineer",
            "graduate engineer",
            "entry level engineer",
            "entry-level engineer",
            "new graduate engineer",

            # Internships
            "ai engineer intern",
            "ai/ml intern",
            "artificial intelligence intern",
            "machine learning intern",
            "ml intern",
            "data science intern",
            "software engineer intern",
            "software development engineer intern",
            "swe intern",
            "generative ai intern",
            "genai intern",
            "nlp intern",
            "computer vision intern"
        ]

        for role in allowed_role_keywords:
            if role in title:
                return True

        return False

    # ---------------------------------------------------------
    # LOCATION FILTER
    # ---------------------------------------------------------
    def location_matches(self, job):
        locations = self.preferences["locations"]
        job_location = (job.location or "").lower()

        for location in locations:
            if location.lower() in job_location:
                return True

        return False

    # ---------------------------------------------------------
    # EXPERIENCE FILTER
    # ---------------------------------------------------------
    def experience_matches(self, job):
        max_experience = self.preferences["experience_max"]

        text = ""

        if job.experience:
            text += " " + job.experience.lower()

        if job.description:
            text += " " + job.description.lower()

        # -----------------------------------------------------
        # Reject seniority keywords
        # -----------------------------------------------------
        senior_keywords = [
            "senior",
            "sr.",
            "sr ",
            "staff engineer",
            "principal engineer",
            "lead engineer",
            "engineering manager",
            "technical manager",
            "director",
            "architect"
        ]

        for keyword in senior_keywords:
            if keyword in text:
                return False

        # -----------------------------------------------------
        # Accept explicit fresher / entry-level descriptions
        # -----------------------------------------------------
        fresher_keywords = [
            "fresher",
            "freshers",
            "entry level",
            "entry-level",
            "no experience required",
            "no prior experience",
            "recent graduate",
            "recent graduates",
            "new graduate",
            "new graduates",
            "graduate role",
            "graduate program",
            "graduate programme",
            "early career",
            "early-career",
            "0 years",
            "0 year",
            "0-1 year",
            "0 - 1 year",
            "0 to 1 year",
            "0–1 year",
            "internship",
            "intern"
        ]

        for keyword in fresher_keywords:
            if keyword in text:
                return True

        # -----------------------------------------------------
        # Detect ranges such as:
        #
        # 0-1 years
        # 1-2 years
        # 2-4 years
        # 0 to 1 years
        # -----------------------------------------------------
        range_patterns = [
            r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*\+?\s*years?",
            r"(\d+(?:\.\d+)?)\s+to\s+(\d+(?:\.\d+)?)\s*years?"
        ]

        for pattern in range_patterns:
            matches = re.findall(pattern, text)

            for minimum, maximum in matches:
                minimum = float(minimum)
                maximum = float(maximum)

                # Accept only ranges whose minimum is within
                # the user's maximum experience requirement.
                if minimum <= max_experience and maximum <= max_experience:
                    return True

                # Reject ranges such as 2-3, 3-5, etc.
                if minimum > max_experience:
                    return False

        # -----------------------------------------------------
        # Detect:
        #
        # 1+ years
        # 2+ years
        # 3+ years
        # -----------------------------------------------------
        plus_pattern = r"(\d+(?:\.\d+)?)\s*\+\s*years?"

        plus_matches = re.findall(plus_pattern, text)

        for years in plus_matches:
            years = float(years)

            if years <= max_experience:
                return True

            return False

        # -----------------------------------------------------
        # Detect:
        #
        # 1 year of experience
        # 2 years of experience
        # etc.
        # -----------------------------------------------------
        single_pattern = (
            r"(\d+(?:\.\d+)?)\s+years?\s+"
            r"(?:of\s+)?experience"
        )

        single_matches = re.findall(single_pattern, text)

        for years in single_matches:
            years = float(years)

            if years <= max_experience:
                return True

            return False

        # -----------------------------------------------------
        # If the job is explicitly an internship, allow it.
        # -----------------------------------------------------
        if "intern" in job.title.lower():
            return True

        # -----------------------------------------------------
        # IMPORTANT:
        #
        # If experience cannot be determined, do NOT
        # automatically accept the job.
        #
        # This prevents unknown/senior jobs from passing.
        # -----------------------------------------------------
        return False

    # ---------------------------------------------------------
    # SKILL MATCHING
    # ---------------------------------------------------------
    def skills_match(self, job):
        skills = self.preferences["skills"]

        text = f"{job.title} {job.description or ''}".lower()

        matched_skills = []

        for skill in skills:
            if skill.lower() in text:
                matched_skills.append(skill)

        return matched_skills

    # ---------------------------------------------------------
    # FINAL FILTER
    # ---------------------------------------------------------
    def filter_job(self, job):

        # 1. Company
        if not self.company_matches(job):
            return False

        # 2. Role
        if not self.role_matches(job):
            return False

        # 3. Location
        if not self.location_matches(job):
            return False

        # 4. Experience
        if not self.experience_matches(job):
            return False

        return True


# import json
# import re


# class JobFilter:

#     def __init__(self, preferences_file):

#         with open(
#             preferences_file,
#             "r",
#             encoding="utf-8"
#         ) as file:
#             self.preferences = json.load(file)

#     # -------------------------
#     # COMPANY
#     # -------------------------

#     def company_matches(self, job):
#         companies = self.preferences["companies"]
#         allowed_companies = [
#             company["name"].lower()
#             for company in companies
#             ]
#         return job.company.lower() in allowed_companies

#     # -------------------------
#     # ROLE
#     # -------------------------

#     def role_matches(self, job):

#         roles = self.preferences["roles"]

#         title = job.title.lower()

#         for role in roles:

#             if role.lower() in title:
#                 return True

#         return False

#     # -------------------------
#     # LOCATION
#     # -------------------------

#     def location_matches(self, job):

#         locations = self.preferences["locations"]

#         job_location = job.location.lower()

#         for location in locations:

#             if location.lower() in job_location:
#                 return True

#         return False

#     # -------------------------
#     # EXPERIENCE
#     # -------------------------

#     def experience_matches(self, job):

#         max_experience = self.preferences[
#             "experience_max"
#         ]

#         text = ""

#         if job.experience:
#             text += job.experience.lower()

#         if job.description:
#             text += " " + job.description.lower()

#         # Freshers / entry level
#         fresher_keywords = [
#             "fresher",
#             "freshers",
#             "entry level",
#             "entry-level",
#             "no experience required",
#             "recent graduate",
#             "recent graduates",
#             "graduate role",
#             "new graduate"
#         ]

#         for keyword in fresher_keywords:

#             if keyword in text:
#                 return True

#         # Examples:
#         # 0-1 years
#         # 0 - 2 years
#         # 1+ years
#         # 2 years experience

#         ranges = re.findall(
#             r"(\d+(?:\.\d+)?)\s*[-to]+\s*(\d+(?:\.\d+)?)\s*years?",
#             text
#         )

#         for minimum, maximum in ranges:

#             minimum = float(minimum)
#             maximum = float(maximum)

#             if minimum <= max_experience:
#                 return True

#         # Example:
#         # "1+ years"
#         plus_years = re.findall(
#             r"(\d+(?:\.\d+)?)\s*\+\s*years?",
#             text
#         )

#         for years in plus_years:

#             years = float(years)

#             if years <= max_experience:
#                 return True

#         # Example:
#         # "2 years of experience"
#         single_years = re.findall(
#             r"(\d+(?:\.\d+)?)\s+years?\s+(?:of\s+)?experience",
#             text
#         )

#         for years in single_years:

#             years = float(years)

#             if years <= max_experience:
#                 return True

#         # If no experience information is available,
#         # let the AI make the final decision.
#         return True

#     # -------------------------
#     # SKILLS
#     # -------------------------

#     def skills_match(self, job):

#         skills = self.preferences["skills"]

#         text = (
#             f"{job.title} "
#             f"{job.description or ''}"
#         ).lower()

#         matched_skills = []

#         for skill in skills:

#             if skill.lower() in text:
#                 matched_skills.append(skill)

#         return matched_skills

#     # -------------------------
#     # FINAL FILTER
#     # -------------------------

#     def filter_job(self, job):

#         if not self.company_matches(job):
#             return False

#         if not self.role_matches(job):
#             return False

#         if not self.location_matches(job):
#             return False

#         if not self.experience_matches(job):
#             return False

#         return True
