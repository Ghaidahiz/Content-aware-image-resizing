#pip install opencv-python
#^write the above in the terminal to install cv package.

#numpy should be installed by defult. if not, just write pip install numpy

import cv2 as cv
import numpy as np

#Part 1: Compute the energy map :
sum_RBG = lambda p: 0 if (type(p) is int) else int(int(p[0])+int(p[1])+int(p[2]))
energy = lambda x1,x2,x3,x4,x5,x6:int(sum_RBG(x1) + 2*sum_RBG(x2) + sum_RBG(x3) -sum_RBG(x4) -2*sum_RBG(x5) - sum_RBG(x6))
compute_energy = lambda A,B,C,D,F,G,H,I: int(abs((energy(A,D,G,C,F,I)+energy(A,B,C,G,H,I))**0.5)) #the parameters have default value of 0 
#you may wonder what is lambda, lambda is simplified way to write a method

def compute_energyMap(image): 
    energyMap = np.zeros((image.shape[0],image.shape[1]),dtype=int) 
    global height, width
    height, width = image.shape[:2]
    
    for x in range(height): 
        for y in range(width): 
            #the following if-else statements are being used to handle the image's edges cases
            if x==0 and y==0:
                energyMap[x,y] = compute_energy(0,0,0,0,image[x][y+1],0,image[x+1][y],image[x+1][y+1])
            elif x == 0 and y == width-1 :
                energyMap[x,y] = compute_energy(0,0,0,image[x,y-1],0,image[x+1,y-1],image[x+1,y],0)
            elif x == height-1 and y == 0 : 
                energyMap[x,y] = compute_energy(0,image[x-1][y],image[x-1][y+1],0,image[x][y+1],0,0,0)
            elif x == height-1 and y == width-1 :
                energyMap[x,y] = compute_energy(image[x-1][y-1],image[x-1][y],0,image[x][y-1],0,0,0,0)
            elif x ==0:
                energyMap[x,y] = compute_energy(0,0,0,image[x][y-1],image[x,y+1],image[x+1,y-1],image[x+1,y],image[x+1,y+1])
            elif x == height-1:
                energyMap[x,y] = compute_energy(image[x-1][y-1],image[x-1][y],image[x-1][y+1],image[x][y-1],image[x][y+1],0,0,0)
            elif y == width-1:
                energyMap[x,y] = compute_energy(A=image[x-1][y-1],B=image[x-1][y],C=0,D=image[x][y-1],F=0,G=image[x+1][y-1],H=image[x+1][y],I=0)
            elif y == 0:
                energyMap[x,y] = compute_energy(0,image[x-1][y],image[x-1][y+1],0,F=image[x][y+1],G=0,H=image[x+1][y],I=image[x+1][y+1])
            else:
                energyMap[x,y] = compute_energy(A=image[x-1][y-1],B=image[x-1][y],C=image[x-1][y+1],D=image[x][y-1],F=image[x][y+1],G=image[x+1][y-1],H=image[x+1][y],I=image[x+1][y+1])
    return energyMap

#EXTRA method to transform the energymap array to image (why? just to check the correctness of the energymap)
def array_to_grayimage(energyMap):
    print("Type of energyMap:", type(energyMap))
    print("Shape of energyMap:", energyMap.shape)
    print(energyMap)
    energyMap = energyMap.astype(np.uint8)
    cv.imwrite('EnargyMapImage.png',energyMap)
    return
#End of part 1 ::::::::::::::::::::::::::


#height = 0
#width = 0
minCost = 10**10
opPath = []
counter=0

#global example
#example = np.array([[ 1 , 2 , 3 , 8 , 6],[ 4 , 5 , 6 , 5 , 8],[ 5 , 7  ,4 , 4 , 8],[ 1,  9 ,90  ,5  ,8]])

def main():
     #print(example)
     #findBestSeam()
     image_path = input("Enter the file path of the desired photo please: ")
     image = cv.imread(image_path)
     #desired_width =input(f"Your width is {image.shape[1]}, please enter your desired width: ")
     energyMap = compute_energyMap(image)
     print(energyMap)
     seams = int(input("Enter the the number of seams you want to remove please: "))
     resizedArr = remove_seam(energyMap, seams)
     print("final array after seams deleting")
     cv.imwrite('resizedImage.png',resizedArr)

     
     array_to_grayimage(energyMap) # extra just to view the image , you will find the image as a file called EnargyMapImage.png


def findBestSeam(grid):
     global minCost
     global opPath
     minCost = 10**10
     opPath = []
     for i in range (width):
          findBestSeamRec(grid,0,i,0,[])
     print("~~~~~~~~~~~~~~~~~~~\nthe optimal path is:",opPath , "\nit's cost is: " , minCost)
def findBestSeamRec(grid,row,col,curCost,path):
     global counter
     global minCost
     global opPath
     if col >= width or col  < 0: # if the path surpasses edges
          return # skip it
     if row >= height: # if a path is explored
          if curCost<minCost: # and it's the minimal path so far
               minCost = curCost
               opPath = path.copy()
               counter = counter+1
               print("current path is: ", counter)

     else: #if the path is still not done
          curCost = curCost + grid[row,col] # add this pixel's cost to the current path cost
          path.append(col) # add this pixel to the path  
          # explore neighbors in the next row
          findBestSeamRec(grid,row+1,col-1,curCost,path) 
          findBestSeamRec(grid,row+1,col,curCost,path)
          findBestSeamRec(grid,row+1,col+1,curCost,path)
          path.pop() #removes pixels when backtracing 
     

def remove_seam(energyArr , seams ): #Take the numpy array and the number of iteration wanted to remove seams
    newArr = np.copy(energyArr)
    for i in range(seams): #iterates through the wanted number of times
        findBestSeam(newArr) # calling the method to calculate optimal path
        newArr = np.array([np.delete(energyArr[i], opPath[i]) for i in range (energyArr.shape[0])]) #create a new numpy array that has to delete all 1D array (rows)  (its like deleting each element from a 1D array which is in a whole 2d Array)
        global width
        width = width-1
        compute_energyMap(newArr)
        print("after removing seams =", i+1) #hust for tracing the updates in each deletion
        #print(new_example) # same
    return newArr


if __name__ == "__main__":
    main()
