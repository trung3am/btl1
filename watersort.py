import random
from colorama import init
from termcolor import colored
import copy
init()

POSSIBLE_COLOURS: list = ["BLUE", "RED", "WHITE", "GREEN", "MAGENTA", "YELLOW"]
CAPACITY: int = 6
# test case 1

level = 3
bnum = 5


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
    _res = ""
    for i in range(self.depth):
      _res+="---"
    # _res+="*"
    res =  _res+"depth: "+  str(self.depth) +",idx: " + str(self.get_idx()) + '\n'
    for i in range(len(self.bottles)):
      res +=_res+ str(i) + "|"
      if len(self.bottles[i]) != 0:
        for j in range(len(self.bottles[i])):
          res += colored("███",str(self.bottles[i][j]).lower())
          # if j != len(self.bottles[i])-1: res += " "
      space = ""
      for i in range(CAPACITY- len(self.bottles[i])):
        space += "   "
      res += space + "| \n"
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

  # def print_depth(self,depth):
  #   res = ""
  #   if self.get_depth() == depth:
  #     res += self.__str__()
  #   if len(self.get_next()) != 0:
  #     for i in self.get_next():
  #       res += i.print_depth(depth)
  #   return res

  def cascade(self,depth)->str:
    
    res = self.__str__()
    if Node.stop: return ""
    if self.get_depth() > depth: return ""
    
    if allSorted(self.get_bottles()):
      Node.stop = True
      return res
      
    res += self.proceed()

# this block is for non-random dfs
    if len(self.get_next()) != 0:
      for i in self.get_next():
        if Node.stop: return res
        res += i.cascade(depth)
          
    return res


  def cascade_random(self,depth)->str:
    
    res = self.__str__()
    if Node.stop: return ""
    if self.get_depth() > depth: return ""
    
    if allSorted(self.get_bottles()):
      Node.stop = True
      return res
     
    res += self.proceed()

    if len(self.get_next()) != 0:
      ar = list(range(len(self.get_next())))
      for i in range(len(self.get_next())):
        if Node.stop: return res
        x = random.choice(ar)
        ar.remove(x)
        res += self.get_next()[x].cascade_random(depth)
        
    return res


  def proceed(self):
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
    if len(self.get_next()) == 0: res += '----Stuck'
    return res
def main():

  b1 = []
  b2 = []
  b3 = []
  b4 = []
  b5 = []
  for i in range(level):

    # b2+=[POSSIBLE_COLOURS[i+1%5]]
    b3+=[POSSIBLE_COLOURS[i+1%5]]
    b4+=[POSSIBLE_COLOURS[i+1%5]]
    b5+=[POSSIBLE_COLOURS[i+1%5]]
  
  if(bnum==3): root = Node([b1,b2,b3],0)
  elif(bnum==4): root = Node([b1,b2,b3,b4],0)
  else: root = Node([b1,b2,b3,b4,b5],0)
  print(root.cascade_random(8))
  # print(root.cascade(5))
  # root.proceed()
  # print(root.print_cascade())
  # print(root)
  # print(root.print_cascade())
  # print(root.node_count())
if __name__ == '__main__':
    main()