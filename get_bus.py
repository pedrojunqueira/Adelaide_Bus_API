
import requests

# 281 12505 stop Wilpena 15A south east side - to city

stop_id = 12505

# url = "http://realtime.adelaidemetro.com.au/sirism/SiriStopMonitoring.svc/json/SM?MonitoringRef=16281"
url = f"http://realtime.adelaidemetro.com.au/sirism/SiriStopMonitoring.svc/json/SM?MonitoringRef={stop_id}"

# r = requests.get(url)

# data = r.json()

# # print(data)

import json


# with open(f'{stop_id}_sample.json', 'w') as fp:
#     json.dump(data, fp)


with open(f'{stop_id}_sample.json', 'r') as fp:
    data = json.load(fp)

stamp = int(data["StopMonitoringDelivery"][0]["ResponseTimestamp"].strip("/")[5:15])


from datetime import datetime

# "/Date(1612350540000+1030)/",

d = datetime.fromtimestamp(stamp)

s = "/Date(1612350486000+1030)/",

# print(f"{d.year}-{d.month}-{d.day} {d.hour}:{d.minute} ")

#print(data["StopMonitoringDelivery"][0])

# for key in data["StopMonitoringDelivery"][0].keys():
#     print(key)

# Keys for each StopMonitoringDelivery

# ResponseTimestamp
# Status
# ValidUntil
# MonitoredStopVisit # Details about the incoming bus 
# MonitoringRef # Bus Stop ID
# version

# explore MonitoredStopVisit Data

# print(type(data["StopMonitoringDelivery"][0]["MonitoredStopVisit"])) # list

# print(len(data["StopMonitoringDelivery"][0]["MonitoredStopVisit"])) # 1 Iten

MonitoredStopVisit = data["StopMonitoringDelivery"][0]["MonitoredStopVisit"][0] # dict

for key, value in MonitoredStopVisit.items():
    print(f"{key}: {value} ")

# stop_visit Keys

# RecordedAtTime: Date Recorded 
# ItemIdentifier: Identifier
# MonitoredVehicleJourney: Detail About Vehicle
# MonitoringRef: Bus Stop ID
# StopVisitNote: Stop Type... BS (Bus Stop)
# ValidUntilTime: Null

# Explore MonitoredVehicleJourney

# print(type(stop_visit["MonitoredVehicleJourney"])) # dict

MonitoredVehicleJourney = MonitoredStopVisit["MonitoredVehicleJourney"]

for key, value in MonitoredVehicleJourney.items():
    print(f"{key}: {value}")


# BlockRef: {'Value': '391'}
# ConfidenceLevel: 1
# DestinationAimedArrivalTime: /Date(1612428120000+1030)/
# DestinationAimedArrivalTimeSpecified: True
# DestinationName: [{'Value': 'Marion'}]
# DirectionRef: {'Value': 'O'}
# DriverName: Confidential
# DriverRef: 00000
# FramedVehicleJourneyRef: {'DataFrameRef': {'Value': '2021-02-04'}, 'DatedVehicleJourneyRef': '652981'}
# JourneyPatternRef: {'Value': '29'}
# LineRef: {'Value': 'W90'}
# Monitored: True
# MonitoredCall: {'StopPointName': [{'Value': '15A Wilpena Ave'}], 'StopPointRef': {'Value': '12505'}, 'AimedArrivalTime': '/Date(1612424150000+1030)/', 'AimedArrivalTimeSpecified': True, 'AimedDepartureTime': '/Date(0)/', 'AimedLatestPassengerAccessTime': '/Date(0)/', 'DestinationDisplay': {'Value': 'Marion'}, 'EarliestExpectedDepartureTime': '/Date(0)/', 'ExpectedLatestPassengerAccessTime': '/Date(0)/', 'Item': '/Date(0)/', 'Item1': '/Date(0)/', 'LatestExpectedArrivalTime': '/Date(1612424155000+1030)/', 'LatestExpectedArrivalTimeSpecified': True, 'ProvisionalExpectedDepartureTime': '/Date(0)/', 'VehicleLocationAtStop': {'Items': ['-34.88317674', '138.63373344']}}
# MonitoredSpecified: True
# OperatorRef: {'Value': '5 - Adelaide Metro (Torrens Transit)'}
# OriginAimedDepartureTime: /Date(0)/
# VehicleLocation: {'Items': ['-34.8677', '138.6620']}
# VehicleRef: {'Value': '1057'}

# Data to extract for each request in a tabular format


