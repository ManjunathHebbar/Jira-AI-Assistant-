from fastapi import FastAPI, Request

from app.jira.fetcher import fetch_issue_by_key
from app.jira.updater import update_custom_field

from app.ai.translator import translate_content
from app.ai.summarizer import generate_ai_summary
from app.ai.summarizer import summarize_comments
from app.ai.sentiment import analyze_sentiment
from app.ai.language_detector import detect_language

from app.utils.extractor import extract_text
from app.utils.logger import logger

from app.cache.sqlite_cache import (
    initialize_database,
    is_ticket_processed,
    save_processed_ticket
)

app = FastAPI()

initialize_database()


@app.get("/")
def home():

    return {
        "status": "running"
    }


@app.post("/jira-webhook")
async def jira_webhook(request: Request):

    try:

        raw_body = await request.body()

        print("\n" + "=" * 100)
        print("WEBHOOK RECEIVED")

        if not raw_body:

            print("Empty webhook body received")

            return {
                "status": "ignored",
                "reason": "empty body"
            }

        try:

            payload = await request.json()

        except Exception:

            print("Invalid JSON payload")

            print(raw_body.decode("utf-8"))

            return {
                "status": "ignored",
                "reason": "invalid json"
            }

        print(payload)

        issue_data = payload.get("issue")

        if not issue_data:

            return {
                "status": "failed",
                "error": "No issue found in payload"
            }

        issue_key = issue_data.get("key")

        logger.info(f"Webhook received for {issue_key}")

        print(f"\nPROCESSING ISSUE: {issue_key}")

        # ================= CACHE CHECK =================

        if is_ticket_processed(issue_key):

            logger.info(
                f"Skipping already processed ticket {issue_key}"
            )

            return {
                "status": "skipped",
                "issue": issue_key
            }

        # ================= FETCH ISSUE =================

        issue = fetch_issue_by_key(issue_key)

        fields = issue.get("fields", {})

        title = fields.get("summary", "")

        description = extract_text(
            fields.get("description", {})
        )

        comments = (
            fields
            .get("comment", {})
            .get("comments", [])
        )

        # ================= COMMENTS =================

        all_comments = []

        for comment in comments:

            body = comment.get("body", {})

            comment_text = extract_text(body)

            if comment_text.strip():

                all_comments.append(comment_text)

        combined_comments = "\n".join(all_comments)

        # ================= LANGUAGE =================

        detected_language = detect_language(
            f"{title} {description}"
        )

        # ================= TRANSLATION =================

        translated_content = translate_content(
            title,
            description
        )

        # ================= COMMENT SUMMARY =================

        comments_summary = ""

        if combined_comments.strip():

            comments_summary = summarize_comments(
                combined_comments
            )

        # ================= AI SUMMARY =================

        ai_summary = generate_ai_summary(
            title,
            description,
            combined_comments
        )

        # ================= SENTIMENT =================

        sentiment = analyze_sentiment(
            title,
            description,
            combined_comments
        )

        # ================= FINAL CONTENT =================

        final_content = f"""
🤖 AI ISSUE SUMMARY
==================================================

{ai_summary}

==================================================
🌍 ENGLISH TITLE & DESCRIPTION
==================================================

{translated_content}

==================================================
🌐 DETECTED LANGUAGE
==================================================

{detected_language}

==================================================
😊 CUSTOMER SENTIMENT
==================================================

{sentiment}
"""

        if combined_comments.strip():

            final_content += f"""

==================================================
💬 COMMENT SUMMARY
==================================================

{comments_summary}
"""

        final_content += """

==================================================
"""

        print("\nUPDATING JIRA FIELD...")

        update_custom_field(
            issue_key,
            final_content
        )

        save_processed_ticket(issue_key)

        logger.info(
            f"Successfully processed {issue_key}"
        )

        return {
            "status": "success",
            "issue": issue_key
        }

    except Exception as e:

        logger.error(str(e))

        print("\nERROR:")
        print(str(e))

        return {
            "status": "failed",
            "error": str(e)
        }