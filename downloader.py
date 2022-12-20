import requests
#cases by county
#https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv?raw=true

#vaccination data
#https://data.cdc.gov/api/views/8xkx-amqh/rows.csv?accessType=DOWNLOAD
def httpcall(osoite:str,*args):
    # payload = {key1:value1, key2:value2}
    r = requests.get(osoite)#, params=payload)
    print(r.url)
    return r.text #palauttaa nyt kaiken

def fetchVaccData():
    return httpcall("https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv?raw=true")

def fetchCaseData():
    return httpcall("https://data.cdc.gov/api/views/8xkx-amqh/rows.csv?accessType=DOWNLOAD")
