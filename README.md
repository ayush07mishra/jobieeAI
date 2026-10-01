# 🤖 JobieeAI

> An AI-powered personal job alert agent that automatically finds relevant job openings, evaluates them against your preferences, and sends matching opportunities directly to Telegram.

## 📌 Overview

**JobieeAI** is a personal AI job-search automation system built with Python.

Instead of manually checking multiple company career pages every day, JobieeAI automatically:

- Collects job openings from selected companies
- Filters jobs based on preferred roles, locations, experience, and skills
- Uses AI to evaluate job relevance
- Generates an AI confidence score and explanation
- Sends matching jobs directly to Telegram
- Runs automatically using GitHub Actions

The project is designed as a **personal automation agent** without a web dashboard, frontend, authentication system, or multi-user architecture.

---

## ✨ Features

- 🔎 Automated job collection
- 🏢 Monitor selected companies
- 💼 Role-based filtering
- 📍 Location-based filtering
- 🎓 Fresher / 0–1 year experience filtering
- 🛠️ Skill-based filtering
- 🧠 AI-powered job matching
- 📊 AI confidence score
- 💬 AI-generated matching explanation
- 📱 Telegram notifications
- 🗄️ SQLite job storage
- 📝 Application logging
- ⏰ Scheduled execution
- ☁️ GitHub Actions automation
- 🔐 Secure Telegram credentials using GitHub Secrets
- 🆓 Local AI inference using Ollama

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │    GitHub Actions    │
                         │   Scheduled Runner   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       main.py        │
                         │   Agent Controller   │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐  ┌────────────────┐  ┌───────────────┐
        │   Collectors   │  │  Job Filters   │  │    SQLite     │
        │                │  │                │  │   Database    │
        │   Greenhouse   │  │ Company        │  │   jobs.db     │
        │      API       │  │ Role           │  │               │
        └───────┬────────┘  │ Location       │  └───────────────┘
                │           │ Experience     │
                │           └───────┬────────┘
                │                   │
                └───────────────────▼
                            ┌────────────────┐
                            │   AI Matcher   │
                            │    Ollama      │
                            │   Llama 3.2    │
                            └───────┬────────┘
                                    │
                                    ▼
                            ┌────────────────┐
                            │    Telegram    │
                            │  Notification  │
                            └────────────────┘
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Requests | Job API requests |
| SQLite | Job storage |
| Ollama | Local AI inference |
| Llama 3.2 | AI job matching |
| Telegram Bot API | Job notifications |
| python-dotenv | Environment variables |
| Schedule | Local scheduled execution |
| GitHub Actions | Automated execution |
| JSON | User preferences |

---

# 📁 Project Structure

```text
jobieeAI/
│
├── app/
│   │
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
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/ayush07mishra/jobieeAI.git
cd jobieeAI
```

---

## 2. Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Ollama Setup

JobieeAI uses **Ollama** to run the AI model locally.

Install Ollama and download the model:

```bash
ollama pull llama3.2
```

Verify the model:

```bash
ollama list
```

You should see:

```text
llama3.2
```

If Ollama is not already running:

```bash
ollama serve
```

---

# 📱 Telegram Setup

JobieeAI sends matching jobs directly to Telegram.

## 1. Create a Telegram Bot

Open Telegram and search for:

```text
@BotFather
```

Run:

```text
/newbot
```

Follow the instructions to create your bot.

BotFather will provide a bot token.

Keep this token private.

---

## 2. Get Your Chat ID

Start a conversation with your Telegram bot and send it a message.

Use Telegram's Bot API to retrieve your chat ID.

You will need:

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

Your project should look like:

```text
jobieeAI/
├── .env
├── main.py
├── requirements.txt
└── ...
```

### ⚠️ Important

Never commit your `.env` file to GitHub.

Your `.gitignore` should contain:

```gitignore
venv/
.env
__pycache__/
*.pyc
```

---

# ⚙️ Configure Job Preferences

Edit:

```text
app/filters/user_preferences.json
```

Example:

```json
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
```

---

# 🎯 User Preferences

The following configuration controls which jobs are considered relevant.

