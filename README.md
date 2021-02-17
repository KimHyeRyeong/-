# 2020-internship

1. 2020 동기 백마인턴십 기간 동안 Grafana를 이용해 제작한 대시보드에 필요한 코드입니다. 

2. 각 파일 설명
 - database.py : 데이터베이스 연동에 필요한 초기화 작업을 진행.
 - api.py : 이미지를 처리하기위해 FastAPI를 이용한 파일. 
 - controller.py : 실행 파일. 사용자에게 필요한 정보를 입력받고 데이터 생성을 진행함.
 - model.py : 데이터베이스 테이블을 생성. 각 그래프를 표현할 데이터 생성 코드작성. 심볼과 평균 표현할 테이블을 생성하고 업데이트를 진행

 3. 실행 방법
 1. Grafana, Prometheus를 설치 후 실행, Grafana는  localhost:3000으로 접속합니다. 
 2. 준비된 json파일을 Grafana에서 import합니다.
 3. controller.py를 실행합니다. 사용할 DB와 데이터베이스 이름은 사용자마다 다를 수 있으므로 database.py에서 create_engine을 수정해야합니다.
 4. 이미지 실행을 위해서 fastAPI를 사용합니다. 터미널 창에 uvicorn api:app --reload를 입력하고 실행합니다.
 5. 사용자는 사용하고 싶은 이미지와 날짜 정보를 DB에 넣어 줄 수 있습니다. api.py에서 28번째 줄부터 수정할 수 있습니다. 
 6. 폰트 폴더 경로(71번째 줄)와 localhost로 구축한 이미지의 주소를 수정(generate_html함수안에서 작성한 html 코드)하여 사용하면 됩니다.
