from imports import *

#================================================================
#
# Function: pixelDeletion(image, depth)
#
# Description: This function scales the input image down
#              by removing the odd rows and columns from the
#              image. It repeats this as many times as the input
#              variable 'depth' specifies it should.
#
# Returns: resizedImg | type: openCV image 
#    OR
# Returns: image | original image unchanged
#
#================================================================
def pixelDeletion(image, depth):

    #loop over this method as many times as necessary to reach
    #the desired depth
    resizedImg = image

    #check that depth supplied is not 0 (no alteration)
    if depth != 0:

        #execute as many times as needed
        for i in range(depth):

            #removing the rows from the image via numpy
            resizedImg = np.delete(resizedImg, range(1, resizedImg.shape[0], 2), axis=0)

            #removing the columns from the image via numpy
            resizedImg = np.delete(resizedImg, range(1, resizedImg.shape[1], 2), axis=1)

        #return manipulated image
        return resizedImg

    #else, image fit, exit
    else:
        return image