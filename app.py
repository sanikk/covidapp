import web
import dbhommat as dbh

from flask import Flask


dbh.initDB()
print(dbh.returnNumberOfLinesInDB())
app = Flask(__name__)

print(len(dbh.returnCountyNames()))
print(dbh.returnNumberOfLinesInDB()/len(dbh.returnCountyNames()))
# print(dbh.returnCountyNamesMatching("what"))
# print(dbh.returnMinDatesInDB())
