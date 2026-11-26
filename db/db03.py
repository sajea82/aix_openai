import oracledb
import os
from dotenv import load_dotenv

load_dotenv()
ora_conn = os.getenv('ora_conn')
conn = oracledb.connect(ora_conn)

cursor = conn.cursor()
# insert
no = 2
name = '홍길순'
school = '디지털고'
height=190
kor = 90
eng=90
math=90
total=270
avg=90
specialty='python'
srank=''

# #------------------------------
# # 실행문 --- update
# sql = "delete stuscore2 where no=:no"
# cursor.execute(sql,no=2)
# cursor.close()
# #------------------------------


# #------------------------------
# # 실행문 --- update
# sql = "update stuscore2 set height=:height,specialty=:specialty\
#        where no!=:no"
# cursor.execute(sql,height=180,specialty='C',no=3)
# cursor.close()
# #------------------------------

#------------------------------
# 실행문 --- insert
in_list = [4,'홍홍홍','구로고']
sql = "insert into stuscore2 (no,name,school) values\
    (:1,:2,:3)"
cursor.execute(sql,in_list)
cursor.close()
#------------------------------


# #------------------------------
# # 실행문 --- insert
# sql = "insert into stuscore2 (no,name,school) values\
#     (:no,:name,:school)"
# cursor.execute(sql,no=3,name='홍길자',school='신림고')
# cursor.close()
# #------------------------------
conn.commit()   
conn.close()
print('프로그램 종료') 
