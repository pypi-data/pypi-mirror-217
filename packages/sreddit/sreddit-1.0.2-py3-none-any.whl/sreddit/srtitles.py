import sqlite3
from selenium.webdriver.common.by import By
from srabstract import SubRedditScraper

class SubRedditTitles(SubRedditScraper):
    """
    A tool for scraping post titles from a subreddit
    """

    def __init__(self, subreddit: str, keywords: list = None, 
                 show_progress: bool = True, make_db: bool = True, 
                 db_name: str = "subreddit_info.db", scroll_time: int = 1) -> None:
        """
        Initializes a SubRedditTitles.

        Args:
            subreddit: the name of the subreddit to be scraped
            keywords: list of words to look out for in the subreddit
            show_progress: if the progress should be shown in the terminal
            make_db: if a database of the titles found should be created
            scroll_time: time to wait between each scroll so page can load
        """
        super().__init__(subreddit, keywords, show_progress, make_db, db_name, scroll_time)
        self.titles = set()

    
    # OVERRIDE
    def setup_database(self) -> None:
        """
        Creates a new .db file, if one doesn't already exist, to hold the titles 
        found in the subreddit.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        createTable = """CREATE TABLE IF NOT EXISTS
        srtitles(id INTEGER PRIMARY KEY autoincrement, title TEXT)"""
        self.cursor.execute(createTable)


    # OVERRIDE
    def gather_content(self) -> None:
        """
        Gathers a list of titles of each post on the subreddit.
        """
        self.navigate_to_subreddit()
        use_keywords = len(self.keywords) != 0

        while True:
            raw_titles = self.browser.find_elements(By.CLASS_NAME, "_eYtD2XCVieq6emjKBH3m")
            self.clean_content(raw_titles, use_keywords)
            end_reached = self.scroll_page()
            if (end_reached):
                break
            else:
                continue


    # OVERRIDE
    def clean_content(self, raw_content: list, use_keywords: bool) -> None:
        """
        Cleans the titles found by converting them into text and looking for keywords
        if required.

        Args:
            raw_content: the titles in raw, web-element, format
            use_keywords: whether, or not, keywords are necessary in the titles
        """
        title_count = 0

        for raw_title in raw_content:
            text_title = raw_title.text
            # validate title
            if (len(text_title) > 0 
                and ((use_keywords and any(word in text_title for word in self.keywords))
                    or not use_keywords)):
                self.titles.add(text_title)
                # update progress
                if self.show_progress:
                    title_count +=1 
                    
            # display progress
            print(f"Valid titles Found: {title_count}", end="\r")


    # OVERRIDE
    def add_to_db(self) -> None:
        """
        Adds the found titles to the database
        """
        for title in self.titles:
            self.cursor.execute("INSERT INTO {table_name} (title) VALUES(?)"
                                .format(table_name='srtitles'),(title,))
        self.conn.commit()


    # OVERRIDE
    def run(self) -> None:
        """
        Runs the scraper and finds all the titles
        """
        self.gather_content()
        if self.make_db:
            self.add_to_db()
            print(f"Titles added to {self.db_name}")
        else:
            for title in self.titles:
                print(title + "\n")

