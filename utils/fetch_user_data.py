from pymongo.mongo_client import MongoClient
import pandas as pd


class FetchUserData:
  def __init__(self) :
    self.uri = ""
      
  def fetch_user_data(self,file_path):

    df = pd.read_csv(file_path)
    nbr_list = df.iloc[df.groupby("car_id")["license_number_score"].idxmax()]['license_number'].tolist()
    nbr_list = list(set(nbr_list))


    # Create a new client and connect to the server
    myclient = MongoClient(self.uri)

    # Send a ping to confirm a successful connection
    try:
        myclient.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


    mydb = myclient["mydatabase"]
    mycol = mydb["LicenseDetails"]

    fetched_data = []
    license_plate_number = []
    name_of_owner = []
    home_address = []
    contact_number = []
    type_of_vehicle = []



    for license_nbr in nbr_list:
      query = {}
      query["license plate number"]  = license_nbr
      fetched_data.append(list(mycol.find(query)))

    for x in fetched_data:
      if len(x)>0:

        license_plate_number.append(x[0]['license plate number'])
        name_of_owner.append(x[0]['name of owner'])
        home_address.append(x[0]['home address'])
        contact_number.append(x[0]['contact number'])
        type_of_vehicle.append(x[0]['type of vehicle'])


    df = pd.DataFrame(list(zip(license_plate_number, name_of_owner, home_address, contact_number, type_of_vehicle)),
                      columns =  ["License plate number", "Name of owner", "Home address", "Contact number", "Type of vehicle"])
    


    return df