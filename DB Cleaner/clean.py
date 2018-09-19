import pandas as panda
import numpy as np
import datetime


#####FUNCTIONS###########################################################################################
#Function for converting the date into a readable format.
def convert_to_date (date_cur_format):
    date_as_string = str(date_cur_format)
    year = date_as_string[0:4]
    month = date_as_string[4:6]
    day = date_as_string[6:8]
    return str( day + "/" + month + "/" + year)

# Places all phone numbers in the format ###-###-#####
def phone_format (phone_number):
        rmv_space = phone_number.replace(' ', '')
        rmv_dash = rmv_space.replace('-','')
        phone_consistancy = rmv_dash[0:3] + "-" + rmv_dash[3:6] + "-" + rmv_dash[6:]
        return phone_consistancy
# Fix the store names for consistancy
def update_store_name (store_name):
    store_string = str(store_name)
    rpl_store_string = store_string.replace('_store','_Store')
    return rpl_store_string

def update_car_seats (int):
    seats = float(int)
    if seats < 3:
        seats = 4
    return seats

# removes the prefix ffrom the phone number and cleans up some inconsistantcy 
def convert_to_number (phone_cur_format):
    string_number = str(phone_cur_format)
    if string_number == 'null':
        return 'null'
    else:
        if(string_number.find('1 (11) ', 0, 8)) == 0:
            actual_number = (string_number).lstrip('1 (11) ')
            phone_return = phone_format(actual_number)
            return phone_return
        else:
            phone_return2 = phone_format(string_number)
            return phone_return2

# Function for removing special characters
def rmv_spc_char (data_input):
    invalid_characters = ['!','@','#','$','%','^','&','*',',',' ',]
    string_input = str(data_input)
    for characters in invalid_characters:
        data_output = string_input.replace(characters,'')

#########################################################################################################

# Open the unclean central.csv file to be cleaned
cdata = panda.read_csv('DB_Central.csv')

# Open the unclean Store.csv file to be cleaned
sdata = panda.read_csv('DB_Store.csv')

# Set any blanks or NAN's to null
cdata = cdata.replace(np.nan, 'null', regex=True)
sdata = sdata.replace(np.nan, 'null', regex=True)
cdata = cdata.replace('', 'null', regex=True)
sdata = sdata.replace('', 'null', regex=True)
cdata = cdata.replace('  ', '', regex=True)
sdata = sdata.replace('  ', '', regex=True)

# Rename name incorrectly spelt headers and rename some for consitancy
cdata.rename(columns={'Order_CreateDate': 'Order_Create_Date',
                    'Order_PickupDate': 'Order_Pickup_Date',
                    'Order_PickupStore': 'Order_Pickup_Store',
                    'Order_ReturnDate': 'Order_Return_Date',
                    'Order_ReturnStore': 'Order_Return_Store',
                    'Customer_Addresss': 'Customer_Address',
                    'Customer_Brithday': 'Customer_Birthday'
                    }, inplace=True)

# Get store data from store database and scrub
stores = sdata[['Store_ID', 'Store_Name', 'Store_Address', 'Store_Phone',
	           'Store_City', 'Store_State_Name']]

#Clean all the Customer_Phone data remove (*) -- Marco Coded this line, confimed working
cdata['Customer_Phone'] = cdata['Customer_Phone'].str.slice(0,-1)

# Date data clean/rearrange -- Marco asissted with coding
datenames = ['Order_Create_Date', 'Order_Pickup_Date', 'Order_Return_Date' ]
for datename in datenames:
    cdata[datename] = cdata[datename].apply(convert_to_date)

# remove any phone number pre fixes - Marco Assisted with the coding   

phonenames = ['Pickup_Store_Phone','Return_Store_Phone','Customer_Phone']
for phonename in phonenames:
    cdata[phonename] = cdata[phonename].apply(convert_to_number)
    
sdata['Store_Phone'] = sdata['Store_Phone'].apply(convert_to_number)

# Fixing Store names
storenames = ['Pickup_Store_Name', 'Return_Store_Name']
for storename in storenames:
    cdata[storename] = cdata[storename].apply(update_store_name)
sdata['Store_Name'] = sdata['Store_Name'].apply(update_store_name)

# clean the customer addresses
cdata['Customer_Address'] = cdata['Customer_Address'].apply(rmv_spc_char)

# find null and remove null data
order_data = ['Pickup_Store_Name']

car_data = ['Car_MakeName']
for orders in order_data:
    data_A=cdata.index[cdata['Pickup_Store_Name'] == 'null'].tolist()
    data_B=cdata.index[cdata['Car_MakeName'] == 'null'].tolist()
    data_C=cdata.index[cdata['Return_Store_Name'] =='null'].tolist()
    data=data_A+data_B+data_C
    cdata=cdata.drop(cdata.index[data])

# Remove 0's from car seating
cdata['Car_SeatingCapacity'] = cdata['Car_SeatingCapacity'].apply(update_car_seats)

# Create the clean csv file to be put into the database
cdata.to_csv('Clean_DB_Central.csv', index=False)
stores.to_csv('Clean_DB_Store.csv', index=False)
