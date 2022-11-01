import random
from colorama import init
from termcolor import colored
import copy
init()

POSSIBLE_COLOURS: list = ["BLUE", "RED", "WHITE", "GREEN", "MAGENTA", "YELLOW"]
CAPACITY: int = 6
# test case 1

level = 4
bnum = 6


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
  for i in bottles:
    h += max(len(set(i))-1,0)
  return h


class Node:
  count = 1
  stop = False
  def __init__(self, bottles,depth, parrent) -> None:
      self.parrent = parrent
      self.bottles: list = bottles
      self.next: list = []
      self.depth: int = depth
      self.isWon: bool = False
      self.idx = Node.count
      Node.count+=1
      self.heuristic = heuristicCal(self.bottles)
      self.greed = 0
  def __str__(self) -> str:
    _res = ""
    tree = ""
    for i in range(self.depth):
      _res+="---"
      tree+="   "
    # _res+="*"
    res =  _res+"depth: "+  str(self.depth) +",idx: " + str(self.get_idx()) + "       p_idx"+ str(-1 if self.parrent is None  else self.parrent.idx) + '\n'
    for i in range(len(self.bottles)):
      res +=tree+ str(i) + "|"
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

  # def print_depth(self,depth):
  #   res = ""
  #   if self.get_depth() == depth:
  #     res += self.__str__()
  #   if len(self.get_next()) != 0:
  #     for i in self.get_next():
  #       res += i.print_depth(depth)
  #   return res

  def AStar(self)->str:
    
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
        queue += [self.next[i].heuristic +self.next[i].greed]
        idx += [self.next[i].heuristic +self.next[i].greed]
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


  def dfs_random(self,depth)->str:
    
    res = self.__str__()
    if Node.stop: return ""

    
    if allSorted(self.get_bottles()):
      Node.stop = True
      return res
    if self.get_depth() > depth: return res
    res += self.proceed()

    if len(self.get_next()) != 0:
      ar = list(range(len(self.get_next())))
      for i in range(len(self.get_next())):
        if Node.stop: return res
        x = random.choice(ar)
        ar.remove(x)
        res += self.get_next()[x].dfs_random(depth)
        
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
          pour(bottles,j,i)
          if self.antiDetour(bottles):
            a = Node(bottles,self.depth+1,self)
            if len(self.bottles[j]) != 0: a.greed = 1
            self.add_next(a)
            

          

    for i in range(len(self.bottles)-1,-1,-1):
      if len(self.bottles[i]) == 0: continue
      for j in range(i-1,-1,-1):
        if len(self.bottles[j]) == 0 or self.bottles[i][-1] == self.bottles[j][-1]:

          bottles = copy.deepcopy(self.bottles)
          pour(bottles,j,i)

          if self.antiDetour(bottles):
            a = Node(bottles,self.depth+1,self)
            if len(self.bottles[j]) != 0: a.greed = 1
            self.add_next(a)

    if len(self.get_next()) == 0: res += '----Stuck'
    return res
def main():

  b1 = []
  b2 = []
  b3 = []
  b4 = []
  b5 = []
  b6 =[]
  for i in range(level):

    b2+=[POSSIBLE_COLOURS[(i+1)%5]]
    b3+=[POSSIBLE_COLOURS[(i+4)%5]]
    b4+=[POSSIBLE_COLOURS[(i+3)%5]]
    b5+=[POSSIBLE_COLOURS[(i+2)%5]]
    b6+=[POSSIBLE_COLOURS[(i+5)%5]]
  
  if(bnum==3): root = Node([b1,b2,b3],0,None)
  elif(bnum==4): root = Node([b1,b2,b3,b4],0,None)
  elif(bnum==5): root = Node([b1,b2,b3,b4,b5],0,None)
  else: root = Node([b1,b2,b3,b4,b5,b6],0,None)
  # print(root.dfs_random(4))
  # print(root.dfs(100))
  print(root.AStar())
  # root.proceed()
  # print(root.print_dfs())
  # print(root)
  # print(root.print_dfs())
  print(root.node_count())
if __name__ == '__main__':
    main()