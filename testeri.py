import datetime

if __name__ == "__main__":
    pv = int(input("Päivä: "))
    kk = int(input("Kuukausi: "))
    vv = int(input("Vuosi: "))

    saika = datetime.datetime(vv, kk, pv)

    vertailu = datetime.datetime(1999, 12, 31)

    ero = vertailu - saika

    if ero.days >= 0:
        print("Olit " + str(ero.days) + " päivää vanha, kun vuosituhat vaihtui.")
    else:
        print("Et ollut syntynyt, kun vuosituhat vaihtui.")