| Field | Description |
|---|---|
| `companies` | Companies to monitor |
| `roles` | Target job profiles |
| `locations` | Preferred locations |
| `experience_min` | Minimum experience |
| `experience_max` | Maximum experience |
| `skills` | Relevant technical skills |

Example:

```json
"experience_min": 0,
"experience_max": 1
```

This configures the agent to target opportunities suitable for candidates with approximately 0–1 year of experience.

---

# 🏢 Adding Companies

Companies are configured inside:

```text
app/filters/user_preferences.json
```

For a Greenhouse company:

```json
{
    "name": "Company Name",
    "platform": "greenhouse",
    "board_token": "company-board-token"
}
```

Example:

```json
{
    "name": "Airbnb",
    "platform": "greenhouse",
    "board_token": "airbnb"
}
```

The collector architecture is designed so additional job platforms can be added later.

Currently implemented:

```text
Greenhouse
```

Additional platforms such as Ashby or Lever can be added by implementing their respective collectors.

---

# ▶️ Run the Agent Locally

Make sure Ollama is running and your Telegram configuration is present.

Run:

```bash
python main.py
```

Example output:

```text
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
```

---

# 🧠 How Job Matching Works

JobieeAI uses a two-stage matching system.

## Stage 1: Basic Filtering

Jobs are first checked against:

```text
Company
   ↓
Role
   ↓
Location
   ↓
Experience
```

Only jobs that pass the basic filters are sent to the AI model.

This reduces unnecessary AI processing.

---

## Stage 2: AI Matching

The filtered job is sent to the local Llama 3.2 model through Ollama.

The AI considers:

- Job title
- Job responsibilities
- Required skills
- Experience requirements
- Location
- User preferences

The AI returns structured information such as:

```json
{
    "match": true,
    "confidence": 0.91,
    "reason": "The role matches the requested AI/ML profile and requires relevant Python and machine learning skills."
}
```

If:

```text
match = true
```

the job is sent to Telegram.

---

# 📲 Telegram Notification

A matching job looks similar to:

```text
🚨 NEW JOB MATCH

🏢 Company: Airbnb

💼 Role: Machine Learning Engineer

📍 Location: Remote

📊 AI Confidence: 0.91

🤖 Why it matches:
The role matches the requested AI/ML profile and
requires relevant Python and machine learning skills.

🔗 Apply:
https://example.com/job
```

---

# ☁️ GitHub Actions

JobieeAI can run automatically using GitHub Actions.

Workflow file:

```text
.github/workflows/job-agent.yml
```

The workflow performs:

```text
Checkout Repository
        ↓
Setup Python
        ↓
Install Dependencies
        ↓
Install Ollama
        ↓
Start Ollama
        ↓
Download Llama 3.2
        ↓
Run main.py
        ↓
Send Telegram Notifications
```

The workflow is configured to run automatically every **2 hours**.

Example:

```yaml
schedule:
  - cron: "0 */2 * * *"
```

The workflow can also be triggered manually.

---

# 🧪 Test GitHub Actions

To manually test the automation:

```text
GitHub Repository
        ↓
Actions
        ↓
AI Job Agent
        ↓
Run workflow
        ↓
Run workflow
```

Open the latest workflow run.

Then open:

```text
Run AI Job Agent
```

A successful run should show logs similar to:

```text
🤖 JOB AGENT STARTED

🔎 Checking: Airbnb
Found 150 jobs

✅ Passed basic filters
🤖 AI analyzing...

📱 Telegram notification sent!
```

---

# 🔑 GitHub Secrets

When running the agent through GitHub Actions, Telegram credentials should be stored as **Repository Secrets**.

Go to:

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
→ Repository secrets
```

Add:

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

The workflow uses them as environment variables:

```yaml
env:
  TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
  TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
