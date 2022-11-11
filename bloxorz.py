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
  obstacle = []
  curr =[0,0,0,0]
  startCurr = [0,0,0,0]
  wincheck = [False]
  def __init__(self, n,m) -> None:
    Game.goal = [0,0]
    Game.curr = [0,0,0,0]
    Game.map = [[5 for x in range(n+3)] for x in range(m+3)]
    Game.obstacle = [[5 for x in range(n+3)] for x in range(m+3)]
    Game.wincheck = [False]
    Game.n = n
    Game.m = m
  @staticmethod
  def bordering():
    Game.wincheck[0] = False
    Game.mappingObstacle()
    for i in range(len(Game.map)):
      for j in range(len(Game.map)):
        if Game.map[i][j]!=1 and Game.map[i][j]!=7 and Game.map[i][j]!=8: Game.map[i][j]=5
        if Game.map[i][j]==5 and i>1 and i < len(Game.map)-2 and j>1 and j < len(Game.map)-2: Game.map[i][j]=0
        
  @staticmethod
  def detrailing():
    
    for i in range(len(Game.map)):
      for j in range(len(Game.map)):
        if Game.map[i][j]!=1 and Game.map[i][j]!=8: Game.map[i][j]=5
        if Game.map[i][j]==5 and i>1 and i < len(Game.map)-2 and j>1 and j < len(Game.map)-2: Game.map[i][j]=0

  @staticmethod
  def verticalObstacle(start,end, wPos):
    for i in range(end -start):
      Game.map[start+i][wPos] = 5

  @staticmethod
  def HorizontalObstacle(start,end, hPos):
    for i in range(end -start):
      Game.map[hPos][start+i] = 5

  @staticmethod
  def recObstacle(isVertical, start, end, pos, iterate ):
    if isVertical:
      for i in range(iterate):
        Game.verticalObstacle(start,end,pos+i)
    else:
      for i in range(iterate):
        Game.HorizontalObstacle(start,end,pos+i)

  @staticmethod
  def mappingObstacle():
    for i in range(len(Game.map)):
      for j in range(len(Game.map)):
        if Game.map[i][j] == 5: Game.map[i][j] = 5

  @staticmethod
  def trailing(curr):
    if Game.curr[0]== Game.curr[2] and Game.curr[1] == Game.curr[3]:
      Game.map[curr[0]][curr[1]]=9
    else:
      Game.map[curr[0]][curr[1]]=7
      Game.map[curr[2]][curr[3]]=7

    if Game.goal==curr[0:2]:
      Game.map[Game.goal[0]][Game.goal[1]]=1
    if Game.goal==curr[2:4]:
      Game.map[Game.goal[0]][Game.goal[1]]=1
      if Game.curr[0]== Game.curr[2] and Game.curr[1] == Game.curr[3]:
        Game.map[Game.goal[0]][Game.goal[1]]=3

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
        if Game.map[i][j]==9: res += colored("██",'yellow')
        if Game.map[i][j]==2 or Game.map[i][j]==7: res+= colored("██",'magenta')
        if Game.map[i][j]==3: res+= colored("██",'red','on_yellow')

      res += " |"
    print(res)
    return res
  @staticmethod
  def makemove( move):

    # Game.erase()
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
# for player play the game only
    # for i in Game.curr:
    #   if i>1 and i <=Game.n: continue
    #   else:
        
    #     Game.wincheck[0]= True
    #     Game.loadcurr()
    #     clear()
    #     Game.laprint()
    #     print(Game.curr)
    #     print("you lose kek")
    #     return
    # Game.loadcurr()
    # clear()
    # Game.laprint()

    # if Game.curr[0:2] == Game.curr[2:4] and Game.curr[0:2]==Game.goal:
    #   print("Ok u win, press r to play again")
    #   Game.wincheck[0]=True

    # print(Game.curr)
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
  def __init__(self, depth, curr, parrent, string) -> None:
    self.parrent = parrent
    self.win = False
    Node.count+=1
    self.lost = False
    self.idx = Node.count
    Node.count +=1
    self.depth: int = depth
    self.next: list = []
    self.curr: list = curr
    self.heuritiscal = self.heuritiscalCal(Game.goal)
    self.string = string
  def antiDetour(self,curr)->bool:
    if self.parrent is None: return True
    if self.parrent.curr == curr: return False
    return self.parrent.antiDetour(curr)

  def heuritiscalCal(self,goal)->int:
    heuritiscal = 0
    if Game.map[self.curr[0]][self.curr[1]] == 5 or Game.map[self.curr[2]][self.curr[3]] == 5 or Game.map[self.curr[0]][self.curr[1]] == 8 or Game.map[self.curr[2]][self.curr[3]] == 8: return sys.maxsize
    for i in range(4):
      heuritiscal += abs(self.curr[i]-goal[i%2])
    return heuritiscal

  def __str__(self) -> str:
    Game.curr = self.curr
    Game.loadcurr()
    _res=""
    tree = ""
    # for i in range(self.depth):
    #   _res+="---"
    #   tree +="   "
    res=_res + "depth: "+  str(self.depth) +", id: " + str(self.idx) + ", p_id: " + str(self.parrent.idx if self.parrent is not None else "root") + '\n' 
    res+= _res + "curr: "+ str(self.curr) + ", goal: " + str(Game.goal) + ", heuritiscal: " + str(self.heuritiscal) + '\n'
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
    res += "\n" + self.string
    if self.lost:
       res += "\n----------LOST"

    if self.win: res += "\n----------WIN*******"
    print(res)
    # if self.lost:
    #   time.sleep(.5)
    Game.erase()
    return res

  def proceed(self):
    # self.trailing()
    
    time.sleep(Node.speed)
    # clear()
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
      a = Node(self.depth+1,curr,self,self.string + "a")
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
      a = Node(self.depth+1,curr,self,self.string + "d")
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
      a = Node(self.depth+1,curr,self,self.string + "w")
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
      a = Node(self.depth+1,curr,self,self.string + "s")
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

  def greedy(self):
    res =""
    if Node.stop: return
    
    self.proceed()
    if self.lost: return
    ar = []
    idx = []
    for i in self.next:
      if Node.stop: return
      if i.heuritiscal < sys.maxsize: ar += [i.heuritiscal]
      idx += [i.heuritiscal]
    ar.sort()
    for i in ar:
      self.next[idx.index(i)].greedy()
      if Node.stop:
        return
      time.sleep(1)
      print("*-----------STUCK-----------*")
      idx.remove(i)


