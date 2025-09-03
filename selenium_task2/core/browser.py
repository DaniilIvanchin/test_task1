from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_task2.core.config_reader import ConfigReader


class Browser:
    _instance = None

    @classmethod
    def get_driver(cls, lang=None):
        if cls._instance is None:
            browser_cfg = ConfigReader.get("browser")
            name = browser_cfg.get("name", "chrome").lower()
            options_list = browser_cfg.get("options", [])

            if name == "chrome":
                service = Service(ChromeDriverManager().install())
                options = webdriver.ChromeOptions()
                for arg in options_list:
                    options.add_argument(arg)
                if lang:
                    options.add_argument(f"--lang={lang}")

                cls._instance = webdriver.Chrome(service=service, options=options)

            elif name == "firefox":
                cls._instance = webdriver.Firefox()

            else:
                raise ValueError(f"Browser '{name}' is not supported")

        return cls._instance

    @classmethod
    def quit(cls):
        if cls._instance:
            cls._instance.quit()
            cls._instance = None
