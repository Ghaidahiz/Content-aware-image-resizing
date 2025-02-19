import numpy as np
import cv2
height = 4
width = 6
minCost = 10**10
opPath = []
example = np.array([[1, 2, 3,8,0,6], [4, 5, 6,5,7,8],[5,7,4,4,8,0],[1,9,90,5,8,0]])

def main():
     print(example)
     findBestSeam()

def findBestSeam():
     
     for i in range (width):
          findBestSeamRec(0,i,0,[])
     print("~~~~~~~~~~~~~~~~~~~\nthe optimal path is:",opPath , "\nit's cost is: " , minCost)

def findBestSeamRec(row,col,curCost,path):
     global minCost
     global opPath
     if col >= width or col  < 0: # if the path surpasses edges
          return # skip it
     if row >= height: # if a path is explored
          if curCost<minCost: # and it's the minimal path so far
               minCost = curCost
               opPath = path.copy()

     else: #if the path is still not done
          curCost = curCost + example[row,col] # add this pixel's cost to the current path cost
          path.append((row, col)) # add this pixel to the path
          # explore neighbors in the next row
          findBestSeamRec(row+1,col-1,curCost,path) 
          findBestSeamRec(row+1,col,curCost,path)
          findBestSeamRec(row+1,col+1,curCost,path)
          path.pop() #removes pixels when backtracing 
     
     
     
if __name__ == "__main__":
    main()
