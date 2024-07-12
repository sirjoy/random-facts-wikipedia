"""Nox sessions."""
import nox


nox.options.sessions = "lint", "safety", "tests", "mypy"


locations = "src", "tests", "noxfile.py"


supported_python_versions = ["3.10", "3.9"]


def install_dependencies(session, *args):
    """Install packages"""
    session.install("-e", ".")
    session.install(*args)


@nox.session(python=["3.10", "3.9"])
def tests(session):
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    install_dependencies(
        session,
        "coverage[toml]",
        "pytest",
        "pytest-cov",
        "pytest-mock",
    )
    session.run("pytest", *args)


@nox.session(python=["3.10", "3.9"])
def lint(session):
    """Lint using flake8."""
    args = session.posargs or locations
    install_dependencies(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python="3.10")
def black(session):
    """Run black code formatter."""
    args = session.posargs or locations
    install_dependencies(session, "black")
    session.run("black", *args)


@nox.session(python="3.10")
def safety(session):
    """Scan dependencies for insecure packages."""
    install_dependencies(session, "safety")
    session.run("safety", "check", "--full-report")


@nox.session(python=supported_python_versions)
def mypy(session):
    """Type-check using mypy."""
    args = session.posargs or locations
    install_dependencies(session, "mypy")
    session.run("mypy", *args)


@nox.session(python="3.10")
def pytype(session):
    """Run the static type checker."""
    args = session.posargs or ["--disable=import-error", *locations]
    install_dependencies(session, "pytype")
    session.run("pytype", *args)
