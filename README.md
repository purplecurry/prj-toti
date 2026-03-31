1. 실행방법
- python bgm-import.py로 bgms 내부의 음원을 db에 등록 (음원 추가시에 다시 실행하면 자동 추가됨 (파일 이름 기준)
- 이 후 uvicorn으로 main.py 구동
  
2. .env 필요 내용
- 필수내용
- DATABASE_URL
- GOOGLE_API_KEY

- 테스트용 코드가 포함 된 상태
- SECRET_KEY
- ACCESS_TOKEN_EXPIRE_HOURS

