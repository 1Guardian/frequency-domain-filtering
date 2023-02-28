from imports import *

#================================================================
#
# Function: pixelDuplication(image, depth)
#
# Description: This function scales the input image up
#              by duplication the odd rows and columns from the
#              image. It repeats this as many times as the input
#              variable 'depth' specifies it should.
#
# Returns: combinedImg | type: openCV image 
#    OR
# Returns: image | original image unchanged
#
#================================================================
def pixelDuplication(image, depth):

    #loop over this method as many times as necessary to reach
    #the desired depth
    resizedImg = image
    combinedImg = resizedImg

    #check that depth supplied is not 0 (no alteration)
    if depth != 0:

        #execute as many times as needed
        for i in range(depth):

            #get size
            rows, columns, pixel = resizedImg.shape

            #build the new image by duplicating the rows
            #and columns, then recombining into a new image
            for i in range(columns):
                combinedImg = np.insert(combinedImg,[i*2],resizedImg[:,[i]],axis=1)

            for i in range(rows):
                combinedImg = np.insert(combinedImg,[i*2],combinedImg[i*2],axis=0)

        #return manipulated image
        return combinedImg

    #else, image fit, exit
    else:
        return image