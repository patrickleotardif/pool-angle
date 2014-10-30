from math import *
from random import *
import matplotlib.pyplot as plt

class poolTable:
  def __init__(self,x,y):
    longSide = float(max(x,y))
    shortSide = float(min(x,y))
    self.points = [
      [0,0],
      [shortSide,0],
      [0,longSide/2],
      [shortSide,longSide/2],
      [0,longSide],
      [shortSide,longSide]
    ]
    self.long = longSide
    self.short = shortSide

def angle(pocket,cue,ball):
  a = length(cue,ball)
  b = length(cue,pocket)
  c = length(ball,pocket)
  return degrees(acos(
      (pow(a,2) + pow(b,2) - pow(c,2))
      / (2*a*b)
  ))

def length(x,y):
  return sqrt(pow(x[0] - y[0],2) + pow(x[1] - y[1],2))

def bestAngle(table,cue,ball):
  solution = False
  for pocket in table.points:
    pocketAngle = angle(pocket,cue,ball)
    if not solution or pocketAngle < solution[1]:
      solution = (pocket, pocketAngle)
  return solution

def visualize(cue,ball,pocket,table,angle):
  tableX = map(lambda x: x[0], table.points)
  tableY = map(lambda x: x[1], table.points)

  plt.xlim([-table.long*0.1,table.long*1.1])
  plt.ylim([-table.long*0.1,table.long*1.1])

  plt.plot(tableX,tableY,'bo')
  plt.plot(pocket[0],pocket[1],'ro',ms=10)
  plt.plot(cue[0],cue[1],'wo',ms=12)
  plt.plot(ball[0],ball[1],'ko',ms=12)

  plt.plot([cue[0],ball[0]], [cue[1],ball[1]], 'k-')
  plt.plot([cue[0],pocket[0]], [cue[1],pocket[1]], 'r-')

  plt.text(cue[0],cue[1]-1,str(angle))
  plt.show()

def simulate(x,y,iterations): #insert functionality for fixed cue ball
  table = poolTable(x,y)
  solutions = []
  cueYvals = []
  for i in range(iterations):
    cue = [uniform(0,table.short),uniform(0,table.long)]
    ball = [uniform(0,table.short),uniform(0,table.long)]
    best = bestAngle(table,cue,ball)
    #print 'cue:%s ball:%s pocket:%s angle:%s' % (cue,ball,best[0],best[1])
    #visualize(cue,ball,best[0],table,best[1])
    solutions.append(best[1]) #modify to select angle
    cueYvals.append(cue[1])
  return (solutions, cueYvals)
