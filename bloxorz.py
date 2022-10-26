import random
from colorama import init
from termcolor import colored
import os
import sys
import copy
init()

n=40
m=40
wincheck = [False]

map = [[0 for x in range(n)] for x in range(m)]

def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System

curr = [7,3,7,3]
goal = [15,5]
def initgame():
  wincheck[0] = False
  
  map[goal[0]][goal[1]]= 0
  erase(curr)
  goal[0]=random.randint(0,n-1)
  goal[1]=random.randint(0,m-1)
  
  curr[0]=random.randint(0,n-1)
  curr[1]=random.randint(0,m-1)
  curr[2]=curr[0]
  curr[3]=curr[1]


  map[goal[0]][goal[1]]= 1
  map[curr[0]][curr[1]]= 2

def erase(curr):
  for i in curr:
    if i>0 and i <n: continue
    else: return
  map[curr[0]][curr[1]]=0
  map[curr[2]][curr[3]]=0
  if goal==curr[0:2]:
    map[goal[0]][goal[1]]=1
  if goal==curr[2:4]:
    map[goal[0]][goal[1]]=1

def loadcurr(curr):
  map[curr[0]][curr[1]]=2
  map[curr[2]][curr[3]]=2

  if goal==curr[0:2]:
    map[goal[0]][goal[1]]=3
  if goal==curr[2:4]:
    map[goal[0]][goal[1]]=3
  
def laprint():
  res = ""
  for i in range(n):
    res += '\n | '
    for j in range(m):

      if map[i][j]==0: res += " "
      if map[i][j]==1: res+= "O"
      if map[i][j]==2: res+= "X"
      if map[i][j]==3: res+= colored('X','red','on_yellow')
    res += " |"
  print(res)

def makemove(move):



  erase(curr)
  if move == "a":
    if curr[1]==curr[3] and curr[0]==curr[2]:
      curr[1]-=2
      curr[3]-=1
    elif curr[0]==curr[2]:
      curr[1]-=1
      curr[3]-=2
    else:
      curr[1]-=1
      curr[3]-=1    

  if move == "d":
    if curr[1]==curr[3] and curr[0]==curr[2]:
      curr[1]+=1
      curr[3]+=2
    elif curr[0]==curr[2]:
      curr[1]+=2
      curr[3]+=1
    else:
      curr[1]+=1
      curr[3]+=1    

  if move == "w":
    if curr[1]==curr[3] and curr[0]==curr[2]:
      curr[0]-=2
      curr[2]-=1
    elif curr[1]==curr[3]:
      curr[0]-=1
      curr[2]-=2
    else:
      curr[0]-=1
      curr[2]-=1  

  if move == "s":
    if curr[1]==curr[3] and curr[0]==curr[2]:
      curr[0]+=1
      curr[2]+=2
    elif curr[1]==curr[3]:
      curr[0]+=2
      curr[2]+=1
    else:
      curr[0]+=1
      curr[2]+=1
  for i in curr:
    if i>0 and i <n: continue
    else:
      print("you lose kek")
      initgame()
  loadcurr(curr)


  clear()
  laprint()
  if curr[0:2] == curr[2:4] and curr[0:2]==goal:
    print("Ok u win, press r to play again")
    wincheck[0]=True

  print(curr)


class Node:
  def __init__(self) -> None:
    pass


def play():
  while True:
  
    move = input()
    if move =="e": break
    if move =="r": 
      initgame()
      continue
      
    if not wincheck[0]: makemove(move)

def main():
  initgame()
  print("awsd to move e to end, r to reset, dont kill urself, thx")
  play()


if __name__ == '__main__':
    main()