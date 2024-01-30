import requests
import markdown
from bs4 import BeautifulSoup

def get_github_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Create an empty dictionary to store the GitHub information
        github_info = {}

        # Just the right box
        bordergrid_html_element = soup.select_one('.BorderGrid')

        # Name/Title
        name_html_element = soup.select_one('[itemprop="name"]')
        name = name_html_element.get_text().strip()

        # Stars
        star_icon_html_element = bordergrid_html_element.select_one('.octicon-star')
        stars_html_element = star_icon_html_element.find_next_sibling('strong')
        stars = stars_html_element.get_text().strip().replace(',', '')

        # Watchers
        eye_icon_html_element = bordergrid_html_element.select_one('.octicon-eye')
        watchers_html_element = eye_icon_html_element.find_next_sibling('strong')
        watchers = watchers_html_element.get_text().strip().replace(',', '')

        # Forks
        fork_icon_html_element = bordergrid_html_element.select_one('.octicon-repo-forked')
        forks_html_element = fork_icon_html_element.find_next_sibling('strong')
        forks = forks_html_element.get_text().strip().replace(',', '')

        # Number of GitHub contributors
        contributors_html_element = soup.select_one('a[href$="contributors"]')
        contributors = contributors_html_element.get_text().strip().split()[1]

        # Commits
        commits_element = soup.find('span', class_='num text-emphasized')
        commits_count = commits_element.text.strip() if commits_element else 'Not available'

        # Extracting the languages used
        languages = [lang.text.strip() for lang in soup.select('span[itemprop="programmingLanguage"]')]

        return {
            'url': url,
            'stars': stars,
            'title': name,
            'watchers': watchers,
            'forks': forks,
            'contributors': contributors,
            'commits': commits_count,
            'languages': languages if languages else 'Not available',
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    input_file = 'repos.txt'

    with open(input_file, 'r') as urls_file:
        urls = urls_file.read().splitlines()

    for url in urls:
        print(f"\nFetching information from {url}...")
        github_info = get_github_info(url)

        if github_info:
            print(f"Title: {github_info['title']}")
            print(f"URL: {github_info['url']}")
            print(f"Stars: {github_info['stars']}")
            print(f"Watchers: {github_info['watchers']}")
            print(f"Forks: {github_info['forks']}")
            print(f"Contributors: {github_info['contributors']}")
            print(f"Commits: {github_info['commits']}")
            print(f"Languages: {github_info['languages']}")
        else:
            print("Failed to fetch GitHub information")

if __name__ == "__main__":
    main()