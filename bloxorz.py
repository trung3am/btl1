import random
from colorama import init
from termcolor import colored
import os
import sys
import copy
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
    Game.map = [[0 for x in range(n)] for x in range(m)]
    Game.wincheck = [False]
    Game.n = n
    Game.m = m

  def initgame(self):
    Game.wincheck[0] = False

    Game.map[Game.goal[0]][Game.goal[1]]= 0
    if Game.curr[0] <Game.n and Game.curr[0] >= 0 and Game.curr[1] <Game.m and Game.curr[1] >= 0:
      Game.map[Game.curr[0]][Game.curr[1]]=0
    if Game.curr[2] <Game.n and Game.curr[2] >= 0 and Game.curr[3] <Game.m and Game.curr[3] >= 0:
      Game.map[Game.curr[2]][Game.curr[3]]=0
      
    Game.goal[0]=random.randint(0,Game.n-1)
    Game.goal[1]=random.randint(0,Game.m-1)
    Game.curr[0]=random.randint(0,Game.n-1)
    Game.curr[1]=random.randint(0,Game.m-1)
    Game.curr[2]=Game.curr[0]
    Game.curr[3]=Game.curr[1]
    Game.map[Game.goal[0]][Game.goal[1]]= 1
    Game.map[Game.curr[0]][Game.curr[1]]= 2

  @staticmethod
  def erase():
    for i in Game.curr:
      if i>=0 and i <Game.n: continue
      else: return
    if Game.curr[0] <Game.n and Game.curr[0] >= 0 and Game.curr[1] <Game.m and Game.curr[1] >= 0:
      Game.map[Game.curr[0]][Game.curr[1]]=0
    if Game.curr[2] <Game.n and Game.curr[2] >= 0 and Game.curr[2] <Game.m and Game.curr[2] >= 0:
      Game.map[Game.curr[2]][Game.curr[3]]=0
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
  def laprint()->str:
    res = ""
    for i in range(Game.n):
      res += '\n '+str(i) + '|' 
      for j in range(Game.m):

        if Game.map[i][j]==0: res += "██"
        if Game.map[i][j]==1: res+= colored("██",'blue')
        if Game.map[i][j]==2: res+= colored("██",'magenta')
        if Game.map[i][j]==3: res+= colored("██",'red','on_yellow')
        if i == Game.n-1:
          if j == 0:
            _res='\n   '
          _res+= str(j)+" "
          if j == Game.m-1: res+=_res
      res += " |"
    print(res)
  
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
      if i>=0 and i <Game.n: continue
      else:
        print("you lose kek")
        self.initgame()
    Game.loadcurr()


    clear()
    Game.laprint()
    if Game.curr[0:2] == Game.curr[2:4] and Game.curr[0:2]==Game.goal:
      print("Ok u win, press r to play again")
      Game.wincheck[0]=True

    print(Game.curr)
  def play(self):
    while True:
    
      move = input()
      if move =="e": break
      if move =="r": 
        self.initgame()
        continue
        
      if not Game.wincheck[0]: self.makemove(move)



class Node:
  stop = False
  count = 0
  gameGoal: list = Game.goal
  def __init__(self, depth, curr, goal) -> None:

    Node.count+=1
    self.lost = False
    self.idx = Node.count
    self.depth: int = depth
    self.next: list = []
    self.curr: list = curr
    self.goal: list = goal
  
  def __str__(self) -> str:
    res = ""
    for i in range(Game.n):
      res += '\n '+str(i) + '|' 
      for j in range(Game.m):

        if Game.map[i][j]==0: res += "██"
        if Game.map[i][j]==1: res+= colored("██",'blue')
        if Game.map[i][j]==2: res+= colored("██",'magenta')
        if Game.map[i][j]==3: res+= colored("██",'red','on_yellow')
        if i == Game.n-1:
          if j == 0:
            _res='\n   '
          _res+= str(j)+" "
          if j == Game.m-1: res+=_res
      res += " |"
    print(res)

  def proceed(self):
    Game.laprint()
    Game.erase()
    res = ""
    if Node.stop: return
    if self.curr[0:2] == self.curr[2:4] and self.curr[0:2]==self.goal:
      Node.stop = True
      return
    for i in self.curr:
      if i>=0 and i <Game.n: continue
      else:
        self.lost = True
        res+="---LOST"
        return
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
    a = Node(self.depth+1,curr,self.goal)
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
    a = Node(self.depth+1,curr,self.goal)
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
    a = Node(self.depth+1,curr,self.goal)
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
    a = Node(self.depth+1,curr,self.goal)
    self.next +=[a]

  def cascade(self,depth):
    res =""
    if Node.stop: return
    if self.depth > depth: return
    self.proceed()
    if self.lost: return
    for i in self.next:
      if Node.stop: return
      i.cascade(depth)

  def cascade_random(self,depth):
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
      self.next[x].cascade_random(depth)
    return



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
  # curr[3]=curr[1]
  game =  Game(7,7)

  
  print("awsd to move e to end, r to reset, dont kill urself, thx")
  game.play()


if __name__ == '__main__':
    main()