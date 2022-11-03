import random
from colorama import init
from termcolor import colored
import os
import sys
import copy
import time
init()

def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


class Game:
  goal = [0,0]
  n = 0
  m = 0
  map = []
  curr =[0,0,0,0]
  wincheck = [False]
  def __init__(self, n,m) -> None:
    Game.goal = [0,0]
    Game.curr = [0,0,0,0]
    Game.map = [[5 for x in range(n+3)] for x in range(m+3)]
    Game.wincheck = [False]
    Game.n = n
    Game.m = m
  @staticmethod
  def bordering():
    Game.wincheck[0] = False
    for i in range(len(Game.map)):
      for j in range(len(Game.map)):
        if Game.map[i][j]!=1 and Game.map[i][j]!=7 and Game.map[i][j]!=8: Game.map[i][j]=5
        if Game.map[i][j]==5 and i>1 and i < len(Game.map)-2 and j>1 and j < len(Game.map)-2: Game.map[i][j]=0
        
  @staticmethod
  def detrailing():
    
    for i in range(len(Game.map)):
      for j in range(len(Game.map)):
        if Game.map[i][j]!=1: Game.map[i][j]=5
        if Game.map[i][j]==5 and i>1 and i < len(Game.map)-2 and j>1 and j < len(Game.map)-2: Game.map[i][j]=0

  @staticmethod
  def verticalObstacle(start,end, wPos):
    for i in range(end -start):
      Game.map[start+i][wPos] = 8

  @staticmethod
  def HorizontalObstacle(start,end, hPos):
    for i in range(end -start):
      Game.map[hPos][start+i] = 8

  @staticmethod
  def trailing(curr):
    Game.map[curr[0]][curr[1]]=7
    Game.map[curr[2]][curr[3]]=7

    if Game.goal==curr[0:2]:
      Game.map[Game.goal[0]][Game.goal[1]]=1
    if Game.goal==curr[2:4]:
      Game.map[Game.goal[0]][Game.goal[1]]=1

  def initgame(self):
    Game.bordering()
    Game.map[Game.goal[0]][Game.goal[1]]= 0
    # if Game.curr[0] <Game.n and Game.curr[0] >= 0 and Game.curr[1] <Game.m and Game.curr[1] >= 0:
    Game.map[Game.curr[0]][Game.curr[1]]=0
    # if Game.curr[2] <Game.n and Game.curr[2] >= 0 and Game.curr[3] <Game.m and Game.curr[3] >= 0:
    Game.map[Game.curr[2]][Game.curr[3]]=0
    
    Game.goal[0]=random.randint(2,Game.n-1)
    Game.goal[1]=random.randint(2,Game.m-1)
    Game.curr[0]=random.randint(2,Game.n-1)
    Game.curr[1]=random.randint(2,Game.m-1)
    Game.curr[2]=Game.curr[0]
    Game.curr[3]=Game.curr[1]
    Game.map[Game.goal[0]][Game.goal[1]]= 1
    Game.map[Game.curr[0]][Game.curr[1]]= 2

  @staticmethod
  def erase():
    # for i in Game.curr:
    #   if i>=0 and i <len(Game.map): continue
    #   else: return
    # if Game.curr[0] <Game.n and Game.curr[0] >= 0 and Game.curr[1] <Game.m and Game.curr[1] >= 0:
    Game.map[Game.curr[0]][Game.curr[1]]=0
    # if Game.curr[2] <Game.n and Game.curr[2] >= 0 and Game.curr[2] <Game.m and Game.curr[2] >= 0:
    Game.map[Game.curr[2]][Game.curr[3]]=0
    Game.bordering()
    if Game.goal==Game.curr[0:2]:
      Game.map[Game.goal[0]][Game.goal[1]]=1
    if Game.goal==Game.curr[2:4]:
      Game.map[Game.goal[0]][Game.goal[1]]=1
    
  @staticmethod
  def loadcurr():
    Game.map[Game.curr[0]][Game.curr[1]]=2
    Game.map[Game.curr[2]][Game.curr[3]]=2

    if Game.goal==Game.curr[0:2]:
      Game.map[Game.goal[0]][Game.goal[1]]=3
    if Game.goal==Game.curr[2:4]:
      Game.map[Game.goal[0]][Game.goal[1]]=3

  @staticmethod
  def loadcurr():
    Game.map[Game.curr[0]][Game.curr[1]]=2
    Game.map[Game.curr[2]][Game.curr[3]]=2

    if Game.goal==Game.curr[0:2]:
      Game.map[Game.goal[0]][Game.goal[1]]=3
    if Game.goal==Game.curr[2:4]:
      Game.map[Game.goal[0]][Game.goal[1]]=3

  @staticmethod
  def laprint()->str:
    res = ""
    for i in range(len(Game.map)):
      res += '\n '+ '|' 
      for j in range(len(Game.map)):
        temp =""
        if Game.map[i][j]==5 or  Game.map[i][j]==8 : temp= colored("██",'green')
        if Game.map[i][j]==0 : temp = "██"
        
        res +=temp
        if Game.map[i][j]==1: res+= colored("██",'blue')
        if Game.map[i][j]==2: res+= colored("██",'magenta')
        if Game.map[i][j]==3: res+= colored("██",'red','on_yellow')

      res += " |"
    print(res)
    return res
  
  def makemove(self, move):

    Game.erase()
    if move == "a":
      if Game.curr[1]==Game.curr[3] and Game.curr[0]==Game.curr[2]:
        Game.curr[1]-=2
        Game.curr[3]-=1
      elif Game.curr[0]==Game.curr[2]:
        Game.curr[1]-=1
        Game.curr[3]-=2
      else:
        Game.curr[1]-=1
        Game.curr[3]-=1    

    if move == "d":
      if Game.curr[1]==Game.curr[3] and Game.curr[0]==Game.curr[2]:
        Game.curr[1]+=1
        Game.curr[3]+=2
      elif Game.curr[0]==Game.curr[2]:
        Game.curr[1]+=2
        Game.curr[3]+=1
      else:
        Game.curr[1]+=1
        Game.curr[3]+=1    

    if move == "w":
      if Game.curr[1]==Game.curr[3] and Game.curr[0]==Game.curr[2]:
        Game.curr[0]-=2
        Game.curr[2]-=1
      elif Game.curr[1]==Game.curr[3]:
        Game.curr[0]-=1
        Game.curr[2]-=2
      else:
        Game.curr[0]-=1
        Game.curr[2]-=1  

    if move == "s":
      if Game.curr[1]==Game.curr[3] and Game.curr[0]==Game.curr[2]:
        Game.curr[0]+=1
        Game.curr[2]+=2
      elif Game.curr[1]==Game.curr[3]:
        Game.curr[0]+=2
        Game.curr[2]+=1
      else:
        Game.curr[0]+=1
        Game.curr[2]+=1
    for i in Game.curr:
      if i>1 and i <=Game.n: continue
      else:
        
        Game.wincheck[0]= True
        Game.loadcurr()
        clear()
        Game.laprint()
        print(Game.curr)
        print("you lose kek")
        return
    

    Game.loadcurr()
    clear()
    Game.laprint()
    if Game.curr[0:2] == Game.curr[2:4] and Game.curr[0:2]==Game.goal:
      print("Ok u win, press r to play again")
      Game.wincheck[0]=True

    print(Game.curr)
  def play(self):
    self.initgame()
    clear()
    Game.laprint()
    while True:
    
      move = input()
      if move =="e": break
      if move =="r": 
        self.initgame()
        continue
        
      if not Game.wincheck[0]: self.makemove(move)



