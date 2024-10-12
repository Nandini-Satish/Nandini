from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection string
MONGO_DETAILS = (
    "mongodb+srv://Nandini_1:RDPsXmSCQwDmkXDi@cluster0.rcmql.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Initialize MongoDB client and database
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client["fastapi_assignment"]

# Access collections within the database
items_collection = db.get_collection("items")
clock_in_records_collection = db.get_collection("clock_in_records")
