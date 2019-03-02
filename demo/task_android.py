from utils.dataflow import *

from flask import Flask
import _thread


app = Flask(__name__)

labels = []

def get_data():
    global labels
    while True:
        label = dataflow.getData(inport=20003) #get the labels
        if label!=None:
            if len(label)>0:
                labels.append(label[0])
        else:
            labels.append('None')
        print('labels:',labels)
        if len(labels)>5:
            labels = []

@app.route("/")
def hello():
    global labels
    print('lables are:',labels)
    return '{}'.format(labels)


if __name__ == '__main__':
    _thread.start_new_thread( get_data, () )

    web_ip, web_port = '192.168.1.6','7788'
    app.run(host=web_ip, port=int(web_port))
