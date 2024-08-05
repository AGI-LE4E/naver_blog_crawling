import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class BlogContentFetcher:
    def __init__(self, headless=True):
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument("--headless")
        self.browser = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=self.options
        )

    def fetch_blog_content(self, link: str, directory_path:str=".") -> bool:
        """Naver 블로그의 본문 내용을 수집합니다.

        Args:
            link (str): naver 블로그의 URL
            directory_path (str, optional): 파일이 저장 될 경로. Defaults to ".".

        Returns:
            bool: 성공여부
        """
        try:
            self.browser.get(link)
            time.sleep(2)
            self.browser.switch_to.frame("mainFrame")
            time.sleep(1)
            main_title = self.browser.find_element(By.CSS_SELECTOR, "div.se-title-text").text
        
            try:
                main_text = self.browser.find_element(By.CSS_SELECTOR, "div.se-main-container").text
            except NoSuchElementException:
                main_text = self.browser.find_element(By.CSS_SELECTOR, "div#content-area").text

            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            with open(f'{directory_path}/{main_title.replace("/", "_")}___{link.split("/")[-1]}.txt', 'w') as f:
                f.write(main_text)

            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False


    def quit_browser(self):
        self.browser.quit()