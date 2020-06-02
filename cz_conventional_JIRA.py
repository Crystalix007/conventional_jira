import re

from commitizen.cz.base import BaseCommitizen
from commitizen.cz.utils import multiple_line_breaker, required_validator
from commitizen.cz.exceptions import CzException

class Conventional_jiraCz(BaseCommitizen):
    def questions(self) -> list:
        questions = [
            {
                "type": "list",
                "name": "prefix",
                "message": "Select the type of change you are committing",
                "choices": [
                    {
                        "value": "fix",
                        "name": "fix: A bug fix. Correlates with PATCH in SemVer",
                    },
                    {
                        "value": "feat",
                        "name": "feat: A new feature. Correlates with MINOR in SemVer",
                    },
                    {"value": "docs", "name": "docs: Documentation only changes"},
                    {
                        "value": "style",
                        "name": (
                            "style: Changes that do not affect the "
                            "meaning of the code (white-space, formatting,"
                            " missing semi-colons, etc)"
                        ),
                    },
                    {
                        "value": "refactor",
                        "name": (
                            "refactor: A code change that neither fixes "
                            "a bug nor adds a feature"
                        ),
                    },
                    {
                        "value": "perf",
                        "name": "perf: A code change that improves performance",
                    },
                    {
                        "value": "test",
                        "name": (
                            "test: Adding missing or correcting " "existing tests"
                        ),
                    },
                    {
                        "value": "build",
                        "name": (
                            "build: Changes that affect the build system or "
                            "external dependencies (example scopes: pip, docker, npm)"
                        ),
                    },
                    {
                        "value": "ci",
                        "name": (
                            "ci: Changes to our CI configuration files and "
                            "scripts (example scopes: GitLabCI)"
                        ),
                    },
                ],
            },
            {
                "type": "input",
                "name": "jira_issue",
                "message": ("JIRA issue. Of form $JIRA_Project$-$Issue_Number$:"),
                "filter": self.parse_jira_issues,
            },
            {
                "type": "input",
                "name": "subject",
                "filter": self.parse_subject,
                "message": (
                    "Subject. Concise description of the changes. "
                    "Imperative, lower case and no final dot:\n"
                ),
            },
            {
                "type": "confirm",
                "message": "Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer",
                "name": "is_breaking_change",
                "default": False,
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "Body. Motivation for the change and contrast this "
                    "with previous behavior:\n"
                ),
                "filter": multiple_line_breaker,
            },
            {
                "type": "input",
                "name": "footer",
                "message": (
                    "Footer. Information about Breaking Changes and "
                    "reference issues that this commit impacts:\n"
                ),
            },
        ]
        return questions

    def message(self, answers: dict) -> str:
        prefix = answers["prefix"]
        jira_issue = answers["jira_issue"]
        subject = answers["subject"]
        body = answers["body"]
        footer = answers["footer"]
        is_breaking_change = answers["is_breaking_change"]

        if jira_issue:
            jira_issue = f"({jira_issue})"
        if is_breaking_change:
            body = f"BREAKING CHANGE: {body}"
        if body:
            body = f"\n\n{body}"
        if footer:
            footer = f"\n\n{footer}"

        message = f"{prefix}{jira_issue}: {subject}{body}{footer}"

        return message

    def parse_jira_issues(self, text):
        if not text:
            return ""

        issues = text.strip().split(", ")
        issueRE = re.compile(r"\w+-\d+")

        for issue in issues:
            if not issueRE.fullmatch(issue):
                raise exceptions.InvalidAnswerError(f"JIRA scope of '{issue}' is invalid")

        if len(issues) == 1:
            return issues[0]

        return required_validator(", ".join(issues), msg="JIRA scope is required")


    def parse_subject(self, text):
        if isinstance(text, str):
            text = text.strip(".").strip()

        return required_validator(text, msg="Subject is required.")

    def example(self) -> str:
        return (
            "fix(JIRA-1): correct minor typos in code\n"
            "\n"
            "see the issue for details on the typos fixed\n"
            "\n"
            "closes issue #12"
        )

    def schema(self) -> str:
        return (
            "<type>(<jira_issue>): <subject>\n"
            "<BLANK LINE>\n"
            "(BREAKING CHANGE: )<body>\n"
            "<BLANK LINE>\n"
            "<footer>"
        )

    def schema_pattern(self) -> str:
        PATTERN = (
            r"(?m)(build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)"
            r"(\(\w+-\d+(, \w+-\d+)*\))?:\s[^A-Z][^\n]*?[^.\n]$\n\n(.|\n)*"
        )
        return PATTERN

class InvalidAnswerError(CzException):
    ...

discover_this = Conventional_jiraCz
