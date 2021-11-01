#!/usr/bin/env python3

import argparse
import re
import subprocess
import keyring
from jira import JIRA


def get_issue_name_from_branch_name(branch):
    matches = re.findall('[a-zA-Z]{1,10}-[0-9]{1,5}', branch)
    if len(matches) > 0:
        return matches[0]


def get_issue_title_from_jira(jira_args, issue_name):
    if jira_args:
        server = jira_args[0]
        jira_username = jira_args[1]
        if server and jira_username:
            jira_api_token = keyring.get_password("add-msg-issue-suffix-hook", jira_username)
            jira = JIRA(server=server, basic_auth=(jira_username, jira_api_token))
            return jira.issue(issue_name, fields='summary').fields.summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_filepath")
    parser.add_argument(
        '-t',
        '--template',
        default="[{}]",
        help='Template to render ticket id into'
    )
    parser.add_argument(
        '-j',
        '--jira',
        nargs=2,
        help='Affix issue title by fetching info from Jira\nMust provide server url and email, in this order'
    )
    args = parser.parse_args()
    commit_msg_filepath = args.commit_msg_filepath
    template = args.template

    branch = ""
    try:
        branch = subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"], universal_newlines=True).strip()
    except Exception as e:
        print(e)

    issue_name = get_issue_name_from_branch_name(branch)

    issue_title = get_issue_title_from_jira(args.jira, issue_name)

    with open(commit_msg_filepath, "r+") as f:
        content = f.read()
        content_subject = content.split("\n", maxsplit=1)[0].strip()
        f.seek(0, 0)
        if issue_name and issue_name not in content_subject:
            suffix = template.format(issue_name)
            f.write("{}\n\n{}".format(content, suffix))
            if issue_title and issue_title not in content_subject:
                f.write("\n{}".format(issue_title))
        else:
            f.write(content)


if __name__ == "__main__":
    exit(main())
