from dotenv import load_dotenv

load_dotenv("tests/test.env")


pytest_plugins = [
    "tests.fixture.client",
    "tests.fixture.database",
]
