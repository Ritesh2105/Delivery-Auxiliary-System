import urllib.request
import json
import pymongo
import os
from pymongo import MongoClient
import requests


###initialize mongodb
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.GoogleMaps
collection = db.Directions
### introduce endpoints in
dirEndpoint = 'https://maps.googleapis.com/maps/api/directions/json?'

# Augmenify Apikey
api_key = '' #put your api here

origin = input('Where are you?: ').replace(' ', '+')
destination = input('Where do you want to go?').replace(' ', '+')
print('travel modes are as below:')
travelModeList = ["driving", "bicycling", "walking", "transit"]
for i in range(len(travelModeList)):
    print(travelModeList[i])
travelMode = input('what tansportation are you taking?')

WayPoints=None
Choice=None
def getWaypoints():
    global WayPoints
    global Choice
    WayPoints=''
    while True:
        Choice=input("do you need to add way points?(Y/N)") 
        j=0
           
        if (Choice=="N" or Choice=="n"):        
            return 

        if (Choice=="Y" or Choice=="y"):     
              
            WayPoint=input("Please enter your "+ str(j+1)+ " way point: ") 
            WayPoints+=WayPoint+'|' 
            j+=1
            while True:     
                YN=input("the added point is: "+WayPoint+", do you want to add more?(Y/N)") 
                if (YN=="Y" or YN=="y"):               
                    WayPoint=input("Please enter your "+ str(j+1)+ " way point: ") 
                    WayPoints+=WayPoint+'|' 
                    j+=1             

                if (YN=="N" or YN=="n"): 
                    WayPoints=WayPoints[:-1]               
                    return                       
                else:
                    continue
        else:            
            continue       
               
getWaypoints()  
aWayPoints= WayPoints.split("|") ##aWayPoints is a list
WayPoints=WayPoints.replace(' ', '+')
print(WayPoints)
print(aWayPoints)

    
nav_request = 'origin={}&destination={}&mode={}&waypoints={}&key={}'.format(origin, destination, travelMode,WayPoints, api_key)
dirRequest = dirEndpoint + nav_request

dirResponse = urllib.request.urlopen(dirRequest).read() ## dirRespnse is a JSON object

directions = json.loads(dirResponse) ## directions is dict
## json.dump and json.load are both methods to deal with JSON ENCODED FORMAT files(looks like json)
json_str = json.dumps(directions, indent=4)
with open('originnal_data.json', 'w') as json_file:
    json_file.write(json_str)



travelData=[]
def getDuration():
    routeAccess=directions['routes']
    for routeData in routeAccess:
        legAccess=routeData['legs']
        for legData in legAccess:   #each legData is a dict
                        
            del legData["steps"]
            del legData["traffic_speed_entry"]
            del legData['via_waypoint']
            travelData.append(legData) 
getDuration()
print(travelData)

if (Choice=="N" or Choice=="n"):    
    travelDataDict={
        'origin':travelData[0]["start_address"],
        'destination':travelData[-1]["end_address"],        
        'each segment info':travelData
    }

if (Choice=="Y" or Choice=="y"):    
    travelDataDict={
        'origin':travelData[0]["start_address"],
        'destination':travelData[-1]["end_address"],
        'waypoints':aWayPoints,
        'each segment info':travelData
    }

with open('travelData.json','w') as file:
    json.dump(travelDataDict,file,indent=4)

### save result into mongodb

result = collection.insert_one(travelDataDict)

if result.acknowledged:
    print('search is saved in databse ' + str(result.inserted_id))


