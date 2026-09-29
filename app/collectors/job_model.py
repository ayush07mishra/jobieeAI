from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    title: str
    company: str
    location: str
    url: str
    description: Optional[str] = None
    experience: Optional[str] = None
    posted_date: Optional[str] = None

    def to_dict(self):
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "url": self.url,
            "description": self.description,
            "experience": self.experience,
            "posted_date": self.posted_date
        }