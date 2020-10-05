"""
Single Edge and Server
1- Edge and Server network is created each time before executing the action.
2- We execute a set of actions in this network topology and collect the experience.
3- We use this set of experience to train the RL algorithm.
4- Units of delay between edge and server is in microseconds.

"""

import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from mininet.log import info
from mininet.cli import CLI

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

import time
import pickle
import random


dict_ip ={}
dict_ip['edge']  = '10.0.0.21'
dict_ip['server'] = '10.0.0.22'



class SingleSwitchTopo(Topo):
    "Single switch connected to edge and server hosts."
    def build(self,delay = 10):
        self.switch = self.addSwitch('s0')
        self.edge = self.addHost('edge', ip=dict_ip['edge'])
        self.server = self.addHost('server', ip=dict_ip['server'])

        linkopts = dict(delay=str(delay)+'us')
        self.addLink(self.switch, self.edge,**linkopts)
        self.addLink(self.switch, self.server)



class placementClass1(gym.Env):

  def __init__(self):
      # actions -> compute placement
      self.action_space = spaces.Discrete(5) #0 to 4 actions
      # given delay of the network, 10 us to 5000us
      self.low = np.array([10])
      self.high = np.array([5000])
      self.observation_space = spaces.Box(self.low, self.high, dtype=np.int)
      #Randomly sample the delay between the edge and server network
      self.state = random.randint(10, 50000) #delay is sampled in microseconds

  def step(self, action):
      #print("I am taking a step")

      self.reward = None
      self.done = False

      loop = False

      if loop ==False: # we will run the simulation
        self.CreateNetwork(self.state)## Create the network topology

      #take the action here

      #we will lauch the server and edge tasks here
        for host in self.net.hosts:
            if host.name=='server':
                server = host
            elif host.name =='edge':
                edge = host

        server.cmd('python3 server1.py &')
        time.sleep(0.05) #sleep for 0.5 seconds
        print(edge.cmd('python3 edge1.py '+str(action)))
        self.net.stop() #we need to stop the network

          #see what is the experience stored by the edge
        exp_file = pickle.load( open( "experience.p", "rb" ) )
          #print('exp_file',exp_file)
        self.reward = -1.0*exp_file[1]
        print self.state,action,self.reward

        self.state = 100000
        self.done = True

      info = {}  # additional data, not to be used for training
      return np.array(self.state), self.reward, self.done, info


  def reset(self):
      self.reward = None
      self.done = False
      self.state = random.randint(10, 50000) #delay is sampled in microseconds
      #self.state = 0
      self.steps = 0
      return np.array(self.state)

  def render(self, mode='human', close=False):
      pass


  def CreateNetwork(self, delay):
      topo = SingleSwitchTopo(delay=delay)
      self.net = Mininet(topo, link=TCLink)
      self.net.start()
      #CLI(self.net)
