from colorama import init
from termcolor import colored
import copy
init()

POSSIBLE_COLOURS: list = ["BLUE", "RED", "ORANGE", "GREEN", "PURPLE", "YELLOW"]
CAPACITY: int = 5
# test case 1

level = 2
bnum = 3


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

class Node:
  count = 1
  stop = False
  def __init__(self, bottles,depth) -> None:
      self.bottles: list = bottles
      self.next: list = []
      self.depth: int = depth
      self.isWon: bool = False
      self.idx = Node.count
      Node.count+=1
  def __str__(self) -> str:
    res = "depth: "+  str(self.depth) +",idx: " + str(self.get_idx()) + '\n'
    for i in range(len(self.bottles)):
      res += str(i) + "["
      if len(self.bottles[i]) != 0:
        for j in range(len(self.bottles[i])):
          res += colored("|",str(self.bottles[i][j]).lower())
          if j != len(self.bottles[i])-1: res += ","
      res += "] \n"
    if allSorted(self.bottles): res += "SORTED------------------------------ \n"
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

  
  def node_count(self)->int:
    n = 1 
    if  len(self.get_next()) >= 1:
      for i in self.get_next():
        n += i.node_count()
    return n

  def print_depth(self,depth):
    res = ""
    if self.get_depth() == depth:
      res += self.__str__()
    if len(self.get_next()) != 0:
      for i in self.get_next():
        res += i.print_depth(depth)
    return res

  def cascade(self,depth)->bool:
    if self.get_depth() > depth: return
    if allSorted(self.get_bottles()):
      return True
    self.proceed()

    if len(self.get_next()) != 0:
      for i in self.get_next():
        res = i.cascade(depth)
        
    return False
    # dfs
  def print_cascade(self):
    res: str = self.__str__()
    if allSorted(self.bottles):
      Node.stop = True
      return res
    if len(self.get_next()) != 0:
      for i in self.get_next():
        if Node.stop: return res
        res += i.print_cascade()
    return res
  
    # bfs
  def print_cascade(self):
    res: str = self.__str__()
    if allSorted(self.bottles):
      Node.stop = True
      return res
    if len(self.get_next()) != 0:
      for i in self.get_next():
        if Node.stop: return res
        res += i.print_cascade()
    return res

  # def 

  def proceed(self):
    if allSorted(self.bottles): return
    for i in range(len(self.bottles)):
      if len(self.bottles[i]) == 0: continue
      for j in range(i+1,len(self.bottles)):
        if len(self.bottles[j]) == 0 or self.bottles[i][-1] == self.bottles[j][-1]:

          bottles = copy.deepcopy(self.bottles)

          bottles[j]+=[bottles[i][-1]]
          
          bottles[i] = bottles[i][0:-1]

          a = Node(bottles,self.depth+1)


          self.add_next(a)

    for i in range(len(self.bottles)-1,-1,-1):
      if len(self.bottles[i]) == 0: continue
      for j in range(i-1,-1,-1):
        if len(self.bottles[j]) == 0 or self.bottles[i][-1] == self.bottles[j][-1]:

          bottles = copy.deepcopy(self.bottles)
          bottles[j]+=[bottles[i][-1]]

          bottles[i] = bottles[i][0:-1]

          a = Node(bottles,self.depth+1)
 
          self.add_next(a)

def main():

  b1 = []
  b2 = []
  b3 = []
  for i in range(level):
    b1+=[POSSIBLE_COLOURS[i%2]]
    b2+=[POSSIBLE_COLOURS[i%2]]
  
  root = Node([b1,b2,b3],0)
  root.cascade(2)
  # root.proceed()
  # print(root.print_cascade())
  print(root)
  print(root.print_cascade())
  print(root.node_count())
if __name__ == '__main__':
    main()