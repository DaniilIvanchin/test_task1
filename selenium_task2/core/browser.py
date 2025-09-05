from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_task2.core.config_reader import ConfigReader


class BrowserType(str, Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"


DEFAULT_BROWSER = BrowserType.CHROME


class Browser:
    _instance = None

    @classmethod
    def get_driver(cls, lang=None):
        if cls._instance is None:
            config = ConfigReader.load_config()
            browser_cfg = config["browser"]

            name = browser_cfg["name"].lower()
            options_list = browser_cfg.get("options", [])

            if not lang:
                languages = browser_cfg.get("languages", [])
                if languages:
                    lang = languages[0]

            if name == BrowserType.CHROME.value:
                service = Service(ChromeDriverManager().install())
                options = webdriver.ChromeOptions()
                for arg in options_list:
                    options.add_argument(arg)
                if lang:
                    options.add_argument(f"--lang={lang}")

                cls._instance = webdriver.Chrome(service=service, options=options)

            elif name == BrowserType.FIREFOX.value:
                cls._instance = webdriver.Firefox()

            else:
                raise ValueError(
                    f"Browser '{name}' is not supported. "
                    f"Use one of: {[b.value for b in BrowserType]}"
                )

        return cls._instance

    @classmethod
    def quit(cls):
        if cls._instance:
            cls._instance.quit()
            cls._instance = None
