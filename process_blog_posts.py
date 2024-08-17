import glob
import json

from langchain_community.document_loaders import TextLoader

from blog_post_to_hashtag import extract_chain

cnt = 0
if __name__ == "__main__":
    file_paths = glob.glob("./제주도 여행/*.txt")
    output_file = "hashtag.json"

    for file_path in file_paths:
        try:
            # 기존 데이터 찾기
            try:
                with open(output_file, "r", encoding="utf-8") as f:
                    my_json = json.load(f)
            except FileNotFoundError:
                my_json = {}


            blog_post = TextLoader(file_path).load()
            
            # 이미 처리된 파일
            if file_path in my_json:
                print(f"Already processed: {file_path}")
                continue

            # LLM 으로 해시태그 생성
            result = extract_chain.invoke({"context": blog_post})

            # 결과를 저장
            my_json[file_path] = result
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(my_json, f, ensure_ascii=False, indent=4)
            print(f"Processed: {file_path}")

        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    print("Processing complete.")
