from collections import defaultdict, namedtuple
import json
import logging
import sys
import timeit


import requests 
from bs4 import BeautifulSoup

logging.basicConfig(filename="data_extract.log", level=logging.INFO, 
    format="%(asctime)s:%(levelname)s:%(message)s")

BASE_URL = "https://adelaidemetro.com.au"

Stop = namedtuple("Stop", "code, name, address, stop_url")

def get_timetable_paths(base_url, transport_mean = "buses"):
    time_tables_url = f"{base_url}/timetables/{transport_mean}"
    r = requests.get(time_tables_url)
    bus_stop_soup = BeautifulSoup(r.text, 'html.parser')
    route_tabs = bus_stop_soup.find("ul", {"id": "route-tabs"})
    time_tables_paths = list()
    for item in route_tabs.find_all('li'):
        for link in item.find_all("a"):
            time_tables_paths.append(link.get('href'))
    return time_tables_paths

def get_route_paths(base_url, time_tables_paths):
    routes = list()

    for t in time_tables_paths:
        tab_url = f"{base_url}{t}"
        r = requests.get(tab_url)
        tab_n = t.split("/")[-1]
        
        page_routes_soup = BeautifulSoup(r.text, 'html.parser')

        routes_links = page_routes_soup.find("div", {"id": "related-routes"})

        for item in routes_links.find_all('a'):
            try:
                routes.append(item.get("href"))
            except Exception as e:
                print(e)
        
        logging.info(f"fetched data for tab: {tab_n}")

    return routes

def build_routes_object(base_url, routes):
    routes_db = list()

    routes_to_process = len(routes)
    routes_processed = 0
        
    for rt in routes:
        
        route_object = defaultdict(list)
        route_url = f"{base_url}{rt}"      
        r = requests.get(route_url)
        route_n = rt.split("/")[-1]
        
        route_object["code"] = route_n

        route_soup = BeautifulSoup(r.text, 'html.parser')

        search_tabs = ["tab-content-1","tab-content-2"]
        routes_processed += 1
        print(f"{routes_processed}/{routes_to_process}")
        for st in search_tabs:
            stops = route_soup.find("div", {"id": st})

            if stops:

                direction = stops.find_all("h2")[0].text
                                
                
                for stop in stops.find_all('p'):
                    try:
                        stop_code = stop.a.get("href").split("/")[-1]
                        stop_name = stop.a.text
                        address = stop.contents[-1].strip("\n").strip("\t")
                        stop_url = stop.a.get("href")
                
                        route_object[direction].append(Stop(stop_code, stop_name, address, stop_url))
                    except Exception as e:
                        logging.info(f"there was an error{e} while fetching: {route_n}")
                                        
                logging.info(f"fetched data for {route_n} on direction {direction}")
            else:
                logging.info(f"no stops for route: {route_n}")
                                 
        routes_db.append(route_object)
    
    return routes_db

# Job starts running here

start = timeit.default_timer()

ttp = get_timetable_paths(BASE_URL)

rp = get_route_paths(BASE_URL, ttp)

db = build_routes_object(BASE_URL, rp)

with open("routes_db.json", "w+") as fp:
    json.dump(db, fp)

stop = timeit.default_timer()
total_time = stop - start

mins, secs = divmod(total_time, 60)
hours, mins = divmod(mins, 60)

logging.info(f"Total running time: {hours}:{mins}:{secs}.")

sys.stdout.write("Total running time: %d:%d:%d.\n" % (hours, mins, secs))