"""
IIS API v 0.0.1
@Author: Gabriel Guillen
Details
There is an API (http://api.open-notify.org/) that provides information on the International Space Station. Documentation is provided via the website, along with sample request/response.

Task
    Implement a Python script that will accept the following command line arguments, along with any required information, and print the expected results

loc
    print the current location of the ISS
    Example: “The ISS current location at {time} is {LAT, LONG}”
    common usage: python ISS.py --loc
pass
    print the passing details of the ISS for a given location
    Example: “The ISS will be overhead {LAT, LONG} at {time} for {duration}”
    common usage: python ISS.py --pass  -long 40.71  -lat -74
    common usage: python ISS.py --pass  -long 40.71  -lat -74 -alt 100 -n 1

people
    for each craft print the details of those people that are currently in space
    common usage: python ISS.py --people

"""

import requests
import json
from datetime import datetime

class ISS:
    """
    Class that shows information about the ISS
    """
    def requester(url:str ,params:dict =None):
        """
        Function that returns the JSON dictionary
        Parameters:
        url: URL of the webAPI
        params: Dictionary of parameters (optional)
        """
        #Requesting of the information
        req = requests.get(url,params)

        #Checking that the request was successful
        if req.status_code == 200:
            return req.json()
        else:
            print("Something is wrong")
            exit(-1)

    def loc():
        """
        Print the current location of the ISS
        - No parameters needed -
        """
        #Making the Request and obtaining the JSON dictionary
        data = ISS.requester('http://api.open-notify.org/iss-now.json')

        #Showing the result
        print(f"The ISS current location at {datetime.fromtimestamp(data['timestamp'])} is {data['iss_position']['longitude'],data['iss_position']['latitude']}")

    def pass_(lat:float,long:float,alt=None,n=None):
        """
        Print the passing details of the ISS for a given location

        Mandatory Parameters:
            lat: Latitude
            long: Longitude

        Optional Parameters:
            alt: Altitude (by default = 100)
            n: Number of passes (by default = 5)
        """

        #Creating the dictionary of mandatory parameters
        parameters = {
        "lat": lat,
        "lon": long,
        }

        #adding the alt parameter if available
        if(alt):
            parameters['alt'] =alt

        #adding the n parameter if available
        if(n):
            parameters['n'] =n

        #Making the Request and obtaining the JSON dictionary
        data = ISS.requester("http://api.open-notify.org/iss-pass.json", params=parameters)

        # Data that I requested.
        # Note, I am using this values and not the parameters since the API can round or
        # alter the results. So I am showing the values that the API is actually using.
        request = data['request']

        #Printing te Requested info
        print(f"The following {request['passes']} passes ")
        print(f"In ({request['latitude']},{request['longitude']}) at altitude {request['altitude']} will be:")

        #Printing the response
        for d in data['response']:
            print(f"\tStarting at {datetime.fromtimestamp(d['risetime'])}, for {d['duration']} seconds")


    def people():
        """
        For each craft, this function prints the
        details of those people that are currently in space

        - No parameters needed -

        """
        #Making the Request and obtaining the JSON dictionary
        data = ISS.requester('http://api.open-notify.org/astros.json')['people']

        # Loading of the data
        # Note: This part was not necessary, it was done just to
        # show the people in space by craft.
        # Perhaps this is not the more efficient way to do it,
        # but there is a lack of documentation about if the API
        # is actually showing the results by craft or in a random order
        # This method guarantees the right behaviour of the function in any case.

        bycraft={}
        for d in data:
            if d['craft'] in bycraft.keys():
                bycraft[d['craft']].append(d['name'])
            else:
                bycraft[d['craft']] = [d['name']]

        #Printing of the data
        for craft,people in bycraft.items():
            print(f"Crew of the craft {craft}")
            for p in people:
                print("\t*",p)

#The following part should be in a cli interface, however in order to maintain it simple enough, I keep it here.
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--loc", help="Print the current location of the ISS",action="store_true")
parser.add_argument("--people", help="Print for each craft, the name those people that are currently in space",action="store_true")
parser.add_argument("--pass", help="Print the passing details of the ISS for a given location",action="store_true",dest='pass_')

parser.add_argument("-long",help="Longitude")
parser.add_argument("-lat", help="Latitude")

parser.add_argument("-alt", type=float, help="Altitude")
parser.add_argument("-n", type=float, help="Number of passes")

args = parser.parse_args()
if args.loc:
    ISS.loc()

if args.people:
    ISS.people()

if args.pass_:
    ISS.pass_(args.long,args.lat,args.alt,args.n)


