import oracledb
import os
from dotenv import load_dotenv

load_dotenv()
ora_conn = os.getenv('ora_conn')
conn = oracledb.connect(ora_conn)
cursor = conn.cursor()

# 검색
# kor_loan_status테이블에서
# 지역별로 그룹핑 후, 주택담보대출을 출력하시오.

#------------------------------
# 실행문 --- select
sql = f'''
select region,sum(loan_jan_amt) as amt 
from kor_loan_status
where gubun='주택담보대출'
group by region
'''
cursor.execute(sql)

rows = cursor.fetchall()
print(f'지역\t담보대출')
print('-'*40)
for row in rows:
    print('{}\t{}'.format(*row))

#------------------------------

conn.close()