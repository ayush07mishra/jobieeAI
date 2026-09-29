import logging
import os


os.makedirs("data", exist_ok=True)


logging.basicConfig(
    filename="data/agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


logger = logging.getLogger("job-agent")