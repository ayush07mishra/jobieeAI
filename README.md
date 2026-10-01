🤖 JobieeAI - AI Job Alert Agent

An automated personal AI job-search agent that monitors job openings
from selected companies, filters them according to your preferences,
uses an AI model to evaluate relevance, and sends matching jobs directly
to Telegram.

The project is designed as a simple personal automation system. It does
not require a web UI, dashboard, or multi-user backend.

✨ Features

🔎 Automatically collects jobs from supported company career
platforms

🏢 Monitor specific companies

💼 Filter jobs by role/profile

📍 Filter jobs by location

🎓 Filter for fresher and 0--1 year experience opportunities

🧠 Use an AI model to perform deeper job matching

📊 Generate an AI confidence score and matching reason

📱 Send matching jobs directly to Telegram

🗄️ Store discovered jobs using SQLite

⏰ Run automatically every 2 hours with GitHub Actions

📝 Maintain application logs for debugging

🔐 Keep Telegram credentials in GitHub Secrets

🏗️ Architecture

                    ┌─────────────────────┐
                    │   GitHub Actions    │
                    │  Scheduled Runner   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      main.py        │
                    │   Agent Controller  │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
      │ Collectors  │   │ Job Filter  │   │  SQLite DB  │
      │             │   │             │   │             │
      │ Greenhouse  │   │ Company     │   │ jobs.db     │
      │    API      │   │ Role        │   │             │
      └──────┬──────┘   │ Location    │   └─────────────┘
             │          │ Experience  │
             │          └──────┬──────┘
             │                 │
             │                 ▼
             │        ┌─────────────────┐
             └───────►│   AI Matcher    │
                      │    Ollama       │
                      │    Llama 3.2    │
                      └────────┬────────┘
                               │
                               ▼
                      ┌─────────────────┐
                      │    Telegram     │
                      │   Notification  │
                      └─────────────────┘

📁 Project Structure

jobieeAI/
│
├── app/
│   ├── agent/
│   │   └── job_matching_agent.py
│   │
│   ├── collectors/
│   │   ├── base_collector.py
│   │   ├── collector_factory.py
│   │   ├── greenhouse.py
│   │   └── job_model.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── filters/
│   │   ├── job_filter.py
│   │   └── user_preferences.json
│   │
│   ├── notifications/
│   │   └── telegram.py
│   │
│   ├── scheduler/
│   │   └── scheduler.py
│   │
│   └── logger.py
│
├── data/
│   ├── jobs.db
│   └── agent.log
│
├── .github/
│   └── workflows/
│       └── job-agent.yml
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md

🛠️ Tech Stack

Technology         Purpose

Python             Core application
Requests           Job API requests
SQLite             Job storage
Ollama             Local AI inference
Llama 3.2          Job matching model
Telegram Bot API   Notifications
python-dotenv      Environment variables
Schedule           Local periodic execution
GitHub Actions     Automated cloud execution
JSON               User preferences and configuration

🚀 Getting Started

1. Clone the repository

git clone https://github.com/ayush07mishra/jobieeAI.git
cd jobieeAI

2. Create a virtual environment

macOS / Linux

python3 -m venv venv
source venv/bin/activate

Windows

python -m venv venv
venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

🤖 Configure Ollama

This project uses Ollama for local AI job matching.

Install Ollama from the official Ollama website.

Then download the model:

ollama pull llama3.2

Verify the model:

ollama list

You should see:

llama3.2

Start Ollama if it is not already running:

ollama serve

📱 Configure Telegram

1. Create a Telegram bot

Open Telegram and search for:

@BotFather

Create a new bot using:

/newbot

BotFather will provide a bot token.

Keep this token private.

2. Get your Telegram Chat ID

Start a conversation with your bot and send it a message.

Then use Telegram's Bot API getUpdates endpoint to find your chat ID.

Your .env file should contain:

TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

Never commit .env to GitHub.

⚙️ Configure Job Preferences

Edit:

app/filters/user_preferences.json

Example:

{
    "companies": [
        {
            "name": "Airbnb",
            "platform": "greenhouse",
            "board_token": "airbnb"
        }
    ],
    "roles": [
        "AI Engineer",
        "Machine Learning Engineer",
        "Data Scientist",
        "ML Engineer"
    ],
    "locations": [
        "India",
        "Remote"
    ],
    "experience_min": 0,
    "experience_max": 1,
    "skills": [
        "Python",
        "Machine Learning",
        "Artificial Intelligence",
        "TensorFlow",
        "PyTorch"
    ]
}

Preferences

Field              Description

companies        Companies to monitor
roles            Target job profiles
locations        Accepted job locations
experience_min   Minimum experience
experience_max   Maximum experience
skills           Relevant technical skills

🏢 Adding Companies

Companies are configured in:

app/filters/user_preferences.json

Each supported company contains:

{
    "name": "Company Name",
    "platform": "greenhouse",
    "board_token": "company-board-token"
}

Currently, the collector architecture supports the Greenhouse
platform.

Other platforms can be added later by implementing additional collectors
and registering them in:

app/collectors/collector_factory.py

▶️ Run Locally

From the project root:

python main.py

A successful run will look similar to:

