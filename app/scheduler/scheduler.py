import schedule
import time
from main import run_agent


def start_scheduler():

    # Run every 2 hours
    schedule.every(2).hours.do(run_agent)

    print("🤖 Job Agent started...")
    print("⏰ Checking for new jobs every 2 hours.")

    # Run once immediately
    run_agent()

    while True:
        schedule.run_pending()
        time.sleep(60)