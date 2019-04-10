import requests
import json
import serial
ser = serial.Serial('/dev/ttyACM0',9600)
read_serial=ser.readline()

#Specify here the shelf number of the RFID READER
shelf_number = 3

def loadData():
    url = "https://fv3md359db.execute-api.ap-south-1.amazonaws.com/final/readrecords"
    r = requests.get(url)
    data=json.loads(r.text)
    return data


def findNameFromTag(tag):
    for i in range(0, No_Of_Books):
        if tag in booksData[i]["Tags"]:
            global index
            index = i
            return booksData[i]["Name"]

def removeBook(name,tag):
        url = "https://fv3md359db.execute-api.ap-south-1.amazonaws.com/final/readlocation?find=" + name
        r = requests.get(url)
        data=json.loads(r.text)
        print(name)
        print(data)
        arr = data[0]["Location"]["Shelf " + str(shelf_number)]
        arr.remove(tag)
        data[0]["Location"]["Shelf " + str(shelf_number)] = arr
        updateurl = "https://fv3md359db.execute-api.ap-south-1.amazonaws.com/final/updatebook"
            newData = {
                "bookname" : name,
                    "book" : data[0]["Location"]
                        }
                            print(newData)
                            r = requests.post(updateurl, json=newData)
                            print(r)

def updateData(tag,regno):
    if "Issued" not in  booksData[index]:
        booksData[index]['Issued'] = {}
            old_json = booksData[index]['Issued']
            old_json[tag] = regno
            data={
                "bookname" : book_to_remove,
                    "updated" : old_json
                        }
                            print(data)
                            url = "https://fv3md359db.execute-api.ap-south-1.amazonaws.com/final/updatebookinrecord"
                                r = requests.post(url, json=data)
                                print(r)


while True:
    booksData = loadData()
    No_Of_Books = len(booksData)
    print ("Keep the book on scanner")
    tag_from_rfid=ser.readline().decode('utf-8').strip()
    book_to_remove = findNameFromTag(tag_from_rfid)
    removeBook(book_to_remove,tag_from_rfid)
    print ("Put your id card")
    regno=ser.readline().decode('utf-8').strip()
    updateData(tag_from_rfid, regno)
    choice = input("Add another book? Y/N")
    if choice=="Y":
        continue
    else:
        print("Thank you for adding the book")
        break