============================================================
🤖 JOB AGENT STARTED
============================================================

🔎 Checking: Airbnb
Found 150 jobs

🆕 New job: Machine Learning Engineer
✅ Passed basic filters
🤖 AI analyzing...
📱 Telegram notification sent!

========== SUMMARY ==========
Total jobs checked: 150
New jobs: 10
Jobs sent to AI: 3
AI matching jobs: 1
============================================================

If a job does not match the basic filters, it will be rejected before
the AI step.

🧠 How Job Matching Works

The agent uses two stages.

Stage 1: Basic Filtering

The job is checked against:

Company

Role

Location

Experience

Only jobs that pass the basic filters are sent to the AI model.

This reduces unnecessary AI processing.

Stage 2: AI Matching

The remaining job information is sent to Llama 3.2.

The AI considers:

Job title

Responsibilities

Skills

Experience requirements

Location

User preferences

The model returns:

{
    "match": true,
    "confidence": 0.91,
    "reason": "The role closely matches the requested AI/ML profile and requires Python and machine learning experience."
}

If match is true, the job is sent to Telegram.

📲 Telegram Notification

A matching job is sent in a format similar to:

🚨 NEW JOB MATCH

🏢 Company: Airbnb

💼 Role: Machine Learning Engineer

📍 Location: Remote

📊 AI Confidence: 0.91

🤖 Why it matches:
The role closely matches the requested AI/ML profile.

🔗 Apply:
https://...

☁️ GitHub Actions Automation

The project can run automatically through:

.github/workflows/job-agent.yml

The workflow:

Checks out the repository

Installs Python

Installs dependencies

Installs Ollama

Starts Ollama

Downloads Llama 3.2

Runs main.py

Sends matching jobs to Telegram

The workflow can be triggered manually and is also scheduled to run
every 2 hours.

Example schedule:

schedule:
  - cron: "0 */2 * * *"

🔐 GitHub Secrets

For GitHub Actions, Telegram credentials must be stored as Repository
Secrets.

Go to:

Repository
→ Settings
→ Secrets and variables
→ Actions
→ Repository secrets

Create:

TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID

The workflow passes them to the application:

env:
  TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
  TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}

Do not put Telegram credentials directly inside Python files or workflow
YAML.

🧪 Testing GitHub Actions

To test the automation manually:

GitHub Repository
→ Actions
→ AI Job Agent
→ Run workflow
→ Run workflow

Then open the workflow run and inspect:

Run AI Job Agent

A successful run should not contain:

TELEGRAM_BOT_TOKEN is missing

If a matching job is found, the logs should contain:

📱 Telegram notification sent!

📝 Logging

Application logs are stored in:

data/agent.log

The logger records events such as:

Agent startup

Company checks

Collector errors

New jobs

Filter results

AI failures

Telegram failures

Agent completion

🗄️ Database

The project uses SQLite:

data/jobs.db

The database stores information such as:

Job title

Company

Location

URL

Description

Experience

Posted/updated date

Creation timestamp

The job URL is unique, which allows the application to detect jobs that
have already been stored.

⚠️ Important Deployment Note

GitHub-hosted Actions runners are temporary.

The runner is created for a workflow execution and removed after the
workflow finishes.

Because this project currently uses:

data/jobs.db

you should treat database persistence across separate GitHub Actions
runs as a deployment concern.

If the database is not persisted between runs, the agent can lose its
previous job history and may treat previously seen jobs as new jobs.

A future improvement is to persist job state using a durable storage
mechanism or commit the updated state back to the repository with
appropriate GitHub Actions permissions.

🔮 Future Improvements

Possible future improvements include:

Add Ashby collector

Add Lever collector

Improve semantic role matching

Improve experience extraction

Add job deduplication across deployments

Persist job history between GitHub Actions runs

Improve AI JSON parsing

Add retry handling for APIs

Add more notification formats

Add application tracking

Add additional job sources

🔒 Security

Never commit these files or values:

.env
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
API keys
Private credentials

The .gitignore should contain:

venv/
.env
__pycache__/
*.pyc

Keep all credentials in environment variables or GitHub Secrets.

🧑‍💻 Local Development

The main entry point is:

main.py

The application flow is:

Load preferences
      ↓
Initialize database
      ↓
Load collectors
      ↓
Fetch jobs
      ↓
Check if job already exists
      ↓
Apply basic filters
      ↓
Send suitable jobs to AI
      ↓
AI evaluates job
      ↓
If matched
      ↓
Send Telegram notification

📌 Current Scope

JobieeAI is intentionally designed as a personal automation project
rather than a full job-search platform.

It currently focuses on:

Automated job collection

Personalized filtering

AI-based matching

Telegram alerts

Scheduled execution

There is no:

Web dashboard

Frontend

User authentication

Multi-user system

Paid API requirement for the core AI matching flow

👨‍💻 Author

Ayush Mishra

B.Tech in Computer Science - Data Science

GitHub: @ayush07mishra

⭐ Project Goal

The goal of JobieeAI is simple:

Find relevant job opportunities automatically and send only the jobs
that match my requirements to Telegram.

Instead of repeatedly searching multiple company career pages, the agent
handles the repetitive monitoring and matching process automatically.
