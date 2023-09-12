""" Module for initializing the driver. """
import pytest
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class Initialization:

    @pytest.fixture(autouse=True)
    def init_driver(self, command_line_arguments: dict):
        """
        Initialize the driver and yield it to the test.

        Args:
            command_line_arguments (dict): Command line arguments.

        Raises:
            KeyError: If the browser is not found.

        Yields:
            Iterator[webdriver]: A webdriver instance.
        """
        AVAILABLE_BROWSERS = {'chrome': self.chrome, 'firefox': self.firefox,}

        browser = command_line_arguments['browser']
        location = command_line_arguments["location"]
        headless = command_line_arguments['headless']
        full_screen = command_line_arguments['full_screen']

        try:
            browser = AVAILABLE_BROWSERS[browser]

        except KeyError:
            raise KeyError(f"Browser {browser} not found.")
        
        web_driver = browser(location, headless)

        if full_screen:
            web_driver.maximize_window()

        self.driver = web_driver

        try:
            start_time = time.time()
            print(f'Start test at: {datetime.now()}')
            yield web_driver
            print(f'\nTest duration: {time.time() - start_time}')
        finally:
            # Tear down
            web_driver.close()
            web_driver.quit()
    
    def firefox(self, where: str, headless: bool = False) -> webdriver.Firefox:
        """
        Returns a Firefox driver instance.

        Args:
            where (str): Path to the geckodriver executable.
            headless (bool, optional): Whether to run the browser in headless mode. Defaults to False.

        Returns:
            webdriver.Firefox: A Firefox driver instance.
        """
        firefox_opt = webdriver.FirefoxOptions()
        if where == 'local':           
            if headless:
                firefox_opt.add_argument("--headless")

            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_opt)
        
        else:
            return webdriver.Remote(
                command_executor="http://firefox:4444", options=firefox_opt
                # default firefox container or any other container port is 4444  
            )


    def chrome(self, where: str, headless: bool = False) -> webdriver.Chrome:
        """
        Returns a Chrome driver instance.

        Args:
            headless (bool, optional): Whether to run the browser in headless mode. Defaults to False.

        Returns:
            webdriver.Chrome: A Chrome driver instance.
        """
        chrome_opt = webdriver.ChromeOptions()
        if where == 'local':              
            if headless:
            
                chrome_opt.add_argument("--headless")            
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_opt)
        
        else:
            return webdriver.Remote(
                command_executor="http://chrome:4444", options=chrome_opt 
                # any container default port is 4444  
            )   