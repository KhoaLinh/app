from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# Create a new client and connect to the server
uri = "mongodb+srv://nguyenlinhanhkhoa3:zTT1NGJzkyoL5VGH@cluster0.to3lvrc.mongodb.net/"
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to the database
mydb = client["CE412"]
mycol1 = mydb["IOT"]

# Update checkin time
def update_nhietdo():
    gio_vao = datetime.now().isoformat()
    mycol1.update_one({'id_Nhanvien': employee_id}, {'$set': {'timestamp': gio_vao}})
    print('Time checkin updated successfully.')
