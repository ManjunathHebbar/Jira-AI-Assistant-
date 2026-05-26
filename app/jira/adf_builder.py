def text_node(text):

    return {
        "type": "text",
        "text": str(text)
    }


def paragraph(text):

    return {
        "type": "paragraph",
        "content": [
            text_node(text)
        ]
    }


def heading(text, level=2):

    return {
        "type": "heading",
        "attrs": {
            "level": level
        },
        "content": [
            text_node(text)
        ]
    }


def bullet_list(items):

    return {
        "type": "bulletList",
        "content": [
            {
                "type": "listItem",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            text_node(item)
                        ]
                    }
                ]
            }
            for item in items
        ]
    }


def panel(text):

    return {
        "type": "panel",
        "attrs": {
            "panelType": "info"
        },
        "content": [
            paragraph(text)
        ]
    }


def build_ai_summary_adf(
    ai_summary,
    translated_content,
    sentiment,
    comments_summary,
    detected_language
):

    content = []

    # ==================================================
    # TITLE
    # ==================================================

    content.append(
        heading("🤖 AI Issue Summary", 2)
    )

    # ==================================================
    # SUMMARY PANEL
    # ==================================================

    content.append(
        panel(
            "AI-generated analysis for this Jira issue."
        )
    )

    # ==================================================
    # AI SUMMARY
    # ==================================================

    content.append(
        heading("📌 Summary", 3)
    )

    content.append(
        paragraph(ai_summary)
    )

    # ==================================================
    # TRANSLATION
    # ==================================================

    content.append(
        heading("🌍 English Translation", 3)
    )

    content.append(
        paragraph(translated_content)
    )

    # ==================================================
    # SENTIMENT
    # ==================================================

    content.append(
        heading("😊 Customer Sentiment", 3)
    )

    content.append(
        bullet_list([
            sentiment
        ])
    )

    # ==================================================
    # COMMENT SUMMARY
    # ==================================================

    if comments_summary.strip():

        comment_items = [
            line.strip("- ").strip()
            for line in comments_summary.split("\n")
            if line.strip()
        ]

        content.append(
            heading("💬 Comment Summary", 3)
        )

        content.append(
            bullet_list(comment_items)
        )

    # ==================================================
    # LANGUAGE
    # ==================================================

    content.append(
        heading("🌐 Detected Language", 3)
    )

    content.append(
        bullet_list([
            detected_language
        ])
    )

    return {
        "type": "doc",
        "version": 1,
        "content": content
    }