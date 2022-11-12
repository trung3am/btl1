import random
from colorama import init
from termcolor import colored
import time
import copy
init()
import os
import sys

POSSIBLE_COLOURS: list = ["BLUE", "RED", "WHITE", "GREEN", "MAGENTA", "YELLOW"]
CAPACITY: int = 6
# test case 1



def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System



def sorted(bottle)->bool:
  if len(bottle)==0:
    return True
  for i in bottle:
    if i != bottle[0]: return False
  return True

def allSorted(bottles)->bool:
  if len(bottles) == 0: return True
  for i in bottles:
    res = sorted(i)
    if res == False: return False
  for i in range(len(bottles)):
    if len(bottles[i])==0: continue
    for j in range(i+1,len(bottles)):
      if len(bottles[j])==0: continue
      if bottles[i][0] == bottles[j][0]: return False
  return res

def pour(bottles,j,i):
  while len(bottles[j])==0 or bottles[j][-1] == bottles[i][-1]:
    bottles[j]+=[bottles[i][-1]]
    bottles[i] = bottles[i][0:-1]
    if len(bottles[i]) ==0: break

def heuristicCal(bottles)->int:
  h = 0
  c = ""
  
  for i in bottles:
    if len(i)!=0: c= i[0]  
    count = 0
    for j in i:
      if c !=j:
        c = j 
        count +=1
    h+=count
    
  return h


class Node:
  speed = 0.2
  count = 1
  stop = False
  def __init__(self, bottles,depth, parrent,step) -> None:
      self.step = step
      self.parrent = parrent
      self.bottles: list = bottles
      self.next: list = []
      self.depth: int = depth
      self.isWon: bool = False
      self.idx = Node.count
      Node.count+=1
      self.heuristic = heuristicCal(self.bottles)
      self.uniformCost = 0
  def __str__(self) -> str:
    _res =self.step + "---\n" 
    res =  _res+"depth: "+  str(self.depth) +",idx: " + str(self.get_idx()) + "       p_idx"+ str(-1 if self.parrent is None  else self.parrent.idx) + " g(n): "+ str(self.heuristic) + " h(n): " +str(self.uniformCost)+ '\n'
    for i in range(len(self.bottles)):
      res += str(i) + "|"
      if len(self.bottles[i]) != 0:
        for j in range(len(self.bottles[i])):
          res += colored("███",str(self.bottles[i][j]).lower())
          # if j != len(self.bottles[i])-1: res += " "
      space = ""
      for i in range(CAPACITY- len(self.bottles[i])):
        space += "   "
      res += space + "| \n"
    
    if allSorted(self.bottles): res += "SORTED------------------------------ \n"
    print(res)
    return res
  def get_bottles(self)->list:
    return self.bottles

  def get_next(self)->list:
    return self.next

  def get_depth(self)->int:
    return self.depth

  def set_depth(self,depth):
    self.depth = depth

  def get_idx(self)->int:
    return self.idx

  def set_idx(self,idx):
    self.idx = idx

  def add_next(self, node):
    self.next += [node]

  def antiDetour(self,bottles)->bool:
    if self.parrent is None: return True
    if self.parrent.bottles == bottles: return False
    return self.parrent.antiDetour(bottles)

  def node_count(self)->int:
    n = 1 
    if  len(self.get_next()) >= 1:
      for i in self.get_next():
        n += i.node_count()
    return n


  def AStar(self)->str:
    # if self.parrent is not None: self.parrent.__str__()
    res = self.__str__()
    if Node.stop: return ""
    
    
    if allSorted(self.get_bottles()):
      Node.stop = True
      return res
    res += self.proceed()


    if len(self.get_next()) != 0:
      queue = []
      idx = []
      for i in range(len(self.next)):
        queue += [self.next[i].heuristic +self.next[i].uniformCost]
        idx += [self.next[i].heuristic +self.next[i].uniformCost]
      idx.sort()
      for i in idx:
        res+= self.next[queue.index(i)].AStar()
        queue[queue.index(i)] = -1
        if Node.stop: return res

    return res

  def dfs(self,depth)->str:
    
    res = self.__str__()
    if Node.stop: return ""
    if self.get_depth() >= depth: return ""
    
    if allSorted(self.get_bottles()):
      Node.stop = True
      return res
      
    res += self.proceed()

# this block is for non-random dfs
    if len(self.get_next()) != 0:
      for i in self.get_next():
        if Node.stop: return res
        res += i.dfs(depth)
          
    return res


  # def dfs_random(self,depth)->str:
    
  #   res = self.__str__()
  #   if Node.stop: return ""

    
  #   if allSorted(self.get_bottles()):
  #     Node.stop = True
  #     return res
  #   if self.get_depth() > depth: return res
  #   res += self.proceed()

  #   if len(self.get_next()) != 0:
  #     ar = list(range(len(self.get_next())))
  #     for i in range(len(self.get_next())):
  #       if Node.stop: return res
  #       x = random.choice(ar)
  #       ar.remove(x)
  #       res += self.get_next()[x].dfs_random(depth)
        
  #   return res


  def proceed(self):
    time.sleep(Node.speed)
    # clear()
    res= ""
    if Node.stop == True: return ""
    
    if allSorted(self.bottles): 
      Node.stop = True
      return res
      
    for i in range(len(self.bottles)):
      if len(self.bottles[i]) == 0: continue
      for j in range(i+1,len(self.bottles)):

        if len(self.bottles[j]) == 0 or self.bottles[i][-1] == self.bottles[j][-1]:

          bottles = copy.deepcopy(self.bottles)
          pour(bottles,j,i)
          if self.antiDetour(bottles):
            a = Node(bottles,self.depth+1,self, "step: "+str(i)+"->" + str(j))
            if len(self.bottles[j]) == 0: a.uniformCost = 1
            self.add_next(a)
            

          

    for i in range(len(self.bottles)-1,-1,-1):
      if len(self.bottles[i]) == 0: continue
      for j in range(i-1,-1,-1):
        if len(self.bottles[j]) == 0 or self.bottles[i][-1] == self.bottles[j][-1]:

          bottles = copy.deepcopy(self.bottles)
          pour(bottles,j,i)

          if self.antiDetour(bottles):
            a = Node(bottles,self.depth+1,self,"step: "+str(i)+"->" + str(j))
            if len(self.bottles[j]) != 0 and self.heuristic != 0: a.uniformCost = 1
            self.add_next(a)

    if len(self.get_next()) == 0: res += '----Stuck'
    return res

