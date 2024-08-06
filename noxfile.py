import nox

@nox.session
def lint(session):
    session.install("ruff")
    session.run("ruff", "meemirobotti")

@nox.session
def isort(session):
    session.install("isort")
    session.run("isort", "meemirobotti")

@nox.session
def test(session):
    session.install("pytest")
    session.run("pytest")

@nox.session(tags=["security"])
def pip_audit(session):
    session.install("pip-audit")
    session.run("pip-audit", "-r", "requirements/requirements.txt")

@nox.session(tags=["security"])
def bandit(session):
    session.install("bandit")
    session.run("bandit", "-r", "meemirobotti")

