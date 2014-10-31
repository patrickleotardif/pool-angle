from math import *
from random import *
import numpy
from itertools import *
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
 
 # print cue,ball,pocket 
 # print (pow(a,2) + pow(b,2) - pow(c,2))/ (2*a*b)
  if a == 0 or b == 0:
      return 0
  else:
      return 180 - degrees(acos(
    max(min(  (pow(a,2) + pow(b,2) - pow(c,2))
      / (2*a*b),
       0.999999999
       ), -0.999999999)
  ))

#length between two points
def length(x,y):
  return sqrt(pow(x[0] - y[0],2) + pow(x[1] - y[1],2))

#returns best angle choice between the pockets
def bestAngle(table,cue,ball):
  solution = False
  if list(ball) in table.points:
     return (table.points.index(list(ball))+1,0,list(ball))

  else:
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

#Given a constant cue position, draw an image showing which pocket is chosen
def pocketMapForFixedCue(x,y,cue):
    img = numpy.zeros(shape=(y*10,x*10))
    
    for a,b in product(range(y*10),range(x*10)):
       img[a][b] = simulate(x,y,1,(float(b)/10,float(a)/10),cue, False)[1][0]

    return img 

    
def heatMapForFixedCue(x,y,cue):
    img = numpy.zeros(shape=(y*10,x*10))
    
    for a,b in product(range(y*10),range(x*10)):
       img[a][b] = simulate(x,y,1,(float(b)/10,float(a)/10),cue, False)[0][0]

    return img 

def meanHeatMap(x,y):
    img = numpy.zeros(shape=(y*10,x*10))
    
    for a,b in product(range(y*10),range(x*10)):
       img[a][b] = numpy.mean(simulate(x,y,1000,False,(float(b)/10,float(a)/10), False)[0])

    return img 

def tableSizeMeanAndVariance():
    results = []
    for i in chain(numpy.arange(1,5,0.1),numpy.arange(5,25,0.5)):
        s = simulate(5,i,10000)[0]
        k = float(i)/5
        
        results.append( [k, (numpy.mean(s)  , numpy.var(s)  )] )        
    return results



    
    
