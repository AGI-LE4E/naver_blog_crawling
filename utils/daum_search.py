import os
import requests
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class DaumSearcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"Authorization": f"KakaoAK {self.api_key}"}
        self.base_url = "https://dapi.kakao.com/v2/search/blog"
    
    def search_naver_blog(self, query: str, sort: str = "accuracy", page: int = 1, size: int = 50) -> Dict:
        """
        Kakao 블로그 검색 API를 사용하여 블로그 정보를 검색합니다.

        Parameters:
            query (str): 검색할 쿼리
            sort (str): 정렬 방법 (accuracy, recency)
            page (int): 페이지 번호
            size (int): 한 페이지에 표시할 레코드 수

        Returns:
            Dict: API 응답을 포함하는 딕셔너리
        """
        params = {"sort": sort, "page": page, "size": size, "query": query}
        response = requests.get(self.base_url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {"Error": response.status_code}

    def get_all_urls(self, query: str, include_url: str, size: int = 20) -> List[str]:
        """
        URL을 수집합니다.

        Parameters:
            query (str): 검색할 쿼리
            include_url (str): 포함될 URL 필터링 문자열
            size (int): 한 페이지에 표시할 레코드 수

        Returns:
            List[str]: URL 목록
        """
        page = 1
        naver_blog_urls = []

        while True:
            result = self.search_naver_blog(query, page=page, size=size)
            if 'Error' in result:
                print(f"Error occurred: {result['Error']}")
                break

            filtered_urls = [
                doc["url"] for doc in result["documents"] if include_url in doc["url"]
            ]
            naver_blog_urls.extend(filtered_urls)

            if len(result["documents"]) < size or page * size >= result["meta"]["pageable_count"]:
                break

            page += 1

        return naver_blog_urls

