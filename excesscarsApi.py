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
# conn = psycopg2.connect(connectionString)

# #initiaite Connection Object
# cur = conn.cursor()

#Get Code goes here
def getAllVehicles():
    conn = psycopg2.connect(connectionString)
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles;")
    tableVals = cur.fetchall()
    return tableVals;
def getAllFeaturedVehicles():
    conn = psycopg2.connect(connectionString)
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles WHERE CAST(price as INT) < 15000 AND CAST(mileage as INT) < 70000 AND CAST(caryear as INT) > 2018 ORDER BY RANDOM() LIMIT 8;")
    tableVals = cur.fetchall()
    return tableVals;
def getAllVehicleWithVIN(vin=""):
    conn = psycopg2.connect(connectionString)
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles WHERE vin = '" + str(vin) + "';")
    tableVals = cur.fetchall()
    return tableVals;
def getFIlteredVehicles(minYear = None, maxYear = None, make = None, model = None, minPrice = None, maxPrice = None, miles = None, body = None, location = None):
    conn = psycopg2.connect(connectionString)
    cur = conn.cursor()
    if(minYear == ""):
        minYear = None
    if(maxYear == ""):
        maxYear = None
    if(make == ""):
        make = None
    if(model == ""):
        model = None
    if(minPrice == ""):
        minPrice = None
    if(maxPrice == ""):
        maxPrice = None
    if(miles == ""):
        miles = None
    if(body == ""):
        body = None
    if(location == ""):
        location = None
    query="SELECT * FROM vehicles WHERE 1=1"
    params = []
    if make is not None:
        query+=" AND make = %s"
        params.append(make)
    if minYear is not None:
        query+=" AND CAST(caryear AS INT) >= %s"
        params.append(int(minYear))
    if maxYear is not None:
        query+=" AND CAST(caryear AS INT) <= %s"
        params.append(int(maxYear))
    if model is not None:
        query+=" AND model = %s"
        params.append(model)
    if minPrice is not None:
        query+=" AND CAST(price AS INT) >= %s"
        params.append(int(minPrice))
    if maxPrice is not None:
        query+=" AND CAST(price AS INT) <= %s"
        params.append(int(maxPrice))
    if miles is not None:
        query+=" AND CAST(mileage AS INT) <= %s"
        params.append(int(miles))
    if body is not None:
        query+=" AND bodytype = %s"
        params.append(body)
    if location is not None:
        query+=" AND location = %s"
        params.append(location)
    cur.execute(query, params)
    return cur.fetchall()
#Filters
def getMakes():
    conn = psycopg2.connect(connectionString)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT make FROM vehicles")
    tableVals = cur.fetchall()
    return tableVals;

def getBodys():
    conn = psycopg2.connect(connectionString)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT bodytype FROM vehicles")
    tableVals = cur.fetchall()
    return tableVals;

def getLocations():
    conn = psycopg2.connect(connectionString)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT location FROM vehicles")
    tableVals = cur.fetchall()
    return tableVals;

def getModels(make = ""):
    conn = psycopg2.connect(connectionString)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT model FROM vehicles WHERE make LIKE '%" + make + "%';")
    tableVals = cur.fetchall()
    return tableVals;
    
def getMinMaxYear():
    conn = psycopg2.connect(connectionString)
    cur = conn.cursor()
    cur.execute("SELECT Min(carYear), MAX(carYear) FROM vehicles")
    tableVals = cur.fetchall()
    return tableVals;
    
#commit table changes

def addOffer(name = "", email = "", number = "", zipcode = "", offer = "", vin = ""):
    conn = psycopg2.connect(connectionString)
    cur = conn.cursor()
    cur.execute("INSERT INTO offers (name, number, email, offer, zipcode, vin) VALUES (%s,%s,%s,%s,%s,%s)", (name, number, email, offer, zipcode, vin))
    conn.commit()
def contactMe(name = "", email = "", number = "", subject = "", message = ""):
    conn = psycopg2.connect(connectionString)
    cur = conn.cursor()
    cur.execute("INSERT INTO contactform (contactname, contactnumber, contactemail, contactsubject, contactmessage) VALUES (%s,%s,%s,%s,%s)", (name, number, email, subject, message))
    conn.commit()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/getFilteredVehicles/")
async def read_item(minYear: str = "", maxYear: str = "", make: str = "", model: str = "", minPrice: str = "", maxPrice: str = "", miles: str = "", body : str = "", location : str = ""):
    return getFIlteredVehicles(minYear, maxYear, make, model, minPrice, maxPrice, miles, body, location)

@app.get("/getVehcileVin/")
async def read_item(vin: str = ""):
    return getAllVehicleWithVIN(vin)

@app.get("/getAllVehicles/")
async def read_item2():
    return getAllVehicles()

@app.get("/getFeaturedVehicles/")
async def read_item2():
    return getAllFeaturedVehicles()

@app.get("/insertOffer/")
async def read_item(name: str = "", email: str = "", number: str = "", zipcode: str = "", offer: str = "", vin: str = ""):
    return addOffer(name, email, number, zipcode, offer, vin)

@app.get("/insertContact/")
async def read_item(name: str = "", email: str = "", number: str = "", subject: str = "", message: str = ""):
    return contactMe(name, email, number, subject, message)

@app.get("/getMakes/")
async def read_item():
    return getMakes()

@app.get("/getBodys/")
async def read_item():
    return getBodys()

@app.get("/getLocations/")
async def read_item():
    return getLocations()
    
@app.get("/getMinMaxYear/")
async def read_item():
    return getMinMaxYear()

@app.get("/getModels/")
async def read_item(make: str = ""):
    return getModels(make)
