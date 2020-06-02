from setuptools import setup


setup(
    name="conventional_JIRA",
    version="0.2.2",
    py_modules=["cz_conventional_JIRA"],
    author = 'Michael Kuc',
    author_email = 'michaelkuc6@gmail.com',
    url = 'https://github.com/Crystalix007/conventional_jira',
    license="MIT",
    long_description="A variation of conventional commits enforcing a JIRA issue as the scope.",
    install_requires=["commitizen"],
)
