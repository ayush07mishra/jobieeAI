import sqlite3
from app.collectors.job_model import Job


class JobDatabase:

    def __init__(self, db_path="data/jobs.db"):
        self.db_path = db_path
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_table(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                url TEXT UNIQUE NOT NULL,
                description TEXT,
                experience TEXT,
                posted_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()
        connection.close()

    def job_exists(self, url):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM jobs WHERE url = ?",
            (url,)
        )

        result = cursor.fetchone()

        connection.close()

        return result is not None

    def save_job(self, job: Job):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO jobs
            (title, company, location, url, description, experience, posted_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            job.title,
            job.company,
            job.location,
            job.url,
            job.description,
            job.experience,
            job.posted_date
        ))

        connection.commit()
        connection.close()

    def get_all_jobs(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT title, company, location, url, posted_date
            FROM jobs
            ORDER BY id DESC
        """)

        jobs = cursor.fetchall()

        connection.close()

        return jobs