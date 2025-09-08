#!/Users/alex/Code/raycast-script-commands/.venv/bin/python

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
        issue = jira_client.issue(ticket_id, expand='comments')
        
        ticket_info = {
            'key': issue.key,
            'title': issue.fields.summary,
            'description': issue.fields.description or "No description provided",
            'status': issue.fields.status.name,
            'assignee': getattr(issue.fields.assignee, 'displayName', 'Unassigned'),
            'reporter': getattr(issue.fields.reporter, 'displayName', 'Unknown'),
            'created': format_datetime(issue.fields.created),
            'updated': format_datetime(issue.fields.updated),
            'comments': []
        }
        
        # Get comments sorted chronologically
        comments = sorted(issue.fields.comment.comments, key=lambda x: x.created)
        
        for comment in comments:
            ticket_info['comments'].append({
                'author': comment.author.displayName.split()[0],  # First name only
                'created': format_datetime(comment.created),
                'body': comment.body
            })
        
        return ticket_info
        
    except Exception as e:
        return None, str(e)


def generate_summary(openai_client, ticket_info):
    """Generate AI summary of the ticket and comments."""
    try:
        # Prepare content for summarization
        content = f"""
Ticket: {ticket_info['title']}
Status: {ticket_info['status']}
Description: {ticket_info['description']}

Comments ({len(ticket_info['comments'])} total):
"""
        
        for comment in ticket_info['comments']:
            content += f"\n{comment['author']} ({comment['created']}): {comment['body']}\n"
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes JIRA tickets. Provide a concise, structured summary that highlights the key points, current status, and main discussion topics from the comments."
                },
                {
                    "role": "user",
                    "content": f"Please summarize this JIRA ticket and its comments:\n\n{content}"
                }
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
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
        print("❌ JIRA credentials not found. Please set JIRA_SERVER, JIRA_EMAIL, and JIRA_API_TOKEN environment variables.")
        print("💡 Add these to your .env file:")
        print("   JIRA_SERVER=https://your-domain.atlassian.net")
        print("   JIRA_EMAIL=your-email@company.com")
        print("   JIRA_API_TOKEN=your-api-token")
        sys.exit(1)
    
    try:
        print(f"🔍 Fetching JIRA ticket: {ticket_id}")
        
        # Connect to JIRA
        jira_client = JIRA(
            server=jira_server,
            basic_auth=(jira_email, jira_token)
        )
        
        # Get ticket information
        result = get_ticket_info(jira_client, ticket_id)
        
        if isinstance(result, tuple):
            ticket_info, error = result
            print(f"❌ Error fetching ticket: {error}")
            sys.exit(1)
        
        ticket_info = result
        
        # Display ticket information
        print(f"\n🎫 **{ticket_info['key']}: {ticket_info['title']}**")
        print(f"📊 Status: {ticket_info['status']}")
        print(f"👤 Assignee: {ticket_info['assignee']}")
        print(f"📝 Reporter: {ticket_info['reporter']}")
        print(f"📅 Created: {ticket_info['created']}")
        print(f"🔄 Updated: {ticket_info['updated']}")
        
        print("\n📋 **Description:**")
        print(ticket_info['description'])
        
        # Display comments
        if ticket_info['comments']:
            print(f"\n💬 **Comments ({len(ticket_info['comments'])}):**")
            print("-" * 50)
            
            for comment in ticket_info['comments']:
                print(f"\n👤 **{comment['author']}** - {comment['created']}")
                print(comment['body'])
                print("-" * 50)
        else:
            print("\n💬 **Comments:** No comments found")
        
        # Generate AI summary if requested
        if include_summary:
            openai_api_key = os.environ.get("OPENAI_API_KEY")
            if not openai_api_key:
                print("\n❌ OpenAI API key not found. Cannot generate summary.")
                print("💡 Set OPENAI_API_KEY environment variable to enable AI summaries.")
            else:
                print("\n🤖 **AI Summary:**")
                print("Generating summary...")
                
                openai_client = OpenAI(api_key=openai_api_key)
                summary = generate_summary(openai_client, ticket_info)
                
                print(summary)
        
        print(f"\n✅ Successfully retrieved information for {ticket_id}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()