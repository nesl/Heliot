
# ip of the airsim machine need to be fixed to send sceanrio
from utils.dataflow import *
scenario = 0
result = dataflow.sendData(id='air_sim_scenario',data=scenario)
print(result)
