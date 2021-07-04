import pymysql
# 连接database
conn = pymysql.connect(
    host="198.13.47.120",
    port=3306,
    user="teach",password="B6twdJ2pXh3Z3pdz",
    database="test",
    charset="utf8")
cursor = conn.cursor()
# 创建user表:
print(cursor)
cursor.close()
conn.close()