# //geneticalgorithm
def heuritiscalCal()->int:
  heuritiscal = 0
  for i in Game.curr:
    if i <0 or i > len(Game.map)-1: return sys.maxsize
  if Game.map[Game.curr[0]][Game.curr[1]] == 5 or Game.map[Game.curr[2]][Game.curr[3]] == 5 or Game.map[Game.curr[0]][Game.curr[1]] == 8 or Game.map[Game.curr[2]][Game.curr[3]] == 8: return sys.maxsize
  for i in range(4):
    heuritiscal += abs(Game.curr[i]-Game.goal[i%2])
  return heuritiscal

class Individual:
  genetic = ["w","s","a","d"]
  estimateStepIThink = 23
  maxPop = 50
  generation = 0
  matingParrentThreshold = 50
  eliteThreshold = 10
  def __init__(self, chromosome ) -> None:
    self.chromosome = chromosome
    map = copy.deepcopy(Game.map)
    cal = Individual.fitCal(chromosome)
    self.fitness = cal[0]
    self.bestMove = cal[1]
    self.map = cal[2]
    Game.map = map

  def iPrint(self):
    print("best chromosome: "+ self.chromosome[0:1+self.bestMove], " fitness: " + str(self.fitness) + " Generation: " + str(Individual.generation))
    map = copy.deepcopy(Game.map)
    Game.map = self.map
    Game.laprint()
    Game.map = map
  @staticmethod
  def createMutation():
    return random.choice(Individual.genetic)

  @staticmethod  
  def createChromosome():
    res = ""
    for i in range((Individual.estimateStepIThink)):
      res += Individual.createMutation()
    return res

  def __lt__(self,other):
    return self.fitness < other.fitness

  def __gt__(self,other):
    return self.fitness > other.fitness

  def mate(par1, par2):
    res = ""
    for i in range(len(par1.chromosome)):
      x = random.random()
      if x < .45: res+= par1.chromosome[i]
      elif x > .45 and x <.9: res+= par2.chromosome[i]
      elif x > .9: res+= Individual.createMutation()
      
    return res
  
  
  @staticmethod
  def fitCal(chromosome):
    Game.curr = copy.deepcopy(Game.startCurr)
    bestFitness = sys.maxsize
    bestMove = 0
    Game.trailing(Game.curr)
    for i in range(len(chromosome)):
      
      Game.makemove(chromosome[i])
      x = heuritiscalCal()
      Game.trailing(Game.curr)
      
      if x >= sys.maxsize: return (bestFitness, bestMove, Game.map)
      if x < bestFitness:
        bestFitness = x
        bestMove = i
      if bestFitness == 0: return (bestFitness, bestMove, Game.map)
    return (bestFitness, bestMove, Game.map)