class Node:
  stop = False
  count = 1
  gameGoal: list = Game.goal
  speed = 0.5
  def __init__(self, depth, curr,parrent) -> None:
    self.parrent = parrent
    self.win = False
    Node.count+=1
    self.lost = False
    self.idx = Node.count
    Node.count +=1
    self.depth: int = depth
    self.next: list = []
    self.curr: list = curr
    self.fitness = self.fitnessCal(Game.goal)

  def antiDetour(self,curr)->bool:
    if self.parrent is None: return True
    if self.parrent.curr == curr: return False
    return self.parrent.antiDetour(curr)

  def fitnessCal(self,goal)->int:
    fitness = 0
    if Game.map[self.curr[0]][self.curr[1]] == 5 or Game.map[self.curr[2]][self.curr[3]] == 5 or Game.map[self.curr[0]][self.curr[1]] == 8 or Game.map[self.curr[2]][self.curr[3]] == 8: return sys.maxsize
    for i in range(4):
      fitness += abs(self.curr[i]-goal[i%2])
    return fitness
  def __str__(self) -> str:
    Game.curr = self.curr
    Game.loadcurr()
    _res=""
    tree = ""
    # for i in range(self.depth):
    #   _res+="---"
    #   tree +="   "
    res=_res + "depth: "+  str(self.depth) +", id: " + str(self.idx) + ", p_id: " + str(self.parrent.idx if self.parrent is not None else "root") + '\n' 
    res+= _res + "curr: "+ str(self.curr) + ", goal: " + str(Game.goal) + ", fitness: " + str(self.fitness) + '\n'
    for i in range(len(Game.map)):
      # res +=tree
      res += '\n '+ tree+'|' 
      for j in range(len(Game.map)):
        temp =colored("██",'grey')
        if Game.map[i][j]==5: temp= colored("██",'green')
        if Game.map[i][j]==8: temp= colored("██",'green')
        if Game.map[i][j]==0 : temp = "██"
        
        
        if Game.map[i][j]==1: temp= colored("██",'blue')
        if Game.map[i][j]==2: temp= colored("██",'magenta')
        if Game.map[i][j]==3: temp= colored("██",'red','on_yellow')
        res +=temp
      res += " |"

    if self.lost: res += "\n----------LOST"
    if self.win: res += "\n----------WIN*******"
    print(res)
    Game.erase()
    return res

  def proceed(self):
    # self.trailing()
    
    time.sleep(Node.speed)
    clear()
    res = ""
    
    if Game.map[self.curr[0]][self.curr[1]] == 5 or Game.map[self.curr[2]][self.curr[3]] == 5 or Game.map[self.curr[0]][self.curr[1]] == 8 or Game.map[self.curr[2]][self.curr[3]] == 8: 
      self.lost = True
      res+= self.__str__()
      Game.bordering()
      return res


    if Node.stop: 
      res+= self.__str__()
      return res
    if self.curr[0:2] == self.curr[2:4] and self.curr[0:2]==Game.goal:
      Node.stop = True
      self.win = True
      res+= self.__str__()
      return res

    curr = copy.deepcopy(self.curr)
    if curr[1]==curr[3] and curr[0]==curr[2]:
      curr[1]-=2
      curr[3]-=1
    elif curr[0]==curr[2]:
      curr[1]-=1
      curr[3]-=2
    else:
      curr[1]-=1
      curr[3]-=1    
    if self.antiDetour(curr):
      a = Node(self.depth+1,curr,self)
      self.next +=[a]

    curr = copy.deepcopy(self.curr)
    if curr[1]==curr[3] and curr[0]==curr[2]:
      curr[1]+=1
      curr[3]+=2
    elif curr[0]==curr[2]:
      curr[1]+=2
      curr[3]+=1
    else:
      curr[1]+=1
      curr[3]+=1    
    if self.antiDetour(curr):
      a = Node(self.depth+1,curr,self)
      self.next +=[a]

    curr = copy.deepcopy(self.curr)
    if curr[1]==curr[3] and curr[0]==curr[2]:
      curr[0]-=2
      curr[2]-=1
    elif curr[1]==curr[3]:
      curr[0]-=1
      curr[2]-=2
    else:
      curr[0]-=1
      curr[2]-=1  
    if self.antiDetour(curr):
      a = Node(self.depth+1,curr,self)
      self.next +=[a]

    curr = copy.deepcopy(self.curr)
    if curr[1]==curr[3] and curr[0]==curr[2]:
      curr[0]+=1
      curr[2]+=2
    elif curr[1]==curr[3]:
      curr[0]+=2
      curr[2]+=1
    else:
      curr[0]+=1
      curr[2]+=1
    if self.antiDetour(curr):
      a = Node(self.depth+1,curr,self)
      self.next +=[a]
    res+= self.__str__()
    
  def trailing(self):
    Game.trailing(self.curr)
    if self.parrent is not None: self.parrent.trailing()

  def dfs(self,depth):
    res =""
    if Node.stop: return
    
    self.proceed()
    if self.depth >= depth: return
    if self.lost: return
    for i in self.next:
      if Node.stop: return
      i.dfs(depth)

  def geneticAlg(self):
    res =""
    if Node.stop: return
    
    self.proceed()
    if self.lost: return
    ar = []
    idx = []
    for i in self.next:
      if Node.stop: return
      if i.fitness < sys.maxsize: ar += [i.fitness]
      idx += [i.fitness]
    ar.sort()
    for i in ar:
      self.next[idx.index(i)].geneticAlg()
      idx.remove(i)

  def dfs_random(self,depth):
    res =""
    if Node.stop: return
    if self.depth > depth: return
    self.proceed()
    if self.lost: return
    ar = list(range(len(self.next)))
    for i in range(len(self.next)):
      if Node.stop: return
      x = random.choice(ar)
      ar.remove(x)
      self.next[x].dfs_random(depth)
    return res



