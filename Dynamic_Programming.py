
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
def array_to_grayimage(energyMap):
    print("Type of energyMap:", type(energyMap))
    print("Shape of energyMap:", energyMap.shape)
    print(energyMap)
    energyMap = energyMap.astype(np.uint8)
    cv.imwrite('EnargyMapImage.png',energyMap)
    return
#End of part 1 ::::::::::::::::::::::::::


opPath = []
seams =0

def main():
     image_path = input("Enter the file path of the desired photo please: ")
     image = cv.imread(image_path)
     seams = int(input("Enter the the number of seams you want to remove please: "))
     choice = int(input("Enter 0 if you want to remove one seam a time, and enter x number if you want to remove them in x batches:"))
     if choice==0:
         energyMap = compute_energyMap(image)
         array_to_grayimage(energyMap) # extra just to view the image , you will find the image as a file called EnargyMapImage.png
         print(energyMap)
         print(" EnargyMapImage.png Has been uploaded successfuly !")

         cumulativeEnergyMap = getCumulativeEnergyMap(energyMap)
         resizedImg = remove_seam(image,cumulativeEnergyMap, seams)
     else:
         resizedImg = remove_seams_in_batches(image, seams, choice)
         
     cv.imwrite('ResizedImage.png',resizedImg)
     print(" ResizedImage.png Has been uploaded successfuly !")


     #End of Main ::::::::::::::::::::::::::

def getCumulativeEnergyMap(energyMap):
    height, width = energyMap.shape
    cumulativeEnergyMap = np.copy(energyMap).astype(float) # why flout ? to allow infinite value

    for i in range(1, height):
        for j in range(width):
            left = cumulativeEnergyMap[i-1, j-1] if j > 0 else np.inf
            up = cumulativeEnergyMap[i-1, j]
            right = cumulativeEnergyMap[i-1, j+1] if j < width - 1 else np.inf
            cumulativeEnergyMap[i, j] += min(left, up, right)
    return cumulativeEnergyMap

def findBestSeam(grid):
     #### calc From buttom row to top (backtrack)
    height, width = grid.shape
    opPath = [0] * height  # a new zero array to put the min pixel for each row  
    opPath[height - 1] = np.argmin(grid[height - 1]) #from the bottom we will look for the min energy pixel in that row and save it in the col number in opPath

    for row in range(height-2, -1,-1): #from bottom to top
            prev_col = opPath[row + 1]  # The column index is taken from the row below
            min_col = prev_col # Initialize the minimum as the pixel directly above

            if prev_col > 0: # Ensure we are not at the first column
                    if grid[row , prev_col-1] < grid[row , prev_col]: # compare the above left to the mid
                        min_col = prev_col-1

            if prev_col < width - 1:  # Ensure we're not at the last column
                    if grid[row , prev_col+1] < grid[row , min_col]: #compare the previous winner as the minimum with the above right pixel
                        min_col = prev_col+1

            opPath[row] = min_col # assighn the min cost winner at each row 

    return opPath


def find_k_seams(cumulativeEnergyMap, k):
    height, width = cumulativeEnergyMap.shape
    seams = []
    for _ in range(k):
        seam = [0] * height  
        j = np.argmin(cumulativeEnergyMap[-1])
        for i in reversed(range(height)):
            seam[i] = j
            if i == 0:
                break           
            neighbors = []
            if j > 0 and cumulativeEnergyMap[i-1, j-1] != np.inf:
                neighbors.append((j - 1, cumulativeEnergyMap[i-1, j-1]))
            if cumulativeEnergyMap[i-1, j] != np.inf:
                neighbors.append((j, cumulativeEnergyMap[i-1, j]))
            if j < width - 1 and cumulativeEnergyMap[i-1, j + 1] != np.inf:
                neighbors.append((j + 1, cumulativeEnergyMap[i-1, j + 1]))
            if not neighbors:
                break
            j = min(neighbors, key=lambda x: x[1])[0]
        seams.append(seam)
        for i, j in enumerate(seam):
            cumulativeEnergyMap[i, j] = np.inf
    return seams

#End of part 2 ::::::::::::::::::::::::::

def remove_seams_in_batches(image, total_seams, batch_size=5):
    for _ in range(0, total_seams, batch_size):
        seams_to_remove = min(batch_size, total_seams)  # for last iteration
        energyMap = compute_energyMap(image)
        array_to_grayimage(energyMap) # extra just to view the image , you will find the image as a file called EnargyMapImage.png
        print(energyMap)
        print(" EnargyMapImage.png Has been uploaded successfuly !")

        cumulativeEnergy = getCumulativeEnergyMap(energyMap)
        seams = find_k_seams(cumulativeEnergy, seams_to_remove)
        image = remove_seams(image, seams)
        global width
        width -= seams_to_remove
        total_seams -= seams_to_remove
        print(f"Removed {seams_to_remove} seams, remaining: {total_seams}")
    return image

def remove_seams(image, seams):
    h, w, _ = image.shape
    new_image = []
    # For each row, remove the seam column(s)
    for row in range(h):
        cols_to_remove = sorted(seam[row] for seam in seams)
        row_pixels = list(image[row])
        for offset, col in enumerate(cols_to_remove):
            row_pixels.pop(col - offset)  # Adjust for previous pops
        new_image.append(row_pixels)
    return np.array(new_image, dtype=image.dtype)

def remove_seam(image, energyArr, seams):
    new_image = np.copy(image)  #Keep a copy of the original image
    newArr = np.copy(energyArr) #Keep a copy of the energy map 
    opPath = findBestSeam(newArr)

    global width

    for i in range(seams):  #A loop for number of seams wanted to be deleted
        opPath = findBestSeam(newArr)  # To calculate the best path after each delete
       
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
