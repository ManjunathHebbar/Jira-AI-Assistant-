from fastapi import FastAPI, Request

from app.jira.fetcher import fetch_issue_by_key
from app.jira.updater import add_ai_comment

from app.ai.translator import translate_content
from app.ai.summarizer import generate_ai_summary
from app.ai.summarizer import summarize_comments
from app.ai.sentiment import analyze_sentiment
from app.ai.language_detector import detect_language

from app.utils.extractor import extract_text
from app.utils.logger import logger

from app.cache.sqlite_cache import (
    initialize_database,
    is_input_processed,
    save_processed_input
)

from app.jira.adf_builder import (
    build_ai_summary_adf
)

import hashlib
import time

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

        # ==================================================
        # EMPTY BODY CHECK
        # ==================================================

        if not raw_body:

            print("Empty webhook body received")

            return {
                "status": "ignored",
                "reason": "empty body"
            }

        # ==================================================
        # JSON PARSE
        # ==================================================

        try:

            payload = await request.json()

        except Exception:

            print("Invalid JSON payload")

            print(
                raw_body.decode("utf-8")
            )

            return {
                "status": "ignored",
                "reason": "invalid json"
            }

        print(payload)

        # ==================================================
        # ISSUE VALIDATION
        # ==================================================

        issue_data = payload.get("issue")

        if not issue_data:

            return {
                "status": "failed",
                "error": "No issue found in payload"
            }

        issue_key = issue_data.get("key")

        logger.info(
            f"Webhook received for {issue_key}"
        )

        print(
            f"\nPROCESSING ISSUE: {issue_key}"
        )

        # ==================================================
        # FETCH ISSUE
        # ==================================================

        issue = fetch_issue_by_key(issue_key)

        fields = issue.get("fields", {})

        title = fields.get(
            "summary",
            ""
        )

        description = extract_text(
            fields.get(
                "description",
                {}
            )
        )

        comments = (
            fields
            .get("comment", {})
            .get("comments", [])
        )

        # ==================================================
        # EXTRACT COMMENTS
        # ==================================================

        all_comments = []

        for comment in comments:

            body = comment.get(
                "body",
                {}
            )

            comment_text = extract_text(
                body
            )

            if comment_text.strip():

                all_comments.append(
                    comment_text
                )

        combined_comments = "\n".join(
            all_comments
        )

        # ==================================================
        # PREVENT INFINITE LOOP
        # ==================================================

        input_data = (
            title
            + description
            + combined_comments
        )

        input_hash = hashlib.md5(
            input_data.encode()
        ).hexdigest()

        print(
            f"\nINPUT HASH: {input_hash}"
        )

        if is_input_processed(
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

        # ==================================================
        # LANGUAGE DETECTION
        # ==================================================

        detected_language = detect_language(
            f"{title} {description}"
        )

        # ==================================================
        # TRANSLATION
        # ==================================================

        translated_content = translate_content(
            title,
            description
        )

        # ==================================================
        # COMMENTS SUMMARY
        # ==================================================

        comments_summary = ""

        if combined_comments.strip():

            comments_summary = summarize_comments(
                combined_comments
            )

        # ==================================================
        # AI SUMMARY
        # ==================================================

        ai_summary = generate_ai_summary(
            title,
            description,
            combined_comments
        )

        # ==================================================
        # SENTIMENT
        # ==================================================

        sentiment = analyze_sentiment(
            title,
            description,
            combined_comments
        )

        # ==================================================
        # BUILD JIRA ADF CONTENT
        # ==================================================

        adf_content = build_ai_summary_adf(
            ai_summary=ai_summary,
            translated_content=translated_content,
            sentiment=sentiment,
            comments_summary=comments_summary,
            detected_language=detected_language
        )

        # ==================================================
        # ADD AI COMMENT
        # ==================================================

        print("\nADDING AI COMMENT...")

        add_ai_comment(
            issue_key,
            adf_content
        )

        # ==================================================
        # SAVE CACHE
        # ==================================================

        save_processed_input(
            issue_key,
            input_hash
        )

        total_time = round(
            time.time() - start_time,
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