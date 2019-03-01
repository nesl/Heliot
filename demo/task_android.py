from utils.dataflow import *

from flask import Flask


app = Flask(__name__)

DISPLAY_IP = None
DISPLAY_PORT = None

@app.route("/")
def hello():
    labels = dataflow.getData(inport=20003) #get the labels
    print('lables are:',labels)
    result = None
    if labels!=None:
        if len(labels)>0:
            result = labels[0]
            if result !='car' or result !='person':
                result =None
    return '{}'.format(result)


if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print(
    #         'usage: python {0} WEB_IP:WEB_PORT DISPLAY_IP:DISPLAY_PORT. \n'
    #         'e.g. python {0} 172.17.51.1:7788 172.17.51.1:18900'.format(
    #             sys.argv[0]))
    #     exit(0)
    # print('{} running at {} and getting data from {}'.format(
    #     sys.argv[0], sys.argv[1], sys.argv[2]))
    web_ip, web_port = '172.17.15.21','7788'#sys.argv[1].split(':')
    #DISPLAY_IP, DISPLAY_PORT = sys.argv[2].split(':')
    app.run(host=web_ip, port=int(web_port))
