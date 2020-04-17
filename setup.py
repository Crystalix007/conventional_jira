from setuptools import setup


setup(
    name="conventional_JIRA",
    version="0.1.0",
    py_modules=["cz_conventional_JIRA"],
    license="MIT",
    long_description="A variation of conventional commits enforcing a JIRA issue as the scope.",
    install_requires=["commitizen"],
)
