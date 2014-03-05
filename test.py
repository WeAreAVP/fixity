from Database import Database

db1 = Database()
db1.initProjectPathObj()
print(db1)
page_q =  db1.dbSession.query(db1.ProjectPathCls)

print(page_q)
SingleResult = page_q.get(1)

print(SingleResult.id)
exit()