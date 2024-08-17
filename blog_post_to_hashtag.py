# 자연어로 작성된 blog_post를 llm을 통해 hashtag로 키워드만 추출
from dotenv import load_dotenv

from langchain import hub
from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv(override=True)

llm = ChatUpstage(
      base_url="https://api.upstage.ai/v1/solar"
)

class HashTag(BaseModel):
    restaurant: str = Field(
        description="포스트 작성자가 방문한 모든 음식점 정보."
    )
    cafe: str = Field(
        description="포스트 작성자가 방문한 모든 카페 정보입니다."
    )
    tourist_spot: str = Field(
        description="포스트 작성자가 방문한 모든 관광지 정보입니다. 공항, 편의점, 대형마트, 렌트카업체 등은 제외해주세요."
    )
    companion: str = Field(
        description="포스트 작성자의 동행 정보 Enum: '혼자', '친구', '가족', '연인', '부모님', '아이', '반려견'"
    )
    theme: str = Field(
        description="포스트 작성자의 여행 테마 Enum: '로맨틱', '레포츠', '쇼핑', '맛집투어', '카페투어', '빵지순례', '힐링'"
    )

parser = JsonOutputParser(pydantic_object=HashTag)

extract_place_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                너는 제주도 여행 블로그 포스트를 읽고 해시태그를 추출하는 Assistance이다.
                작성된 제주도 블로그 포스트를 읽고, 해당 블로그 포스트 작성자가 방문한 '식당', '카페', '관광지정보', '동행정보' 해시태그를 추출해주세요.
                
                추출 예시를 지켜 해시태그를 추출해주세요.

                추출예시:
                '관광지' - #애월카페거리 #애월해안도로 #협재해수욕장 #중문해안도로 #천지연폭포 #사려니숲길 #동문올레시장
                '식당' - #숙성도 #연돈 #우진해장국 #미영이네식당 #오는정김밥 #자매국수 #고집돌우럭
                '카페' - #델문도 #카페코지 #카페바람 #섬앤썸 #파우커피파티
                '동행정보' - #부모님 #연인 #친구 #혼자 #가족 #아이 #반려견
                '테마' - #로맨틱 #레포츠 #쇼핑 #맛집투어 #카페투어 #빵지순례 #힐링
                
            #제주도 #제주여행 #제주도여행 #제주도맛집 #제주도카페 #제주도관광 #제주도풍경 #제주도힐링 과 같은 구체적이지 않은 해시태그는 추출하지 않도록 합니다.
            #하나로마트 #편의점 #이마트 #농협 #렌트카업체 등과 같은 일상적인 장소는 추출하지 않도록 합니다.
            
            동행정보는 '혼자' '친구' '가족' '연인' '부모님' '아이' '반려견' 중 하나로 선택해주세요.
            테마는 '로맨틱' '레포츠' '쇼핑' '맛집투어' '카페투어' '빵지순례' '힐링' 중 하나로 선택해주세요.

            각 카테고리별(관광지,식당,카페,동행정보,테마)로 추출할 해시태그가 없는 경우에는 X 로 표기해주세요.

            아래는 제주도 여행 블로그 포스트입니다.
            {context}
            """,
        ),
    ]
)

extract_chain = extract_place_prompt | llm | StrOutputParser()
