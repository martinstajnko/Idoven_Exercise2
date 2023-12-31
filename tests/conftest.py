import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="browser: chrome or firefox"
    )
    parser.addoption(
        "--location", action="store", default="local" # local | remote
    ) 
    parser.addoption(
        "--headless", action="store", default=False, help="headless: true or false"
    )
    parser.addoption(
        "--full_screen", action="store", default=False, help="full_screen: true or false"
    )


@pytest.fixture
def command_line_arguments(request):
    return {
        "browser": request.config.getoption("--browser"),
        "location": request.config.getoption("--location"),
        "headless": request.config.getoption("--headless"),
        "full_screen": request.config.getoption("--full_screen"),
    }