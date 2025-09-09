#!/usr/bin/env python3
"""Get JIRA Ticket Info - Fetch comprehensive JIRA ticket information."""

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

import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import click
from jira import JIRA
from openai import OpenAI
from rich.console import Console
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import settings
from .logging import ScriptLogger, configure_logging
from .utils import print_error, print_success, set_clipboard_text

console = Console()


class JIRATicketInfo:
    """Handles JIRA ticket information retrieval and processing."""

    def __init__(self) -> None:
        """Initialize JIRA client."""
        if not settings.has_jira_config:
            print_error("JIRA credentials not found. Please set JIRA_SERVER, JIRA_EMAIL, and JIRA_API_TOKEN environment variables.")
            console.print("💡 Add these to your .env file:", style="blue")
            console.print("   JIRA_SERVER=https://your-domain.atlassian.net", style="blue")
            console.print("   JIRA_EMAIL=your-email@company.com", style="blue")
            console.print("   JIRA_API_TOKEN=your-api-token", style="blue")
            sys.exit(1)
        
        self.jira_client = JIRA(
            server=settings.jira_server,
            basic_auth=(settings.jira_email, settings.jira_api_token)
        )
        
        self.openai_client: Optional[OpenAI] = None
        if settings.has_openai_config:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)

    def format_datetime(self, dt_str: str) -> str:
        """Format JIRA datetime string to readable format."""
        try:
            dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            return dt.strftime("%B %d, %Y at %I:%M %p")
        except Exception:
            return dt_str

    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    def get_ticket_info(self, ticket_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Fetch ticket information from JIRA with retry logic."""
        try:
            issue = self.jira_client.issue(ticket_id, expand="comments")

            ticket_info = {
                "key": issue.key,
                "title": issue.fields.summary,
                "description": issue.fields.description or "No description provided",
                "status": issue.fields.status.name,
                "assignee": getattr(issue.fields.assignee, "displayName", "Unassigned"),
                "reporter": getattr(issue.fields.reporter, "displayName", "Unknown"),
                "created": self.format_datetime(issue.fields.created),
                "updated": self.format_datetime(issue.fields.updated),
                "comments": [],
            }

            # Get comments sorted chronologically
            comments = sorted(issue.fields.comment.comments, key=lambda x: x.created)

            for comment in comments:
                ticket_info["comments"].append({
                    "author": comment.author.displayName.split()[0],  # First name only
                    "created": self.format_datetime(comment.created),
                    "body": comment.body,
                })

            return ticket_info, None

        except Exception as e:
            return None, str(e)

    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    def generate_summary(self, ticket_info: Dict[str, Any]) -> str:
        """Generate AI summary of the ticket and comments."""
        if not self.openai_client:
            return "❌ OpenAI API key not found. Cannot generate summary."

        try:
            # Prepare content for summarization
            content = f"""
Ticket: {ticket_info["title"]}
Status: {ticket_info["status"]}
Description: {ticket_info["description"]}

Comments ({len(ticket_info["comments"])} total):
"""

            for comment in ticket_info["comments"]:
                content += f"\n{comment['author']} ({comment['created']}): {comment['body']}\n"

            input_text = f"Please summarize this JIRA ticket and its comments. Provide a concise, structured summary that highlights the key points, current status, and main discussion topics from the comments:\n\n{content}"

            response = self.openai_client.responses.create(
                model=settings.model,
                input=input_text,
                text={"verbosity": "low"},
            )

            return response.output_text.strip()

        except Exception as e:
            return f"❌ Failed to generate summary: {str(e)}"

    def format_output(self, ticket_info: Dict[str, Any], include_summary: bool = False) -> str:
        """Format ticket information for output."""
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
        if include_summary:
            summary = self.generate_summary(ticket_info)
            output_text += f"\n🤖 AI Summary:\n{summary}"

        return output_text

    def display_ticket_info(self, ticket_info: Dict[str, Any], include_summary: bool = False) -> None:
        """Display ticket information to console."""
        console.print(f"\n🎫 **{ticket_info['key']}: {ticket_info['title']}**", style="bold")
        console.print(f"📊 Status: {ticket_info['status']}", style="blue")
        console.print(f"👤 Assignee: {ticket_info['assignee']}", style="blue")
        console.print(f"📝 Reporter: {ticket_info['reporter']}", style="blue")
        console.print(f"📅 Created: {ticket_info['created']}", style="blue")
        console.print(f"🔄 Updated: {ticket_info['updated']}", style="blue")

        console.print("\n📋 **Description:**", style="bold")
        console.print(ticket_info["description"])

        # Display comments
        if ticket_info["comments"]:
            console.print(f"\n💬 **Comments ({len(ticket_info['comments'])}):**", style="bold")
            console.print("-" * 50)

            for comment in ticket_info["comments"]:
                console.print(f"\n👤 **{comment['author']}** - {comment['created']}", style="bold")
                console.print(comment["body"])
                console.print("-" * 50)
        else:
            console.print("\n💬 **Comments:** No comments found", style="bold")

        # Display AI summary if generated
        if include_summary:
            summary = self.generate_summary(ticket_info)
            if "❌" in summary:
                console.print(f"\n{summary}", style="red")
            else:
                console.print("\n🤖 **AI Summary:**", style="bold")
                console.print(summary)

    def process_ticket(self, ticket_id: str, include_summary: bool = False) -> None:
        """Process a JIRA ticket and display/copy information."""
        console.print(f"🔍 Fetching JIRA ticket: {ticket_id}", style="blue")

        # Get ticket information
        ticket_info, error = self.get_ticket_info(ticket_id)

        if error:
            print_error(f"Error fetching ticket: {error}")
            sys.exit(1)

        if not ticket_info:
            print_error("Failed to fetch ticket information")
            sys.exit(1)

        # Format output
        output_text = self.format_output(ticket_info, include_summary)

        # Copy to clipboard
        set_clipboard_text(output_text)

        # Display to console
        self.display_ticket_info(ticket_info, include_summary)

        print_success(f"Successfully retrieved information for {ticket_id}")
        console.print("📋 Full ticket information copied to clipboard!", style="green")


@click.command()
@click.argument("ticket_id")
@click.option("--summary/--no-summary", default=False, help="Include AI summary")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def main(ticket_id: str, summary: bool, verbose: bool) -> None:
    """Fetch JIRA ticket details including title, description, and comments."""
    if verbose:
        settings.log_level = "DEBUG"
    
    configure_logging()
    
    with ScriptLogger("jira-ticket-info", ticket_id=ticket_id, include_summary=summary, verbose=verbose):
        jira_handler = JIRATicketInfo()
        jira_handler.process_ticket(ticket_id, summary)


if __name__ == "__main__":
    # Handle Raycast arguments
    if len(sys.argv) >= 3:
        # Raycast mode - ticket ID and summary flag
        ticket_id = sys.argv[1]
        include_summary = sys.argv[2] == "summary"
        main([ticket_id, "--summary" if include_summary else "--no-summary"])
    else:
        # CLI mode
        main()