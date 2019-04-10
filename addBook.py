import requests
import serial

ser = serial.Serial('/dev/ttyACM0',9600)
read_serial=ser.readline()

#Assume this pi is considered as Shelf 1
def createRecord(name,tags):
    url = "https://fv3md359db.execute-api.ap-south-1.amazonaws.com/final/createrecords"
    data = {
        "name" : name ,
        "book" : tags
    }
    print(data)
    r = requests.post(url, json=data)
    print(tag + " Added Successfully")
def updateAWS(name,floor,shelf):
    url = "https://fv3md359db.execute-api.ap-south-1.amazonaws.com/final/addbooks"
    data = {
    "name"  :name,
    "floor" : floor,
    "shelf" : shelf
    }
    print(data)
    r = requests.post(url, json=data)
    print(tag + " Added Successfully")

while True:
    print ("Welcome to SMART LIBRARY\nHERE YOU CAN ADD A NEW BOOK INTO THE LIBRARY")
    name =  input("Enter the name of book to be kept on that shelf : ")
    quantity = input("Enter the number of shelves on which the books are kept : ")
    data = {}
    tag_array=[]
    for x in range(0,int(quantity)):
        snum = input("Enter the shelf Number: ")
        bnum = input("Enter the number of book on shelf " + snum + ": ")
        arr = []
        for y in range(0,int(bnum)):
           print ("Keep the book on scanner")
           tag=ser.readline().decode('utf-8').strip()
           arr.append(tag)
           tag_array.append(tag)
           print("Book Recorded")
        
        data["Shelf " + snum] = arr


    floor = input("Enter the floor of the location (1-3) : ")
    createRecord(name,tag_array)
    updateAWS(name,floor,data)
    choice = input("Add another book? Y/N")
    if choice=="Y":
        continue
    else:
        print("Thank you for adding the book")
        break




