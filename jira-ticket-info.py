#!/bin/sh
''''exec "$(dirname "$0")/.venv/bin/python" "$0" "$@" #'''

# Required parameters
# @raycast.schemaVersion 1
# @raycast.title Get JIRA Ticket Info
# @raycast.mode fullOutput

# Optional parameters
# @raycast.icon 🎫
# @raycast.description Fetch JIRA ticket details including title, description, and comments
# @raycast.packageName JIRA Integration
# @raycast.needsConfirmation false
# @raycast.argument1 {"type": "text", "placeholder": "Enter JIRA ticket ID (e.g., PROJ-123)"}
# @raycast.argument2 {"type": "dropdown", "placeholder": "Include AI summary?", "data": [{"title": "No summary", "value": "none"}, {"title": "Include AI summary", "value": "summary"}]}

import os
import sys
from datetime import datetime
from jira import JIRA
from openai import OpenAI
from dotenv import load_dotenv
import pyperclip


def format_datetime(dt_str):
    """Format JIRA datetime string to readable format."""
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except Exception:
        return dt_str


def get_ticket_info(jira_client, ticket_id):
    """Fetch ticket information from JIRA."""
    try:
        issue = jira_client.issue(ticket_id, expand="comments")

        ticket_info = {
            "key": issue.key,
            "title": issue.fields.summary,
            "description": issue.fields.description or "No description provided",
            "status": issue.fields.status.name,
            "assignee": getattr(issue.fields.assignee, "displayName", "Unassigned"),
            "reporter": getattr(issue.fields.reporter, "displayName", "Unknown"),
            "created": format_datetime(issue.fields.created),
            "updated": format_datetime(issue.fields.updated),
            "comments": [],
        }

        # Get comments sorted chronologically
        comments = sorted(issue.fields.comment.comments, key=lambda x: x.created)

        for comment in comments:
            ticket_info["comments"].append(
                {
                    "author": comment.author.displayName.split()[0],  # First name only
                    "created": format_datetime(comment.created),
                    "body": comment.body,
                }
            )

        return ticket_info

    except Exception as e:
        return None, str(e)


def generate_summary(openai_client, ticket_info):
    """Generate AI summary of the ticket and comments."""
    try:
        # Prepare content for summarization
        content = f"""
Ticket: {ticket_info["title"]}
Status: {ticket_info["status"]}
Description: {ticket_info["description"]}

Comments ({len(ticket_info["comments"])} total):
"""

        for comment in ticket_info["comments"]:
            content += (
                f"\n{comment['author']} ({comment['created']}): {comment['body']}\n"
            )

        input_text = f"Please summarize this JIRA ticket and its comments. Provide a concise, structured summary that highlights the key points, current status, and main discussion topics from the comments:\n\n{content}"

        response = openai_client.responses.create(
            model=os.environ.get("MODEL", "gpt-5-mini"),
            input=input_text,
            text={"verbosity": "low"},
        )

        return response.output_text.strip()

    except Exception as e:
        return f"❌ Failed to generate summary: {str(e)}"


def main():
    load_dotenv()

    if len(sys.argv) < 3:
        print("❌ Usage: jira-ticket-info.py <ticket-id> <include-summary>")
        sys.exit(1)

    ticket_id = sys.argv[1].strip()
    include_summary = sys.argv[2].strip() == "summary"

    # JIRA connection setup
    jira_server = os.environ.get("JIRA_SERVER")
    jira_email = os.environ.get("JIRA_EMAIL")
    jira_token = os.environ.get("JIRA_API_TOKEN")

    if not all([jira_server, jira_email, jira_token]):
        print(
            "❌ JIRA credentials not found. Please set JIRA_SERVER, JIRA_EMAIL, and JIRA_API_TOKEN environment variables."
        )
        print("💡 Add these to your .env file:")
        print("   JIRA_SERVER=https://your-domain.atlassian.net")
        print("   JIRA_EMAIL=your-email@company.com")
        print("   JIRA_API_TOKEN=your-api-token")
        sys.exit(1)

    try:
        print(f"🔍 Fetching JIRA ticket: {ticket_id}")

        # Connect to JIRA
        jira_client = JIRA(server=jira_server, basic_auth=(jira_email, jira_token))

        # Get ticket information
        result = get_ticket_info(jira_client, ticket_id)

        if isinstance(result, tuple):
            ticket_info, error = result
            print(f"❌ Error fetching ticket: {error}")
            sys.exit(1)

        ticket_info = result

        # Prepare formatted output for clipboard
        output_text = f"🎫 {ticket_info['key']}: {ticket_info['title']}\n"
        output_text += f"📊 Status: {ticket_info['status']}\n"
        output_text += f"👤 Assignee: {ticket_info['assignee']}\n"
        output_text += f"📝 Reporter: {ticket_info['reporter']}\n"
        output_text += f"📅 Created: {ticket_info['created']}\n"
        output_text += f"🔄 Updated: {ticket_info['updated']}\n\n"

        output_text += "📋 Description:\n"
        output_text += f"{ticket_info['description']}\n\n"

        # Add comments to output
        if ticket_info["comments"]:
            output_text += f"💬 Comments ({len(ticket_info['comments'])}):\n"
            output_text += "-" * 50 + "\n"

            for comment in ticket_info["comments"]:
                output_text += f"\n👤 {comment['author']} - {comment['created']}\n"
                output_text += f"{comment['body']}\n"
                output_text += "-" * 50 + "\n"
        else:
            output_text += "💬 Comments: No comments found\n"

        # Generate AI summary if requested
        summary_text = ""
        if include_summary:
            openai_api_key = os.environ.get("OPENAI_API_KEY")
            if not openai_api_key:
                summary_text = "\n❌ OpenAI API key not found. Cannot generate summary.\n💡 Set OPENAI_API_KEY environment variable to enable AI summaries."
            else:
                print("🤖 Generating AI summary...")

                openai_client = OpenAI(api_key=openai_api_key)
                summary = generate_summary(openai_client, ticket_info)

                summary_text = f"\n🤖 AI Summary:\n{summary}"

        # Add summary to output if available
        if summary_text:
            output_text += summary_text

        # Copy formatted output to clipboard
        pyperclip.copy(output_text)

        # Display ticket information
        print(f"\n🎫 **{ticket_info['key']}: {ticket_info['title']}**")
        print(f"📊 Status: {ticket_info['status']}")
        print(f"👤 Assignee: {ticket_info['assignee']}")
        print(f"📝 Reporter: {ticket_info['reporter']}")
        print(f"📅 Created: {ticket_info['created']}")
        print(f"🔄 Updated: {ticket_info['updated']}")

        print("\n📋 **Description:**")
        print(ticket_info["description"])

        # Display comments
        if ticket_info["comments"]:
            print(f"\n💬 **Comments ({len(ticket_info['comments'])}):**")
            print("-" * 50)

            for comment in ticket_info["comments"]:
                print(f"\n👤 **{comment['author']}** - {comment['created']}")
                print(comment["body"])
                print("-" * 50)
        else:
            print("\n💬 **Comments:** No comments found")

        # Display AI summary if generated
        if summary_text:
            if "❌" in summary_text:
                print(summary_text)
            else:
                print("\n🤖 **AI Summary:**")
                print(summary.strip())

        print(f"\n✅ Successfully retrieved information for {ticket_id}")
        print("📋 Full ticket information copied to clipboard!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