```

Never put the actual Telegram token inside:

- Python files
- README.md
- GitHub Actions YAML
- user_preferences.json

---

# 🗄️ Database

JobieeAI uses SQLite to store discovered jobs.

Database:

```text
data/jobs.db
```

The database stores information including:

- Job title
- Company
- Location
- URL
- Description
- Experience
- Posted/updated date
- Creation timestamp

The job URL is stored as a unique value so the application can identify jobs that have already been saved.

---

# 📝 Logging

Application logs are stored in:

```text
data/agent.log
```

The logger records:

- Agent startup
- Company checks
- Jobs fetched
- New jobs
- Filter results
- AI processing
- AI failures
- Telegram notifications
- Telegram failures
- Collector errors
- Agent completion

---

# 🔄 Complete Workflow

```text
Start Agent
     ↓
Load User Preferences
     ↓
Initialize Database
     ↓
Load Company Collector
     ↓
Fetch Jobs
     ↓
Check Existing Job
     ↓
New Job?
     │
     ├── No → Skip
     │
     └── Yes
          ↓
     Basic Filters
          ↓
     Company
          ↓
     Role
          ↓
     Location
          ↓
     Experience
          ↓
     Passed?
       │
       ├── No → Reject
       │
       └── Yes
            ↓
        AI Analysis
            ↓
      Relevant Job?
         │
         ├── No → Reject
         │
         └── Yes
              ↓
       Generate Match
              ↓
       Send to Telegram
```

---

# 📊 Example

Suppose your preferences are:

```text
Role:
Machine Learning Engineer

Location:
India / Remote

Experience:
0–1 year

Skills:
Python
Machine Learning
TensorFlow
PyTorch
```

The agent might find:

```text
Machine Learning Engineer
India
0–2 years
Python
TensorFlow
```

The job passes the initial filters and is sent to the AI matcher.

The AI evaluates the complete job description instead of relying only on a single keyword.

If the AI determines that the job is relevant:

```json
{
    "match": true
}
```

the job is sent to Telegram.

---

# 🔒 Security

Never commit sensitive credentials.

Do not commit:

```text
.env
Telegram Bot Token
API Keys
Passwords
Private Credentials
```

For local development use:

```text
.env
```

For GitHub Actions use:

```text
GitHub Repository Secrets
```

---

# ⚠️ Deployment Consideration

GitHub-hosted Actions runners are temporary.

Each scheduled workflow starts on a fresh runner.

Because the project currently uses:

```text
data/jobs.db
```

job history needs to be persisted properly between separate GitHub Actions executions.

Without persistent storage, a future workflow run may not have the database state from the previous run and could treat previously seen jobs as new jobs.

A future improvement is to use persistent storage or another reliable state-management mechanism for scheduled executions.

---

# 🔮 Future Improvements

- [ ] Add Ashby collector
- [ ] Add Lever collector
- [ ] Improve semantic role matching
- [ ] Improve experience extraction
- [ ] Improve duplicate detection
- [ ] Persist job history between GitHub Actions runs
- [ ] Improve AI JSON parsing
- [ ] Add API retry mechanisms
- [ ] Add more job sources
- [ ] Add application tracking
- [ ] Add job priority levels
- [ ] Add daily job summaries
- [ ] Add Telegram commands for changing preferences

---

# 📌 Project Scope

JobieeAI is intentionally designed as a **personal job automation agent**.

It does not currently include:

- ❌ Web dashboard
- ❌ Frontend
- ❌ User authentication
- ❌ Multi-user architecture
- ❌ Paid AI API requirement for core matching

The main focus is:

```text
Job Collection
      ↓
Personalized Filtering
      ↓
AI Matching
      ↓
Telegram Alerts
      ↓
Automated Execution
```

---

# 💡 Why JobieeAI?

Searching for jobs manually across multiple company career pages can be repetitive.

JobieeAI automates the repetitive part while keeping the user in control of the actual application.

The agent finds opportunities, evaluates their relevance, and sends the information to Telegram so the user can decide whether to apply.

---

# 👨‍💻 Author

**Ayush Mishra**

B.Tech in Computer Science - Data Science

GitHub:  
https://github.com/ayush07mishra

---

# ⭐ Project Goal

> **Automatically find relevant job opportunities and send only the jobs that match my requirements to Telegram.**

JobieeAI turns repetitive job searching into an automated personal workflow.
