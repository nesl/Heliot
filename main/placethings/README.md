# placethings

code taken from https://github.com/kumokay/placethings

## Overview
<b>placethings</b> allows developers to construct an experimental testbed to evaluate and verify their internet of things (IoT) applications during the development phase. <b>placethings</b>leverages the famous Mininet/Containernet emulation environment to span the emulation across virtual machines, containers, and bare metal devices. Developers can configure the emulated network and add virtual or real <b>THINGs</b>. Based on the network and devices configuration, <b>placethings</b> also suggests good solutions for deploying IoT applications.

<b>placethings</b> follows python PEP8 standard and is python 2-3 compatible.

### Features

- Allow user to <b>PLACE</b> virtual or real <b>THINGs</b> in a emulated network, such as
  - data sources, e.g. virtual or real sensors
  - network devices, e.g. switches, mininet switches
  - servers and edge devices, e.g. virtual machines, containers, and bare metal devices

- Define computation tasks and find an optimal solution to <b>PLACE</b> them on those virtual or bare metal servers and edge devices

## Installation

1. Install containernet
```
$ sudo apt-get install ansible git aptitude
$ git clone https://github.com/containernet/containernet.git
$ cd containernet/ansible
$ sudo ansible-playbook -i "localhost," -c local install.yml
$ cd ..
$ sudo python setup.py install
$ sudo py.test -v mininet/test/test_containernet.py
```

2. Intall ilp solvers and python packages
```
$ pip install --upgrade pip==9.0.1
$ sudo pip install msgpack-rpc-python numpy Pillow future networkx matplotlib six aenum pulp
$ sudo apt-get install glpk-utils
```

3. Run demo case
```
$ python main.py -tc test_ddflow_demo.Test -c config_ddflow_demo
```

run with -v option to print the output graphs

## Example

Al examples are in placethings/demo.
See https://github.com/nesl/Heliot/blob/dev/main/placethings/placethings/demo/README.md

```
$ python main.py -tc TESTCASE_FILE.TESTCASE -c CONFIGFILE

all TESTCASE_FILEs are in placethings/demo
TESTCASE is the name of each lcass

e.g.
$ python main.py -tc test_ddflow_demo.Test -c config_ddflow_demo
```

