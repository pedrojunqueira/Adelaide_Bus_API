import json
from datetime import datetime
from collections import defaultdict
import time


import requests
import pandas as pd

def str_to_date(string:str ):
    stamp = int(string.strip("/")[5:15])
    return datetime.fromtimestamp(stamp)

# 281 12505 stop Wilpena 15A south east side - to city

stop_id = 12505

# url = "http://realtime.adelaidemetro.com.au/sirism/SiriStopMonitoring.svc/json/SM?MonitoringRef=16281"
url = f"http://realtime.adelaidemetro.com.au/sirism/SiriStopMonitoring.svc/json/SM?MonitoringRef={stop_id}"


def validate_data(data):
    return data if not None else 0

def extract_data(data):

    if not data["StopMonitoringDelivery"][0].get("MonitoredStopVisit"):
        return None

    extracted_data = defaultdict(list)

    for StopMonitoringDelivery  in data["StopMonitoringDelivery"]:
        for MonitoredStopVisit in StopMonitoringDelivery["MonitoredStopVisit"]:
            extracted_data["RecordedAtTime"].append(str_to_date(MonitoredStopVisit["RecordedAtTime"]))
            extracted_data["ItemIdentifier"].append(MonitoredStopVisit["ItemIdentifier"])
            extracted_data["BlockRef"].append(MonitoredStopVisit["MonitoredVehicleJourney"]["BlockRef"]["Value"])
            extracted_data["ConfidenceLevel"].append(MonitoredStopVisit["MonitoredVehicleJourney"]["ConfidenceLevel"])
            extracted_data["DestinationAimedArrivalTime"].append(str_to_date(MonitoredStopVisit["MonitoredVehicleJourney"]["DestinationAimedArrivalTime"]))
            extracted_data["DestinationName"].append(MonitoredStopVisit["MonitoredVehicleJourney"]["DestinationName"][0]['Value'])
            extracted_data["DatedVehicleJourneyRef"].append(MonitoredStopVisit["MonitoredVehicleJourney"]["FramedVehicleJourneyRef"]['DatedVehicleJourneyRef'])
            extracted_data["LineRef"].append(MonitoredStopVisit["MonitoredVehicleJourney"]["LineRef"]['Value'])
            extracted_data["StopPointName"].append(MonitoredStopVisit["MonitoredVehicleJourney"]["MonitoredCall"]["StopPointName"][0]["Value"])
            extracted_data["AimedArrivalTime"].append(str_to_date(MonitoredStopVisit["MonitoredVehicleJourney"]["MonitoredCall"]["AimedArrivalTime"]))
            extracted_data["LatestExpectedArrivalTime"].append(str_to_date(MonitoredStopVisit["MonitoredVehicleJourney"]["MonitoredCall"]["LatestExpectedArrivalTime"]))
            extracted_data["At_stop_Lat"].append(float(MonitoredStopVisit["MonitoredVehicleJourney"]["MonitoredCall"]["VehicleLocationAtStop"]['Items'][0]))
            extracted_data["At_stop_Lon"].append(float(MonitoredStopVisit["MonitoredVehicleJourney"]["MonitoredCall"]["VehicleLocationAtStop"]['Items'][1]))
            extracted_data["OperatorRef"].append(MonitoredStopVisit["MonitoredVehicleJourney"]["OperatorRef"]["Value"])
            extracted_data["VehicleLocation_Lat"].append(float(MonitoredStopVisit["MonitoredVehicleJourney"]["VehicleLocation"]['Items'][0]))
            extracted_data["VehicleLocation_Lon"].append(float(MonitoredStopVisit["MonitoredVehicleJourney"]["VehicleLocation"]['Items'][1]))
            
    return  extracted_data


frame = pd.DataFrame()

for i in range(3):
    print(f"extracting data: {datetime.now().strftime('%Y-%m-%d %X')}")
    r = requests.get(url)
    data = r.json()
    time.sleep(3)
    # with open(f'{stop_id}_sample.json', 'r') as fp:
    #     data = json.load(fp)
    try:        
        df_data = extract_data(data)
        if  df_data:
            df = pd.DataFrame(df_data)
            frame = frame.append(df)
        else:
            print(f"No streaming data for {datetime.now().strftime('%Y-%m-%d %X')}")
            continue
    except Exception as err:
        print(f"{type(err)}: {err}")
    
    


frame.to_csv("bus_data.csv", index=False)

        
            

