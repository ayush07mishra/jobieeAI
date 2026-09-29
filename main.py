import json

from app.collectors.collector_factory import create_collector
from app.database.database import JobDatabase
from app.filters.job_filter import JobFilter
from app.agent.job_matching_agent import JobMatchingAgent
from app.notifications.telegram import TelegramNotifier
from app.logger import logger


def run_agent():

    logger.info("Job agent started")

    print("\n" + "=" * 60)
    print("🤖 JOB AGENT STARTED")
    print("=" * 60)

    try:

        database = JobDatabase()

        with open(
            "app/filters/user_preferences.json",
            "r",
            encoding="utf-8"
        ) as file:
            preferences = json.load(file)

        job_filter = JobFilter(
            "app/filters/user_preferences.json"
        )

        ai_agent = JobMatchingAgent()

        telegram = TelegramNotifier()

    except Exception as error:

        logger.exception(
            f"Agent initialization failed: {error}"
        )

        print(
            f"❌ Agent initialization failed: {error}"
        )

        return

    total_jobs = 0
    total_new_jobs = 0
    total_ai_checked = 0
    total_matches = 0

    # --------------------------------
    # COMPANY LOOP
    # --------------------------------

    for company in preferences["companies"]:

        company_name = company["name"]

        print(
            f"\n🔎 Checking: {company_name}"
        )

        logger.info(
            f"Checking company: {company_name}"
        )

        # --------------------------------
        # CREATE COLLECTOR
        # --------------------------------

        try:

            collector = create_collector(
                company
            )

            jobs = collector.fetch_jobs()

            logger.info(
                f"{company_name}: "
                f"{len(jobs)} jobs fetched"
            )

        except Exception as error:

            logger.exception(
                f"{company_name} collector failed: {error}"
            )

            print(
                f"❌ Failed to fetch {company_name}"
            )

            continue

        print(
            f"Found {len(jobs)} jobs"
        )

        total_jobs += len(jobs)

        # --------------------------------
        # JOB LOOP
        # --------------------------------

        for job in jobs:

            try:

                # Duplicate check
                if database.job_exists(
                    job.url
                ):
                    continue

                # Save new job
                database.save_job(job)

                total_new_jobs += 1

                logger.info(
                    f"New job found: "
                    f"{job.title} - "
                    f"{job.company}"
                )

                print(
                    f"\n🆕 New job: {job.title}"
                )

                # --------------------------------
                # BASIC FILTER
                # --------------------------------

                if not job_filter.filter_job(
                    job
                ):

                    print(
                        "❌ Failed basic filters"
                    )

                    logger.info(
                        f"Job rejected by "
                        f"basic filters: "
                        f"{job.title}"
                    )

                    continue

                print(
                    "✅ Passed basic filters"
                )

                # --------------------------------
                # AI
                # --------------------------------

                total_ai_checked += 1

                print(
                    "🤖 AI analyzing..."
                )

                try:

                    result = ai_agent.match_job(
                        job,
                        preferences
                    )

                except Exception as error:

                    logger.exception(
                        f"AI failed for "
                        f"{job.title}: {error}"
                    )

                    print(
                        f"❌ AI failed: {error}"
                    )

                    continue

                # --------------------------------
                # AI RESULT
                # --------------------------------

                if result.get("match") is True:

                    total_matches += 1

                    confidence = result.get(
                        "confidence",
                        0
                    )

                    reason = result.get(
                        "reason",
                        ""
                    )

                    message = f"""
🚨 NEW JOB MATCH

🏢 Company: {job.company}

💼 Role: {job.title}

📍 Location: {job.location}

📊 AI Confidence: {confidence}

🤖 Why it matches:
{reason}

🔗 Apply:
{job.url}
"""

                    # --------------------------------
                    # TELEGRAM
                    # --------------------------------

                    try:

                        telegram.send_message(
                            message
                        )

                        logger.info(
                            f"Telegram notification "
                            f"sent for {job.title}"
                        )

                        print(
                            "📱 Telegram notification sent!"
                        )

                    except Exception as error:

                        logger.exception(
                            f"Telegram failed: "
                            f"{error}"
                        )

                        print(
                            f"❌ Telegram failed: "
                            f"{error}"
                        )

                else:

                    logger.info(
                        f"AI rejected: "
                        f"{job.title}"
                    )

                    print(
                        "❌ AI rejected job"
                    )

            except Exception as error:

                logger.exception(
                    f"Unexpected error while "
                    f"processing {job.title}: "
                    f"{error}"
                )

                print(
                    f"❌ Error processing job: "
                    f"{error}"
                )

                continue

    # --------------------------------
    # SUMMARY
    # --------------------------------

    print(
        "\n========== SUMMARY =========="
    )

    print(
        f"Total jobs checked: "
        f"{total_jobs}"
    )

    print(
        f"New jobs: "
        f"{total_new_jobs}"
    )

    print(
        f"Jobs sent to AI: "
        f"{total_ai_checked}"
    )

    print(
        f"AI matching jobs: "
        f"{total_matches}"
    )

    print("=" * 60)

    logger.info(
        f"Agent finished | "
        f"Total={total_jobs}, "
        f"New={total_new_jobs}, "
        f"AI={total_ai_checked}, "
        f"Matches={total_matches}"
    )


if __name__ == "__main__":
    run_agent()