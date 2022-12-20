# vaihdetaan PostgreSQL tämä vielä
import sqlite3

import os
import csv
from datetime import datetime

import downloader

# SETUP FUNCTIONS


def initDB(dbname="vaccinations.db"):
    if not os.path.isfile(dbname):
        print("Database file not found, creating new one...")
        createDB()
        print("Done!")
        populateDatabase()


def createDB(dbname="vaccinations.db"):
    con, cur = returnConnection()
    cur.execute("CREATE TABLE vaccinations (name TEXT, fips INTEGER,state TEXT,date DATE,percentFullyVaccinated FLOAT,totalFully INTEGER, fully12plus INTEGER)")
    cur.execute(
        "CREATE TABLE cases (name TEXT, fips INTEGER, state TEXT, date DATE,cases INTEGER)")
    con.commit()
    con.close()

# näihin vielä async
# https://stackoverflow.com/questions/57126286/fastest-parallel-requests-in-python


def populateDatabase(vaccTiedosto="COVID-19_Vaccinations_in_the_United_States_County.csv", caseTiedosto="time_series_covid19_confirmed_US.csv"):
    if not os.path.isfile(vaccTiedosto):
        print("Vaccinations data file not found!")
        print("Fetching vaccination data from CDC, this will take a while.(very slow, sry)")
        downloader.fetchVaccData()
        print("Done!")
    if not os.path.isfile(caseTiedosto):
        print("Cases data file not found!")
        print("Fetching case data from Johns Hopkins, hosted at github.")
        downloader.fetchCaseData()
        print("Done!")
    print("populating vaccs table...")
    vaccinationReader(vaccTiedosto)
    print("populating cases table...")
    caseReader(caseTiedosto)
    print("Database populated!")


def returnConnection(dbname="vaccinations.db"):
    con = sqlite3.connect(dbname)
    return con, con.cursor()


def vaccinationReader(vaccTiedosto="COVID-19_Vaccinations_in_the_United_States_County.csv"):
    con, cur = returnConnection()
    with open(vaccTiedosto) as tiedosto:
        for rivi in csv.reader(tiedosto, delimiter=','):
            # skipataan toi eka rivi
            if rivi[0] == 'Date':
                continue
            if not rivi[7]:  # osasta puuttuu tää
                rivi[7] = 0
            name, fips, state, percentFullyVaccinated, totalFully, fully12plus = rivi[3], rivi[1], rivi[4], float(
                rivi[5]), int(rivi[6]), int(rivi[7])
            date = datetime.strptime(rivi[0], '%m/%d/%Y')
            cur.execute("INSERT INTO vaccinations VALUES (?,?,?,?,?,?,?)", (name,
                        fips, state, date, percentFullyVaccinated, totalFully, fully12plus))
    con.commit()
    con.close()


def caseReader(caseTiedosto="time_series_covid19_confirmed_US.csv"):
    # tässä vois heittää kaikki ennen 2020-12-13 pois (eli 13.12.20) tai sitten pistää filleriä sinne väliin.
    con, cur = returnConnection()
    with open(caseTiedosto) as tiedosto:
        for rivi in csv.reader(tiedosto, delimiter=','):
            # skipataan toi eka rivi mutta otetaan päivät talteen
            if rivi[0] == 'UID':
                paivamaarat = rivi[11:]
                paivamaarat = [datetime.strptime(
                    x, '%m/%d/%y') for x in paivamaarat]
                continue
            # muutama laitos joilla ei ole fips tunnistetta, skipataan ne (vankilat ym) koska ei ole muutakaan dataa niille
            if not rivi[4]:
                continue
            name, fips, state = rivi[5], int(rivi[4].split('.')[0]), rivi[6]
            laskuri = 11
            while laskuri < len(rivi):
                pvm = paivamaarat[laskuri - 11]
                cases = rivi[laskuri]
                cur.execute("INSERT INTO cases VALUES (?,?,?,?,?)",
                            (name, fips, state, pvm, cases))
                laskuri += 1
    con.commit()
    con.close()

# SEARCH FUNCTIONS


def returnListOfFIPSOverCutoffValue(cutoff: int):
    con, cur = returnConnection()
    # if not cutoff or cutoff > 100 or cutoff < 0:
    #    return None
    fipsit = cur.execute("SELECT DISTINCT fips FROM vaccinations WHERE percentFullyVaccinated>:value", {
                         "value": cutoff}).fetchall()
    fipsit = [rivi[0] for rivi in fipsit]
    con.close()
    return fipsit


def returnAllRowsOfCountiesOnList(lista: list):
    con, cur = returnConnection()
    sql = f"SELECT * FROM vaccinations WHERE fips in ({','.join(['?']*len(lista))})"
    # print(sql)
    vastaus = cur.execute(sql, lista).fetchall()
    con.close()
    return vastaus


def returnMaxDatesInDB():
    con, cur = returnConnection()
    sql = f"SELECT MAX(date) FROM vaccinations"
    vaccpvm = cur.execute(sql).fetchone()
    sql = f"SELECT MAX(date) FROM cases"
    casespvm = cur.execute(sql).fetchone()
    con.close()
    return casespvm[0], vaccpvm[0]


def returnMinDatesInDB():
    con, cur = returnConnection()
    sql = f"SELECT MIN(date) FROM vaccinations"
    vaccpvm = cur.execute(sql).fetchone()
    sql = f"SELECT MIN(date) FROM cases"
    casespvm = cur.execute(sql).fetchone()
    con.close()
    return casespvm[0], vaccpvm[0]


def returnCountyNames():
    con, cur = returnConnection()
    sql = f"SELECT DISTINCT name FROM Vaccinations"
    result = cur.execute(sql).fetchall()
    return [x[0] for x in result]


def returnCountyNamesMatching(searchfor: str):
    con, cur = returnConnection()
    searchfor = "%"+searchfor+"%"
    sql = f"SELECT DISTINCT name FROM Vaccinations WHERE name LIKE :searchfor"
    result = cur.execute(sql, {"searchfor": searchfor}).fetchall()
    return [x[0] for x in result]


# jotain dev rutiineja:

# def returnAllRowsOfCountyOverCutoffValue(self,cutoff:int):
#        con,cur = self.returnConnection()
#        vastaus = cur.execute("SELECT * FROM vaccinations WHERE fips in (SELECT DISTINCT fips FROM vaccinations WHERE percentFullyVaccinated>:value)", {"value":cutoff}).fetchall()
#        con.close()
#        return vastaus

#    def returnNameOfCountyByFIPS(self,fips:int):
#        con,cur = self.returnConnection()
#        vastaus = cur.execute("SELECT name FROM vaccinations WHERE FIPS=:fips", {"fips":fips}).fetchone()
#        con.close()
#         return vastaus

# def sortByCountyAndDate(lista:list):
#    lista.sort(key=lambda rivi: (rivi[0],rivi[2],-1 * rivi[3]))

def returnNumberOfLinesInDB():
    con, cur = returnConnection()
    return cur.execute("SELECT COUNT(*) FROM vaccinations").fetchone()[0] + cur.execute("SELECT COUNT(*) FROM cases").fetchone()[0]
