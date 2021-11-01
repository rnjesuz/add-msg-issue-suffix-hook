add-msg-issue-suffix-hook
=========================

A prepare-commit-msg hook for pre-commit.
See also: https://github.com/pre-commit/pre-commit

This hook searches the branch's name for Jira issues and apends commit messages with it

## Install pre-commit

```bash
pip install pre-commit
```

## Install pre-commit-msg hook
Install prepare-commit-msg hooks using

```bash
pre-commit install --hook-type prepare-commit-msg
```

## Using with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/rnjesuz/add-msg-issue-suffix-hook
    rev: v0.2.0  # Use the ref you want to point at
    hooks:
    -   id: add-msg-issue-suffix
```

## Optionals
### Template argument
Change how the issue is rendered to the commit message using the `--template` argument.

Default is `[<issue name goes here>]`

```yaml
-   repo: https://github.com/rnjesuz/add-msg-issue-suffix-hook
    rev: v0.2.0  # Use the ref you want to point at
    hooks:
    -   id: add-msg-issue-suffix
        args:
            - --template=[{}]
```
```yaml
-   repo: https://github.com/rnjesuz/add-msg-issue-suffix-hook
    rev: v0.2.0  # Use the ref you want to point at
    hooks:
    -   id: add-msg-issue-suffix
        args:
            - --template=Jira-Ref:{}
```

### Issue title argument
Add the issue's title to the commit message using the `--jira` argument.
Must provide the URL hosting the server and your Jira user's email, in this order.

```yaml
-   repo: https://github.com/rnjesuz/add-msg-issue-suffix-hook
    rev: v0.2.0  # Use the ref you want to point at
    hooks:
    -   id: add-msg-issue-suffix
        args:
            - --jira localhost:1234 throwaway@dispostable.com
```
```yaml
-   repo: https://github.com/rnjesuz/add-msg-issue-suffix-hook
    rev: v0.2.0  # Use the ref you want to point at
    hooks:
    -   id: add-msg-issue-suffix
        args:
            - --jira https://jira.atlassian.com throwaway@dispostable.com
```

The code makes use of a keyring implementation to use credentials safely secured in your OS.<br>
See: https://github.com/jaraco/keyring

Use your preferred keyring implementation, or install the above one using: 
```bash
pip install keyring
```
Add an **API token** to the keyring, with your jira email. Store them in the `add-msg-issue-suffix-hook` groupname.<br>
You can use an existing API token, or create a new one in your Jira account settings.<br>
If you're using the above-mentioned keyring, do: 
```bash
keyring set add-msg-issue-suffix-hook your_jira_email
```
Example:
```bash
keyring set add-msg-issue-suffix-hook teste@notreal.nop
```
You will then be prompted to insert the API token.