def makeBottle(bnum, colourNum, fillIndex, Nunfilledbottle):
  t = int(fillIndex*bnum/colourNum) +1
  b = []
  bottles = []
  for i in range(bnum):
    bottles += [copy.deepcopy(b)]
  colour = POSSIBLE_COLOURS[0:colourNum]
  n = [0]*colourNum
  for i in bottles:
    for x in range(fillIndex):
      c = random.choice(colour)
      n[colour.index(c)]+=1
      if n[colour.index(c)] >= t:
        colour.remove(c)
        n.remove(t)
      i.append(c)
  for i in range(Nunfilledbottle):
    bottles += [copy.deepcopy(b)]
  return bottles

def takeInput():
  print("please enter number of filled bottle(2-10): ")
  x = int(input())
  print("please enter number of colour allowed(2-6): ")
  y = int(input())
  print("please enter number of pre-filled liquid(1-5): ")
  z = int(input())
  print("please enter number of un filled bottle(1-3): ")
  t = int(input())
  print("please enter speed(0 - 0.5) ")
  s = float(input())
  Node.speed = s
  return makeBottle(x,y,z,t)
  
def testcase():
# testcase 5 filled bottles 5 different colours, filled to 4/6 capacity and 1 unfilled bottle
  while(True):
    print("please input test case 1,2,3,4,5")
    i = input()
    if i == "1":
      return makeBottle(5,5,4,1)

# testcase 4 filled bottles 3 different colours, filled to 4/6 capacity and 1 unfilled bottle
    if i == "2":
      return makeBottle(4,3,4,1)

# testcase 3 filled bottles 3 different colours, filled to 4/6 capacity and 1 unfilled bottle
    if i == "3":
      return makeBottle(3,3,4,1)

# testcase 5 filled bottles 5 different colours, filled to 4/6 capacity and 2 unfilled bottle
    if i == "4":
      return makeBottle(5,5,4,2)

# testcase 7 filled bottles 6 different colours, filled to 4/6 capacity and 2 unfilled bottle
    if i == "5":
      return makeBottle(7,6,4,2)
    if i == "6":
      return  [['RED', 'BLUE', 'YELLOW', 'RED'], ['BLUE', 'YELLOW', 'RED', 'BLUE'], ['WHITE', 'MAGENTA', 'YELLOW', 'YELLOW'], ['RED', 'BLUE', 'RED', 'GREEN'], ['MAGENTA', 'MAGENTA', 'BLUE', 'MAGENTA'], ['MAGENTA', 'WHITE', 'GREEN', 'YELLOW'], ['WHITE', 'GREEN', 'WHITE', 'GREEN'], [], []]
    print("invalid input")
def main():
  Node.speed = 0

  bottle = testcase()


  bDfs = copy.deepcopy(bottle)
  bAstar = copy.deepcopy(bottle)
  rootDFS = Node(bDfs,0,None,"start")
  
  rootAstar = Node(bAstar,0,None,"start")
  clear()
  print(bottle)
  print("press a for astar, d for dfs, else for both")
  x = input()
  if x =="a":
    AstarTime = time.time()
    rootAstar.AStar()
    AstarTime = time.time() - AstarTime
    print("ASTAR DONE ----------------------------------------------------------------------------------------------------------" + "\n Astar time: " + str(AstarTime) + "s Node traversed: " + str(rootAstar.node_count()))
  elif x == "d":
    Node.stop = False
    DFSTime = time.time()
    rootDFS.dfs(50)
    DFSTime = time.time() - DFSTime
    print("DFS DONE ----------------------------------------------------------------------------------------------------------" + "\n DFS time: " + str(DFSTime) + "s Node traversed: " + str(rootDFS.node_count()))
  else:
    AstarTime = time.time()
    rootAstar.AStar()
    AstarTime = time.time() - AstarTime
    print("ASTAR DONE ----------------------------------------------------------------------------------------------------------" + "\n Astar time: " + str(AstarTime) + "s Node traversed: " + str(rootAstar.node_count()))
    Node.stop = False
    DFSTime = time.time()
    rootDFS.dfs(50)
    DFSTime = time.time() - DFSTime
    print("DFS DONE ----------------------------------------------------------------------------------------------------------" + "\n DFS time: " + str(DFSTime) + "s Node traversed: " + str(rootDFS.node_count()))
    print("\n Astar time: " + str(AstarTime) + "s Node traversed: " + str(rootAstar.node_count()) + "| DFS time: " + str(DFSTime) + "s Node traversed: " + str(rootDFS.node_count()))
if __name__ == '__main__':
    main()