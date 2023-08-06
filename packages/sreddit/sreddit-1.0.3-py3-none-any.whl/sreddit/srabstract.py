from get_chrome_driver import GetChromeDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from abc import ABC, abstractmethod

class SubRedditScraper(ABC):
    """
    A tool for scraping content from a subreddit
    """

    def __init__(self, subreddit: str, keywords: list = None, 
                 show_progress: bool = True, make_db: bool = True, 
                 db_name: str = "subreddit_info.db", scroll_time: int = 1) -> None:
        """
        Initializes a SubRedditScraper.

        Args:
            subreddit: the name of the subreddit to be scraped
            keywords: list of words to look out for in the subreddit
            show_progress: if the progress should be shown in the terminal
            make_db: if a database of the information found should be created
            scroll_time: time to wait between each scroll so page can load
        """
        # general
        self.subreddit = subreddit
        self.show_progress = show_progress
        if keywords == None:
            keywords = []
        self.keywords = keywords

        # database
        self.make_db = make_db
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.setup_database()

        # browser
        self.browser = None
        self.setup_browser()
        self.scroll_time = scroll_time
        self.scroll_height = self.browser.execute_script("return document.body.scrollHeight")


    def setup_browser(self) -> None:
        """
        Downloads and configures the browser (webdriver) with default settings
        """
        get_driver = GetChromeDriver() 
        get_driver.install()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)
        self.browser = webdriver.Chrome(options=chrome_options)


    def navigate_to_subreddit(self) -> None:
        """
        Navigates to the subreddit if it exists.

        Raises:
            Exception: if the subreddit cannot be found
        """
        assert len(self.subreddit) > 0, "Subreddit name cannot be empty"

        try:
            self.browser.get(f"https://www.reddit.com/r/{self.subreddit}")
        except:
            raise Exception("Subreddit could not be found")


    def scroll_page(self) -> bool:
        """
        Scrolls down the page dynamically after waiting for the page to load

        Returns:
            False: if the end of the subreddit page has been reached
        """
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(self.scroll_time)

        new_height = self.browser.execute_script("return document.body.scrollHeight")
        old_height = self.scroll_height
        self.scroll_height = new_height
        return new_height == old_height
           
    
    @abstractmethod
    def setup_database(self) -> None:
        """
        Creates a new .db file, if one doesn't already exist, to hold the information 
        found in the subreddit.
        """
        pass
    

    @abstractmethod
    def gather_content(self) -> None:
        """
        Gathers the desired content from the subreddit (e.g titles, body content, etc)
        """
        pass


    @abstractmethod
    def clean_content(self, raw_content: list, use_keywords: bool) -> None:
        """
        Cleans the content found by converting them into text and looking for keywords
        if required.

        Args:
            raw_content: the content in raw, web-element, format
            use_keywords: whether, or not, keywords are necessary in the content
        """
        pass


    @abstractmethod
    def add_to_db(self) -> None:
        """
        Adds the content found to the database
        """
        pass
    

    @abstractmethod
    def run(self) -> None:
        """
        Runs the scraper and finds the information
        """
        pass