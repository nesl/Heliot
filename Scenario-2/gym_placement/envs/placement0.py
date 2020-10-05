import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class placementClass0(gym.Env):

  def __init__(self):
      # actions -> compute placement
      self.action_space = spaces.Box(low=np.array([0]), high=np.array([4]), dtype=np.uint8)

      # given delay of the network
      #self.observation_espace = spaces.Box(low=0, high=5,shape=(1), dtype=np.int)


  def step(self, action):
      print("I am taking a step")


      self.reward = None
      self.done = False
      self.next_state = None


      #take the action here, and decide next state and reward
      if action == 0:  # move left
          self.reward = 1
          self.next_state = 1
      elif action == 1:
          self.reward = 1
          self.next_state = 2
      elif action == 2:
          self.reward = 1
          self.next_state = 3
      elif action == 3:
          self.reward = 2
          self.next_state = 4
      elif action == 4:
          self.reward = 1
          self.next_state = 0
      else:  # should not be here
          raise ValueError("Invalid action")



      info = {}  # additional data, not to be used for training
      return self.next_state, self.reward, self.done, info


  def reset(self):
      self.reward = None
      self.done = False
      self.next_state = None
      self.steps = 0

  def render(self, mode='human', close=False):
      pass
