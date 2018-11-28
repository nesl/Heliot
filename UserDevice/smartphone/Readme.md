# Setting up Android Smartphone to receive notifications


## Steps on an Ubuntu Machine.
### We recommend Host-2 (Mininet machine) to be used for this. 

#### 1. Install python packages
```
$ pip install --upgrade pip==9.0.1
$ sudo pip install msgpack-rpc-python future flask
```

#### 2. Get script from our development branch
```
wget https://raw.githubusercontent.com/kumokay/placethings/master/config_ddflow_demo/sample_display_server.py
wget https://raw.githubusercontent.com/kumokay/placethings/master/config_ddflow_demo/sample_flask_server.py
```

#### 3. Run the actuator (display server)
```
python sample_display_server.py DISPLAY_SERVER_IP:DISPLAY_SERVER_PORT
# e.g. python sample_display_server.py 172.17.51.1:18900
```
In current case the DISPLAY_SERVER_IP is the ip of the Mininet machine.

#### 4. Run the web server which gets result from the display server and shows the alert on a web page
```
python sample_flask_server.py WEB_SERVER_IP:WEB_SERVER_PORT DISPLAY_SERVER_IP:DISPLAY_SERVER_PORT
# e.g. python sample_flask_server.py 172.17.51.1:7788 172.17.51.1:18900
```

In current case the WEB_SERVER_IP is the ip of the Mininet machine.

## Setting up the Smartphone
We are actively working on developing an Android App. Currently, we refresh the web address hosted by the
web server which is setup in the previous step on the user smartphone.

5. Use any web browser in the Smartphone to open a webpage at http://WEB_SERVER_IP:WEB_SERVER_PORT with auto-refresh enabled. you should be able to see the result once the whole system starts running.
<br/>

Another easy way is to use auto refresh Android application. We recommend using [Auto refresh web page utility](https://play.google.com/store/apps/details?id=com.murgoo.autowebpagerefresh). In the settings tab add http://WEB_SERVER_IP:WEB_SERVER_PORT 
