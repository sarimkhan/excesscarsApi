from fastapi import FastAPI
import psycopg2
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
import json


origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
connectionString = 'postgresql://neondb_owner:npg_O2IgKtHQMnB0@ep-rough-paper-afrptwb3-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
conn = psycopg2.connect(connectionString)

#initiaite Connection Object
cur = conn.cursor()

#Get Code goes here
def getAllVehicles():
    cur.execute("SELECT * FROM vehicles;")
    tableVals = cur.fetchall()
    return tableVals;
def getAllVehicleWithVIN(vin=""):
    cur.execute("SELECT * FROM vehicles WHERE vin = '" + str(vin) + "';")
    tableVals = cur.fetchall()
    return tableVals;
def getFIlteredVehicles(minYear = "", maxYear = "", make = "", model = "", minPrice = "", maxPrice = "", miles = "", body = ""):
    minyearString = "SELECT * FROM vehicles" + " WHERE CAST(caryear AS INT) >= CAST(" + minYear + " AS INT);"
    maxyearString = "SELECT * FROM vehicles" + " WHERE CAST(caryear AS INT) <= CAST(" + maxYear + " AS INT);"
    minmaxString = "SELECT * FROM vehicles" + " WHERE CAST(caryear AS INT) <= CAST(" + maxYear + " AS INT) AND CAST(caryear AS INT) >= CAST(" + minYear + " AS INT);"
    makeString = "SELECT * FROM vehicles WHERE make LIKE '%" + make + "%';"
    if(minYear != "" and maxYear == ""):
        cur.execute(minyearString)
    if(minYear == "" and maxYear != ""):
        cur.execute(maxyearString) 
    if(minYear != "" and maxYear != ""):
        cur.execute(minmaxString)    
    if(make != ""):
        cur.execute(makeString)
    tableVals = cur.fetchall()
    return tableVals;

#Filters
def getMakes()
    cur.execute("SELECT DISTINCT make FROM vehicles")
    tableVals = cur.fetchall()
    return tableVals;

#commit table changes

def addOffer(name = "", email = "", number = "", zipcode = "", offer = "", vin = ""):
    cur.execute("INSERT INTO offers (name, number, email, offer, zipcode, vin) VALUES (%s,%s,%s,%s,%s,%s)", (name, number, email, offer, zipcode, vin))
    conn.commit()



fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/getFilteredVehicles/")
async def read_item(minYear: str = "", maxYear: str = "", make: str = ""):
    return getFIlteredVehicles(minYear, maxYear, make)

@app.get("/getVehcileVin/")
async def read_item(vin: str = ""):
    return getAllVehicleWithVIN(vin)

@app.get("/getAllVehicles/")
async def read_item2():
    return getAllVehicles()

@app.get("/insertOffer/")
async def read_item(name: str = "", email: str = "", number: str = "", zipcode: str = "", offer: str = "", vin: str = ""):
    return addOffer(name, email, number, zipcode, offer, vin)

@app.get("/getMakes/")
async def read_item():
    return getMakes()
