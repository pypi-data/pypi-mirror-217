import nox

PYTHON_ALL_VERSIONS = ["3.8", "3.9", "3.10", "3.11"]


# PYTHON_DEFAULT_VERSION="3.11"
@nox.session(python=PYTHON_ALL_VERSIONS)
def test(session):
    session.install("-e", ".")
    session.install("-r", "test_requirements.txt")
    session.run("pytest", "-sv", "tests")
