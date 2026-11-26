import os
import oracledb
from dotenv import load_dotenv

# 1. 불러오기
load_dotenv()
ora_conn = os.getenv('ora_conn')

# 2. db연결
conn = oracledb.connect(ora_conn)
cursor = conn.cursor()

# 3. 쿼리작성실행
# employees,emprank non-equi join를 사용해서\
# 월급의 등급을 출력하시오.
# emp_name,salary,erank,low_salary,high_salary,hire_date
# -- 0-3999     E등급
# -- 4000-6999  D
# -- 7000-9999  C
# -- 10000-11999   B
# -- 12000 - 30000 A등급

# 디장고 -> html key, value 전달됨.(dict타입변환)
sql = '''
select name,kor+eng+math total,sw from stuscore
'''
cursor.execute(sql)

# 컬럼명을 추출
columns = [col[0] for col in cursor.description]

# 4. 데이터정보전달
rows = cursor.fetchall()

# 4-2. 딕셔너리 형태로 변환
rows = [ dict(zip(columns,row)) for row in rows ]
print(rows)
context={'stulist':rows}

# return render('index.html',context)

# # 5. 데이터출력
# for row in rows:
#     print(*row)
    # print(row[0],row[1],row[2],row[3])

# 5-2. insert,update,delete할 경우
# insert - board
# insert - file1
# insert - file2
# insert - file3
# conn.commit()
# conn.rollback()

# 6. db정보 닫기
cursor.close()
conn.close()