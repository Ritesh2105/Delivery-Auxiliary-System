import urllib.request
import json

endpoint = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
api_key = ''  # put your api key here
inputLocation = input('Where are you?: ').replace(' ', '+')
inputType = 'textquery'
fields = 'photos,formatted_address,name,geometry'

loc_request = 'input={}&inputtype={}&fields={}&key={}'.format(inputLocation, inputType, fields, api_key)

request = endpoint + loc_request
response = urllib.request.urlopen(request).read()
details = json.loads(response)

print(request)


