
# ip of the airsim machine need to be fixed to send sceanrio
from utils.dataflow import *
import sys

scenario = 1


if __name__ == "__main__":
    if len(sys.argv)==2:
        scenario=int(sys.argv[1])
    result = dataflow.sendData(id='air_sim_scenario',data=scenario)
    print(result)
