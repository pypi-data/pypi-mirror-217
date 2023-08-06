import sqlite3
from selenium.webdriver.common.by import By
from srabstract import SubRedditScraper

class SubRedditBodies(SubRedditScraper):
    """
    A tool for scraping post bodies from a subreddit
    """

    def __init__(self, subreddit: str, keywords: list = None, 
                 show_progress: bool = True, make_db: bool = True, 
                 db_name: str = "subreddit_info.db", scroll_time: int = 1.25) -> None:
        """
        Initializes a SubRedditBodies.

        Args:
            subreddit: the name of the subreddit to be scraped
            keywords: list of words to look out for in the subreddit
            show_progress: if the progress should be shown in the terminal
            make_db: if a database of the bodies found should be created
            scroll_time: time to wait between each scroll so page can load
        """
        super().__init__(subreddit, keywords, show_progress, make_db, db_name, scroll_time)
        self.bodies = set()


    # OVERRIDE
    def setup_database(self) -> None:
        """
        Creates a new .db file, if one doesn't already exist, to hold the bodies 
        found in the subreddit.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        createTable = """CREATE TABLE IF NOT EXISTS
        srbodies(id INTEGER PRIMARY KEY autoincrement, body TEXT)"""
        self.cursor.execute(createTable)


    # OVERRIDE
    def gather_content(self) -> None:
        """
        Gathers a list of bodies of each post on the subreddit.
        """
        self.navigate_to_subreddit()
        use_keywords = len(self.keywords) != 0

        while True:
            # TODO: potentially add more class names for more body text (?)
            raw_bodies = self.browser.find_elements(By.CLASS_NAME, "_1qeIAgB0cPwnLhDF9XSiJM")
            self.clean_content(raw_bodies, use_keywords)
            end_reached = self.scroll_page()
            if (end_reached):
                break
            else:
                continue


    # OVERRIDE
    def clean_content(self, raw_content: list, use_keywords: bool) -> None:
        """
        Cleans the bodies found by converting them into text and looking for keywords
        if required.

        Args:
            raw_content: the bodies in raw, web-element, format
            use_keywords: whether, or not, keywords are necessary in the bodies  
        """
        body_count = 0

        for raw_body in raw_content:
            text_body = raw_body.text
            # validate body content
            if (len(text_body) > 0 
                and ((use_keywords and any(word in text_body for word in self.keywords))
                    or not use_keywords)):
                self.bodies.add(text_body)
                # update progress
                if self.show_progress:
                    body_count +=1 
                    
            # display progress
            print(f"Valid Bodies Found: {body_count}", end="\r")


    # OVERRIDE
    def add_to_db(self) -> None:
        """
        Adds the found bodies to the database
        """
        for body in self.bodies:
            self.cursor.execute("INSERT INTO {table_name} (body) VALUES(?)"
                                .format(table_name='srbodies'),(body,))
        self.conn.commit()


    # OVERRIDE
    def run(self) -> None:
        """
        Runs the scraper and finds all the bodies
        """
        self.gather_content()
        if self.make_db:
            self.add_to_db()
            print(f"Bodies added to {self.db_name}")
        else:
            for body in self.bodies:
                print(body + "\n")


SubRedditBodies("twilight").run()