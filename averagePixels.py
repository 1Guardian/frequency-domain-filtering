from imports import *

#================================================================
#
# Function: averagePixels(image, depth)
#
# Description: This function scales the input image down
#              by averaging the pixels.
#
# Returns: resizedImg | type: openCV image 
#    OR
# Returns: image | original image unchanged
#
#================================================================
def averagePixels(image, depth):

    #loop over this method as many times as necessary to reach
    #the desired depth
    workingImg = image

    #check that depth supplied is not 0 (no alteration)
    if depth != 0:

        #execute as many times as needed
        for i in range(depth):

            #get image size each time
            rows, columns, pixel = workingImg.shape

            #image to hold the scaled down image
            downScaledImg = np.zeros(shape=(math.ceil(rows/4), math.ceil(columns/4), 3), dtype=np.uint8)

            #average the values of the pixels by a factor of 4 per depth
            for i in range(0, rows, 4):
                for j in range(0, columns, 4):
                    downScaledImg[math.ceil(i/4), math.ceil(j/4)] = np.mean(workingImg[i:i + 4, j:j+4], axis=(0,1))
            
            #update the old workingImg to newly scaled image
            workingImg = downScaledImg

        #return manipulated image
        return workingImg

    #else, image fit, exit
    else:
        return image