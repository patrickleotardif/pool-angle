from math import *
from random import *
#import matplotlib.pyplot as plt 
# ^ not needed for interactive IPython imports

#describe the pool table
class poolTable:
  def __init__(self,x,y):
    pocketSide = float(y) #for simplicity x and y are used 
    plainSide = float(x)
    self.points = [
      [0,0],
      [plainSide,0],
      [0,pocketSide/2],
      [plainSide,pocketSide/2],
      [0,pocketSide],
      [plainSide,pocketSide]
    ]
    self.x = float(x)
    self.y = float(y)
    self.long = float(max(x,y))

#angle given all other variables in degrees
def angle(pocket,cue,ball):
  a = length(cue,ball)
  b = length(ball,pocket)
  c = length(cue,pocket)

  return 180 - degrees(acos(
      (pow(a,2) + pow(b,2) - pow(c,2))
      / (2*a*b)
  ))

#length between two points
def length(x,y):
  return sqrt(pow(x[0] - y[0],2) + pow(x[1] - y[1],2))

#returns best angle choice between the pockets
def bestAngle(table,cue,ball):
  solution = False
  for pocket in table.points:
    pocketAngle = angle(pocket,cue,ball)
    if not solution or pocketAngle < solution[1]:
      solution = (table.points.index(pocket)+1, pocketAngle, pocket)
  return solution

#show a representative plot given all variables
def visualize(cue,ball,pocket,table,angle):
  tableX = map(lambda x: x[0], table.points)
  tableY = map(lambda x: x[1], table.points)

  plt.xlim([-table.long*0.1,table.long*1.1]) #in order to keep scaling consistent
  plt.ylim([-table.long*0.1,table.long*1.1])

  plt.plot(tableX,tableY,'bo')
  plt.plot(pocket[0],pocket[1],'ro',ms=10)
  plt.plot(cue[0],cue[1],'wo',ms=12)
  plt.plot(ball[0],ball[1],'ko',ms=12)

  plt.plot([cue[0],ball[0]], [cue[1],ball[1]], 'k-')
  plt.plot([ball[0],pocket[0]], [ball[1],pocket[1]], 'r-')

  plt.text(cue[0],cue[1]-1,str(angle))
  plt.show()

#iterate through many random simulations
def simulate(x,y,iterations,ballFix=False,cueFix=False,viz=False): 
  table = poolTable(x,y)
  solutions = []
  cueVals = []
  pockets = []
  ballVals = []
  for i in range(iterations):
    if not cueFix:
    	cue = [uniform(0,table.x),uniform(0,table.y)]
    else:
        cue = cueFix
    if not ballFix:
    	ball = [uniform(0,table.x),uniform(0,table.y)]
    else:
	ball = ballFix
    best = bestAngle(table,cue,ball)
    if viz:
    	visualize(cue,ball,best[2],table,best[1])
    solutions.append(best[1]) #modify to select angle
    cueVals.append((round(cue[0],1),round(cue[1],1)))
    ballVals.append((round(ball[0],1),round(ball[1],1)))
    pockets.append(best[0])
  return (solutions,pockets,cueVals,ballVals)
