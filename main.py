import os
import requests
import codecs
from jinja2 import Template
from dotenv import load_dotenv

# Set token
def get_private_token():
    access_token = os.environ.get('token.txt')
    return access_token

# Perform the requests to GH
def get_github_repo_info(owner, repo, access_token):
    base_url = f'https://api.github.com/repos/{owner}/{repo}'
    
    headers = {
        'Authorization': f'Token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        # Fetch repository information from GitHub API
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        repo_info = response.json()
        print(repo_info['name'])
        return repo_info

    except requests.exceptions.RequestException as e:
        print(f"Error querying GitHub API: {e}")
        return None
    
# Read the URLs from the file
def read_urls_from_file(input_file, access_token):

    with open(input_file, 'r') as urls_file:
        urls = urls_file.read().splitlines()

    for url in urls:
        # DEBUG for URL
        # print(f"\nSplit the URL -> {url}...")

        # Split the URL into username and repo
        parts = url.split('/')
        github_owner = parts[-2]
        github_repo = parts[-1]

        # DEBUG Print the username and repo
        # print("Username:", github_owner)
        # print("Repository:", github_repo)

        # Get the Repo Information
        repo_info = get_github_repo_info(github_owner, github_repo, access_token)

        # Save each repo to JSON file for DEBUG
        with open(f'output/{github_repo}.json', 'w') as repo_file:
            repo_file.write(str(repo_info))

        # Save each repo to Markdown file
        with open(f'template.md', 'r') as template_file:
            template = Template(template_file.read(),trim_blocks=True)
        rendered = template.render(repo_info=repo_info)

        # Save the rendered template to a report file in Markdown
        report_file = codecs.open(f'reports-md/{github_repo}.md', 'w', encoding='utf-8')
        report_file.write(rendered)
        report_file.close()
       
# Markdown to PDF
# Build this with Docker, or GH Actions

def main():
    load_dotenv()
    access_token = os.environ.get("access_token")
    input_file = 'repos.txt'
    read_urls_from_file(input_file, access_token)

if __name__ == "__main__":
    main()
