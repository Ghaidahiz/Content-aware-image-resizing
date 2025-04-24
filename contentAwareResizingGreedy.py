
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



opPath = []
counter=0

def main():
     image_path = input("Enter the file path of the desired photo please: ")
     image = cv.imread(image_path)

     #desired_width =input(f"Your width is {image.shape[1]}, please enter your desired width: ")

     energyMap = compute_energyMap(image)
     array_to_grayimage(energyMap) # extra just to view the image , you will find the image as a file called EnargyMapImage.png
     print(energyMap)
     print(" EnargyMapImage.png Has been uploaded successfuly !")

     seams = int(input("Enter the the number of seams you want to remove please: "))
     resizedImg = remove_seam(image,energyMap, seams)
     cv.imwrite('ResizedImage.png',resizedImg)
     print(" ResizedImage.png Has been uploaded successfuly !")


     #End of Main ::::::::::::::::::::::::::





def findBestSeam(grid):
    #GREEDY ALGO
     print("~~~~~~~~~~~~~~~~~~~\nthe optimal path is:",opPath , "\nit's cost is: " , minCost)

     #End of part 2 ::::::::::::::::::::::::::






def remove_seam(image, energyArr, seams):
    new_image = np.copy(image)  #Keep a copy of the original image
    newArr = np.copy(energyArr) #Keep a copy of the energy map 

    global width

    for i in range(seams):  #A loop for number of seams wanted to be deleted
        findBestSeam(newArr)  # To calculate the best path after each delete
       
       #TO make a new map for the image after deleting a seam
        map_x = np.zeros((new_image.shape[0], width - 1), dtype=np.float32)
        map_y = np.zeros((new_image.shape[0], width - 1), dtype=np.float32)

        for row in range(new_image.shape[0]):
            col = opPath[row]  #the position of the pixel in the row
            map_x[row, :col] = np.arange(col)
            map_x[row, col:] = np.arange(col + 1, width)
            map_y[row, :] = row  

        #To remake the image without the deleted seam using the previus maps we made 
        new_image = cv.remap(new_image, map_x, map_y, interpolation = cv.INTER_LINEAR)

       
        width -= 1  #To update the width after deleting a seam

        # To recalculate the energyArr from the new image
        newArr = compute_energyMap(new_image)

        print(f"After removing seam {i+1}")

    return new_image

#End of part 3 ::::::::::::::::::::::::::

if __name__ == "__main__":
    main()
