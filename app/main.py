from fastapi import FastAPI, Request
import time

from app.jira.fetcher import fetch_issue_by_key
from app.jira.updater import update_custom_field

from app.ai.translator import translate_content
from app.ai.summarizer import generate_ai_summary
from app.ai.summarizer import summarize_comments
from app.ai.sentiment import analyze_sentiment
from app.ai.language_detector import detect_language

from app.utils.extractor import extract_text
from app.utils.logger import logger
from app.utils.hash_util import generate_content_hash

from app.cache.sqlite_cache import (
    initialize_database,
    should_process_ticket,
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

    start_time = time.time()

    try:

        raw_body = await request.body()

        print("\n" + "=" * 100)
        print("WEBHOOK RECEIVED")

        # ==========================================
        # EMPTY BODY CHECK
        # ==========================================

        if not raw_body:

            print("Empty webhook body received")

            return {
                "status": "ignored",
                "reason": "empty body"
            }

        # ==========================================
        # JSON PARSE
        # ==========================================

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

        # ==========================================
        # ISSUE VALIDATION
        # ==========================================

        issue_data = payload.get("issue")

        if not issue_data:

            return {
                "status": "failed",
                "error": "No issue found in payload"
            }

        issue_key = issue_data.get("key")

        print(f"\nPROCESSING ISSUE: {issue_key}")

        logger.info(
            f"Webhook received for {issue_key}"
        )

        # ==========================================
        # FETCH ISSUE
        # ==========================================

        issue = fetch_issue_by_key(issue_key)

        fields = issue.get("fields", {})

        # ==========================================
        # TITLE
        # ==========================================

        title = fields.get("summary", "")

        # ==========================================
        # DESCRIPTION
        # ==========================================

        description = extract_text(
            fields.get("description", {})
        )

        # ==========================================
        # COMMENTS
        # ==========================================

        comments = (
            fields
            .get("comment", {})
            .get("comments", [])
        )

        all_comments = []

        for comment in comments:

            body = comment.get("body", {})

            comment_text = extract_text(body)

            if comment_text.strip():

                all_comments.append(comment_text)

        combined_comments = "\n".join(all_comments)

        # ==========================================
        # INPUT HASH
        # ==========================================

        input_content = f"""
{title}
{description}
{combined_comments}
"""

        input_hash = generate_content_hash(
            input_content
        )

        print("\nINPUT HASH:", input_hash)

        # ==========================================
        # CACHE CHECK
        # ==========================================

        if not should_process_ticket(
            issue_key,
            input_hash
        ):

            print(
                "\nSKIPPING - INPUT UNCHANGED"
            )

            return {
                "status": "skipped",
                "issue": issue_key
            }

        # ==========================================
        # LANGUAGE DETECTION
        # ==========================================

        detected_language = detect_language(
            f"{title} {description}"
        )

        # ==========================================
        # TRANSLATION
        # ==========================================

        translated_content = translate_content(
            title,
            description
        )

        # ==========================================
        # COMMENT SUMMARY
        # ==========================================

        comments_summary = ""

        if combined_comments.strip():

            comments_summary = summarize_comments(
                combined_comments
            )

        # ==========================================
        # AI SUMMARY
        # ==========================================

        ai_summary = generate_ai_summary(
            title,
            description,
            combined_comments
        )

        # ==========================================
        # SENTIMENT
        # ==========================================

        sentiment = analyze_sentiment(
            title,
            description,
            combined_comments
        )

        # ==========================================
        # FINAL CONTENT
        # ==========================================

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

        # ==========================================
        # UPDATE JIRA
        # ==========================================

        print("\nUPDATING JIRA FIELD...")

        update_custom_field(
            issue_key,
            final_content
        )

        # ==========================================
        # SAVE HASH
        # ==========================================

        save_processed_ticket(
            issue_key,
            input_hash
        )

        end_time = time.time()

        total_time = round(
            end_time - start_time,
            2
        )

        print(
            f"\nPROCESSING TIME: {total_time} sec"
        )

        logger.info(
            f"Successfully processed {issue_key}"
        )

        return {
            "status": "success",
            "issue": issue_key,
            "processing_time": total_time
        }

    except Exception as e:

        logger.error(str(e))

        print("\nERROR:")
        print(str(e))

        return {
            "status": "failed",
            "error": str(e)
        }