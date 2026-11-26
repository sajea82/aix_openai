import oracledb
import os
from dotenv import load_dotenv

load_dotenv()
ora_conn = os.getenv('ora_conn')
conn = oracledb.connect(ora_conn)

cursor = conn.cursor()
# 국어,영어,수학 : 역순정렬로 정렬하시오.
while True:
    input_data = input('정렬할 과목을 입력하세요.>> ')
    if input_data.strip() == '국어': i = 'kor'
    elif input_data.strip() == '영어': i = 'eng'
    else: i='math'
    
    # 실행문
    sql = f"select * from stuscore order by {i} desc"
    cursor.execute(sql)

    rows = cursor.fetchall()
    print(rows)
    print("인원 : ",len(rows))
cursor.close()
print('프로그램 종료')    
