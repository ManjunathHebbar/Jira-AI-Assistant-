Jira AI Assistant 🚀

An AI-powered Jira automation system that automatically:

Translates multilingual Jira tickets
Generates AI issue summaries
Detects customer sentiment
Summarizes comments
Updates Jira tickets automatically
Runs fully locally using Ollama (No paid APIs)

Built using:

Python
FastAPI
Ollama
SQLite
Jira REST API
ngrok
Features
✅ AI Ticket Summarization

Automatically generates:

English title
Short summary
Root cause
Suggested fix
Priority
✅ Multilingual Translation

Supports tickets written in:

Chinese
French
German
Hindi
Japanese
Spanish
etc.

Automatically translates them into English.

✅ Comment Summarization

Long Jira discussions become:

concise
actionable
easy to handoff
✅ Sentiment Analysis

Detects customer tone:

Positive
Neutral
Frustrated
Escalated
Angry
✅ Fully Local AI (Privacy Safe)

Uses:

Ollama
Mistral model

No OpenAI API required.

No external AI calls.

Perfect for:

enterprise
on-prem
internal secure systems
Architecture
Jira Ticket Updated
↓
Jira Automation Rule
↓
Webhook hits FastAPI
↓
FastAPI fetches Jira issue
↓
Ollama generates:

- Summary
- Translation
- Sentiment
- Comment summary
  ↓
  Jira ticket updated automatically
  Project Structure
  Jira-api/
  │
  ├── app/
  │ ├── ai/
  │ │ ├── language_detector.py
  │ │ ├── ollama_client.py
  │ │ ├── sentiment.py
  │ │ ├── summarizer.py
  │ │ └── translator.py
  │ │
  │ ├── cache/
  │ │ └── sqlite_cache.py
  │ │
  │ ├── jira/
  │ │ ├── fetcher.py
  │ │ └── updater.py
  │ │
  │ ├── prompts/
  │ │ ├── sentiment.txt
  │ │ ├── summary.txt
  │ │ ├── translation.txt
  │ │ └── comments.txt
  │ │
  │ ├── utils/
  │ │ ├── extractor.py
  │ │ └── logger.py
  │ │
  │ └── main.py
  │
  ├── .env
  ├── requirements.txt
  └── README.md
  Prerequisites

Install:

Python 3.12+
Ollama
ngrok
Jira Cloud account
Step 1 — Install Python Dependencies

Inside project root:

pip3 install -r requirements.txt
Step 2 — Install Ollama

Install from:

Ollama Official Website

Verify:

ollama --version
Step 3 — Download AI Model

Pull Mistral model:

ollama pull mistral
Step 4 — Start Ollama
ollama serve

If you see:

address already in use

That means Ollama is already running.

Step 5 — Install ngrok

Install:

ngrok Download

Authenticate:

ngrok config add-authtoken YOUR_TOKEN
Step 6 — Start FastAPI Server

Run:

python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Expected:

Uvicorn running on http://0.0.0.0:8000
Step 7 — Start ngrok Tunnel

Open new terminal:

ngrok http 8000

Example:

Forwarding https://abc123.ngrok-free.dev -> http://localhost:8000

Copy this URL.

Step 8 — Configure Jira Automation

Open Jira:

Jira Automation Settings

Create Rule
Trigger

Use:

Issue Updated
Action

Choose:

Send web request
Webhook URL
https://YOUR_NGROK_URL.ngrok-free.dev/jira-webhook

Example:

https://abc123.ngrok-free.dev/jira-webhook
HTTP Method
POST
Headers
Key Value
Content-Type application/json
Request Body

Choose:

Custom Data

Paste:

{
"issue": {
"key": "{{issue.key}}"
}
}
Step 9 — Turn Rule ON

Enable automation rule.

Step 10 — Test the System

Edit any Jira ticket.

Example:

change summary
add comment
update description

Terminal should show:

WEBHOOK RECEIVED
PROCESSING ISSUE: MS-1
UPDATING JIRA FIELD...
Successfully processed
Jira AI Output Example
🤖 AI ISSUE SUMMARY

1. English Title
2. Short Summary
3. Root Cause
4. Priority
5. Suggested Fix

🌍 ENGLISH TITLE & DESCRIPTION

Translated English content

😊 CUSTOMER SENTIMENT

Frustrated

💬 COMMENT SUMMARY

- Login failing
- Token expired
- User blocked
  Environment Variables (.env)
  JIRA_DOMAIN=https://your-domain.atlassian.net

EMAIL=your-email@gmail.com

API_TOKEN=your-jira-api-token

PROJECT_KEY=MS

CUSTOM_FIELD_ID=customfield_10119

OLLAMA_MODEL=mistral
How to Generate Jira API Token

Open:

Atlassian API Tokens

Steps:

Create API Token
Copy token
Add into .env
Custom Jira Field

You need a Jira custom field to store AI summaries.

Example:

customfield_10119
How to Find Custom Field ID

Open Jira issue JSON:

curl --request GET \
--url "https://YOUR_DOMAIN.atlassian.net/rest/api/3/issue/MS-1" \
--user "EMAIL:API_TOKEN"

Search:

customfield\_
SQLite Cache

Used to avoid duplicate processing.

Database:

tickets.db

Stores:

processed ticket IDs
timestamps
Supported Deployment Options
Local Laptop

Runs completely on MacBook/Linux/Windows.

On-Premise Server

Can run internally inside company network.

Kubernetes

Can deploy to:

Azure Kubernetes Service
EKS
GKE
OpenShift
Troubleshooting

1. Ollama not running

Error:

connection refused

Fix:

ollama serve 2. ngrok not found

Install ngrok:

ngrok Download

3. Jira webhook empty body

Fix Jira automation body:

{
"issue": {
"key": "{{issue.key}}"
}
} 4. Module not found

Install dependencies:

pip3 install -r requirements.txt 5. SQLite unable to open database

Create cache folder:

mkdir -p app/cache
Future Improvements
RAG support
Vector database
Slack integration
Email summarization
Auto-priority detection
Duplicate issue detection
AI root-cause clustering
Multi-agent orchestration
Voice ticket summaries
Tech Stack
Technology Usage
FastAPI Backend API
Ollama Local LLM
Mistral AI Model
Jira REST API Ticket integration
SQLite Cache
ngrok Public webhook tunnel
Security
No external AI APIs
Fully local AI
Ticket data stays internal
Supports enterprise privacy requirements

AI-Powered Jira Automation System 🚀
