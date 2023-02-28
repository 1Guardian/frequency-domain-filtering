from imports import *

#================================================================
#
# Function: intensitySampling(image, intensity)
#
# Description: This function down or upsamples the image intensity
#              resolution based on the passed 'intensity' value
#
# Returns: resizedImg | type: openCV image 
#    OR
# Returns: image | original image unchanged
#
#================================================================
def intensitySampling(image, intensity):

    #loop over this method as many times as necessary to reach
    #the desired depth
    workingImg = image

    #check that depth supplied is not 0 (no alteration)
    if intensity != 0:

        #FIXME: CATCH ME
        workingImg = np.array(255*(image / 255) ** intensity, dtype = 'uint8')

        #return manipulated image
        return workingImg

    #else, image fit, exit
    else:
        return image