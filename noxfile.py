import nox

nox.options.sessions = "lint", "safety", "tests"

locations = "src", "tests", "noxfile.py"

def install_dependencies(session, *args):
    session.install("-e", ".")
    session.install(*args)

@nox.session(python=["3.10", "3.9"])
def tests(session):
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
    args = session.posargs or locations
    install_dependencies(
        session,
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)

@nox.session(python="3.10")
def black(session):
    args = session.posargs or locations
    install_dependencies(session, "black")
    session.run("black", *args)

@nox.session(python="3.10")
def safety(session):
    install_dependencies(session, "safety")
    session.run("safety", "check", "--full-report")