def main():
  # m=7
  # n=7
  # curr= [0,0,0,0]
  # goal = [0,0]
  # goal[0]=random.randint(0,n-1)
  # goal[1]=random.randint(0,m-1)
  # curr[0]=random.randint(0,n-1)
  # curr[1]=random.randint(0,m-1)
  # curr[2]=curr[0]
  game =  Game(24,24)
  game.initgame()
  # game.play()
  # print("awsd to move e to end, r to reset, dont kill urself, thx")
  
  
  Game.map[Game.goal[0]][Game.goal[1]]=0
  Game.map[Game.curr[0]][Game.curr[1]]=0
  Game.map[Game.curr[2]][Game.curr[3]]=0
  Game.goal = [2,2]
  Game.map[Game.goal[0]][Game.goal[1]]=1
  Game.curr = [3,4,3,4]
  # Game.verticalObstacle(2,8,6)
  # Game.verticalObstacle(5,11,9)
  # Game.verticalObstacle(16,20,15)
  # Game.HorizontalObstacle(2,8,9)
  # Game.HorizontalObstacle(6,14,12)
  # Game.HorizontalObstacle(16,23,16)
  root = Node(0,Game.curr, None)
  # root.dfs(6)
  Node.speed = 0.2
  root.geneticAlg()


if __name__ == '__main__':
    main()