def geneticAlgorithm(pop: list):
  pop.sort()
  pop[0].iPrint()
  while(pop[0].fitness != 0):
    time.sleep(Node.speed)
    random.seed()
    newPop = []
    for i in range(len(pop)):
      # elite
      if i < Individual.eliteThreshold*len(pop)/100:
        newPop += [pop[i]]
      # mating season :D
      else:
        par1 = pop[random.randint(0,len(pop)/(100/Individual.matingParrentThreshold))]
        par2 = pop[random.randint(0,len(pop)/(100/Individual.matingParrentThreshold))]
        child = Individual(Individual.mate(par1,par2))
        newPop += [child]
    pop = newPop
    pop.sort()
    Individual.generation += 1
    pop[0].iPrint()
 

def initPopulation(population):
  for i in range(Individual.maxPop):
    a = Individual(Individual.createChromosome())
    population += [a]

def main():
  # this for dfs only
  # game =  Game(9,9)

  # game.play()
  # print("awsd to move e to end, r to reset, dont kill urself, thx")
  
  


  # this for dfs only
  # Game.goal = [7,7]



  game =  Game(24,24)
  game.initgame()
  Game.map[Game.goal[0]][Game.goal[1]]=0
  Game.map[Game.curr[0]][Game.curr[1]]=0
  Game.map[Game.curr[2]][Game.curr[3]]=0

  # test case 1
  # Game.curr = [3,4,3,4]
  # Game.startCurr = copy.deepcopy(Game.curr)
  # Game.goal = [21,21]
  # Game.map[Game.goal[0]][Game.goal[1]]=1

  # Game.recObstacle(False,8,25,2,5)
  # Game.recObstacle(True,13,25,2,8)
  # Game.recObstacle(True,13,25,10,5)
  # Game.recObstacle(True,16,25,15,3)

# test case 2
  Game.curr = [3,4,3,4]
  Game.startCurr = copy.deepcopy(Game.curr)
  Game.goal = [21,21]
  Game.map[Game.goal[0]][Game.goal[1]]=1
  Game.HorizontalObstacle(8,25,2)
  Game.recObstacle(False,8,18,4,6)
  Game.recObstacle(False,2,18,7,18)

# test case 3 cannot be solved by genetic
  # Game.curr = [3,4,3,4]
  # Game.startCurr = copy.deepcopy(Game.curr)
  # Game.goal = [3,21]
  # Game.map[Game.goal[0]][Game.goal[1]]=1

  # Game.recObstacle(False,8,18,2,19)
  # Game.recObstacle(False,8,18,22,3)




  Node.speed = .0
  # root.greedy()

  #genetic Algorithm
  Individual.estimateStepIThink = 50
  Individual.maxPop = 20
  population = []
  initPopulation(population)
  print(len(population))
  geneticAlgorithm(population)

  # dfs
  # Node.speed = 0.0
  # root = Node(0,Game.curr, None,"")
  # print(root)
  # root.dfs(6)






if __name__ == '__main__':
    main()