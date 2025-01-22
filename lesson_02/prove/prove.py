"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: Enoch Olayemi
Justification: I met all requirements for the project - 4
Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py" and leave it running.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}

Outline of API calls to server

1) Use TOP_API_URL to get the dictionary above
2) Add "6" to the end of the films endpoint to get film 6 details
3) Use as many threads possible to get the names of film 6 data (people, starships, ...)

"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/

    def __init__(self, url):
        # Call the Thread class's init function
        # threading.Thread.__init__(self)
        super().__init__()
        self.url = url
        self.response = {}
        self.status_code = 0

    def run(self):
        global call_count
        response = requests.get(self.url)
        call_count += 1
        # Check the status code to see if the request succeeded.
        self.status_code = response.status_code
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)


# TODO Add any functions you need here
def request_and_sort(items):
    request_threads = []
    result_list = []

    for item in items:
        thread = Request_thread(rf"{item}")
        request_threads.append(thread)

    for thread in request_threads:
        thread.start()

    for thread in request_threads:
        thread.join()
        result_list.append(thread.response["name"])

    result_list.sort()

    return result_list

def characterRequest(characters):
    return request_and_sort(characters)

def planetRequest(planets):
    return request_and_sort(planets)

def starshipRequest(starships):
    return request_and_sort(starships)

def vehicleRequest(vehicles):
    return request_and_sort(vehicles)

def specieRequest(species):
    return request_and_sort(species)


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')
    log.write("-----------------------------------------")
    

    # TODO Retrieve Top API 
    topAPI = Request_thread(rf"{TOP_API_URL}")
    topAPI.start()
    topAPI.join()
    # print(topAPI.response) # Requests a dictionary of api-links which include the films api that we need.

    # TODO Retrieve Details on film 6
    films = topAPI.response["films"] # Since its a dictionary, we use the key to get the api-link for films
    filmAPI = Request_thread(rf"{films}6") # request the film 6 api specifically.
    filmAPI.start()
    filmAPI.join()
    # print(filmAPI.response)

    # Use the key from the film api to get its datails.
    title = filmAPI.response["title"]
    director = filmAPI.response["director"]
    producer = filmAPI.response["producer"]
    released = filmAPI.response["release_date"]
    characters =  filmAPI.response["characters"]
    planets = filmAPI.response["planets"]
    starships = filmAPI.response["starships"]
    vehicles = filmAPI.response["vehicles"]
    species =  filmAPI.response["species"]


    # TODO Display results
    log.write(f"Title   : {title}")
    log.write(f"Director: {director}")
    log.write(f"Producer: {producer}")
    log.write(f"Released: {released}")
    log.write("")
    log.write(f"Characters: {len(characters)}")
    log.write(f"{', '.join(characterRequest(characters))}")
    log.write("")
    log.write(f"Planets: {len(planets)}")
    log.write(f"{', '.join(planetRequest(planets))}")
    log.write("")
    log.write(f"Starships: {len(starships)}")
    log.write(f"{', '.join(starshipRequest(starships))}")
    log.write("")
    log.write(f"Vehicles: {len(vehicles)}")
    log.write(f"{', '.join(vehicleRequest(vehicles))}")
    log.write("")
    log.write(f"Species: {len(species)}")
    log.write(f"{', '.join(specieRequest(species))}")
    log.write("")
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()