import os
from dotenv import load_dotenv

from utils.daum_search import DaumSearcher
from utils.naver_blog_crawler import BlogContentFetcher

load_dotenv()

if __name__ == "__main__":
    KAKAO_API_KEY = os.getenv('KAKAO_REST_API_KEY')
    SEARCH_KEYWORD = "제주도 여행"
    INCLUDE_URL = "blog.naver"

    daum_searcher = DaumSearcher(api_key=KAKAO_API_KEY)
    naver_blog_url_list = daum_searcher.get_all_urls(SEARCH_KEYWORD, INCLUDE_URL)

    blog_content_fetcher = BlogContentFetcher()
    for idx, url in enumerate(naver_blog_url_list):
        blog_content_fetcher.fetch_blog_content(
            link=url, directory_path=SEARCH_KEYWORD
        )
    blog_content_fetcher.quit_browser()