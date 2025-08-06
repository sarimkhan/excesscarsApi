from fastapi import FastAPI
import psycopg2
app = FastAPI()
import json

connectionString = 'postgresql://neondb_owner:npg_O2IgKtHQMnB0@ep-rough-paper-afrptwb3-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
conn = psycopg2.connect(connectionString)

#initiaite Connection Object
cur = conn.cursor()

#Code goes here
def getAllVehicles():
    cur.execute("SELECT * FROM vehicles;")
    tableVals = cur.fetchall()
    return tableVals;

def getFIlteredVehicles(minYear = "", maxYear = ""):
    minyearString = "SELECT * FROM vehicles" + " WHERE CAST(caryear AS INT) >= CAST(" + minYear + " AS INT);"
    maxyearString = "SELECT * FROM vehicles" + " WHERE CAST(caryear AS INT) <= CAST(" + maxYear + " AS INT);"
    minmaxString = "SELECT * FROM vehicles" + " WHERE CAST(caryear AS INT) <= CAST(" + maxYear + " AS INT) AND CAST(caryear AS INT) >= CAST(" + minYear + " AS INT);"
    if(minYear != "" and maxYear == ""):
        cur.execute(minyearString)
    if(minYear == "" and maxYear != ""):
        cur.execute(maxyearString) 
    if(minYear != "" and maxYear != ""):
        cur.execute(minmaxString)    
    tableVals = cur.fetchall()
    return tableVals;
print(len(getFIlteredVehicles("2018","2022")))
#commit changes
#conn.commit()



fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/getFilteredVehicles/")
async def read_item(minYear: str = "", maxYear: str = ""):
    return getFIlteredVehicles(minYear, maxYear)

@app.get("/getAllVehicles/")
async def read_item():
    return getAllVehicles()