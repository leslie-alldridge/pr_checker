import requests
import json
from env import token, url, slack_webhook_dev
from github import Github

# First create a Github instance:
github = Github(base_url=url, login_or_token=token)

# Globals
python_repos = []
python_repos_issue = []
# Get all repos and analyze their tags
# add repos tagged with python to an array and print it


def lambda_handler(event, context):
    check_issues()    

def check_prs():
    print('Checking repositories, please wait a moment...')
    repositories = github.search_repositories(query='language:python')
    for repo in repositories:
        topics = repo.get_topics()
        if topics != []:
            if "m-and-m" in topics:
                # here we would have all of our team tagged repos but just using 'python' for now
                python_repos.append(repo.full_name)
                # check if it has a PR?
                pulls = repo.get_pulls(
                    state='open')
                for pr in pulls:
                    # Print out message and PR url
                    result = "Your repository"  + repo.full_name + " has an open PR here: " + pr.html_url
                    slack_data = {'text': ":point_right: " + result}                    
                    #print(message)
                    headers = {
                        "Content-type":"application/json"
                    }
                    r = requests.post(slack_webhook_dev, data=json.dumps(slack_data), headers=headers)
                    if r.status_code == 200:
                        print('Webhook sent for PRs!')
                    else:
                        print('Error sending webhook to Slack - PRs')


def check_issues():
    print('Checking issues, please wait a moment...')
    repositories_issue = github.search_repositories(query='language:python')
    for repo in repositories_issue:
        topics_issue = repo.get_topics()
        if topics_issue != []:
            if "m-and-m" in topics_issue:
                # here we would have all of our team tagged repos but just using 'python' for now
                python_repos_issue.append(repo.full_name)
                # check if it has an issue(s)?
                issues = repo.get_issues(
                    state='open')
                print(issues)
                for issue in issues:
                    #print(issue)
                    # Print out message and PR url
                    print(issue.html_url)
                    result_issue = "Your repository"  + repo.full_name + " has an open issue here: " + issue.html_url
                    slack_data_issue = {'text': ":point_right: " + result_issue}                    
                    #print(message)
                    headers_issue = {
                        "Content-type":"application/json"
                    }
                    r = requests.post(slack_webhook_dev, data=json.dumps(slack_data_issue), headers=headers_issue)
                    if r.status_code == 200:
                        print('Webhook sent for issues!')
                    else:
                        print('Error sending webhook to Slack - Issues')

# main lambda call
lambda_handler('test', 'test')
