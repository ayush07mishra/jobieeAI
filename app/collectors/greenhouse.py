import requests

from app.collectors.base_collector import BaseCollector
from app.collectors.job_model import Job


class GreenhouseCollector(BaseCollector):

    def __init__(self, company_name, board_token):
        self.company_name = company_name
        self.board_token = board_token

        self.url = (
            f"https://boards-api.greenhouse.io/v1/boards/"
            f"{board_token}/jobs?content=true"
        )

    def fetch_jobs(self):

        response = requests.get(
            self.url,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        jobs = []

        for item in data.get("jobs", []):

            location = item.get(
                "location",
                {}
            ).get(
                "name",
                ""
            )

            job = Job(
                title=item.get("title", ""),
                company=self.company_name,
                location=location,
                url=item.get("absolute_url", ""),
                description=item.get("content", ""),
                experience=None,
                posted_date=item.get("updated_at", "")
            )

            jobs.append(job)

        return jobs