from dotenv import load_dotenv

load_dotenv(dotenv_path="tests/test.env", verbose=True)


pytest_plugins = [
    "tests.fixture.client",
    "tests.fixture.database",
]
