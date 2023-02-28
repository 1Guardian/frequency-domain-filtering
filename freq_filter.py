#==============================================================================
#
# Class : CS 6420
#
# Author : Tyler Martin
#
# Project Name : Project 1 | Porter Duff Operators
# Date: 2/15/2023
#
# Description: This project implements the Porter-Duff operators
#
# Notes: Since I know you prefer to read and work in C++, this file is set
#        up to mimic a standard C/C++ flow style, including a __main__()
#        declaration for ease of viewing. Also, while semi-colons are not 
#        required in python, they can be placed at the end of lines anyway, 
#        usually to denote a specific thing. In my case, they denote globals, 
#        and global access, just to once again make it easier to parse my code
#        and see what it is doing and accessing.
#
#==============================================================================

#"header" file imports
from imports import *
from checkImages import *
from averagePixels import *
from intensitySampling import *
from getMetaData import *
from pixelDeletion import *
from pixelDuplication import *
from saveJson import *
from grayScaleImage import *
from saveImage import *
from operators import *

#================================================================
#
# NOTES: THE OUTPATH WILL HAVE THE LAST / REMOVED IF IT EXISTS
#        THE imageType WILL HAVE A . APPLIED TO THE FRONT AFTER
#        CHECKING VALIDITY
#
#================================================================

rect_selector = None
fequency_representation_shifted = None
fig = None
filename = None

def onclick(eclick, erelease):

    #globals
    global rect_selector
    global fequency_representation_shifted
    global fig
    global filename

    #make copy of frequency
    fequency_representation_shifted_copy = np.copy(fequency_representation_shifted)

    #draw the circles
    for i in range(int(rect_selector.extents[2]), int(rect_selector.extents[3])):
        for j in range(int(rect_selector.extents[0]), int(rect_selector.extents[1])):
                fequency_representation_shifted_copy[i][j] = 1

    #get reverse coords 
    rect_selector_mirror = np.asarray(rect_selector.extents)
    rect_selector_mirror[0] = fequency_representation_shifted_copy.shape[1] - rect_selector_mirror[0]
    rect_selector_mirror[1] = fequency_representation_shifted_copy.shape[1] - rect_selector_mirror[1]
    rect_selector_mirror[2] = fequency_representation_shifted_copy.shape[0] - rect_selector_mirror[2]
    rect_selector_mirror[3] = fequency_representation_shifted_copy.shape[0] - rect_selector_mirror[3]

    for i in range(int(rect_selector_mirror[3]), int(rect_selector_mirror[2])):
        for j in range(int(rect_selector_mirror[1]), int(rect_selector_mirror[0])):
                fequency_representation_shifted_copy[i][j] = 1

    #reverse the fft
    freq_filt_img = np.fft.ifft2(np.fft.ifftshift(fequency_representation_shifted_copy))
    freq_filt_img = np.abs(freq_filt_img)
    freq_filt_img = freq_filt_img.astype(np.uint8)
    magnitude_spectrum = 20*np.log(np.abs(fequency_representation_shifted_copy))

    #show the new image
    #plt.title('Altered Image'), plt.xticks([]), plt.yticks([])
    #plt.imshow(freq_filt_img, cmap = 'gray')

    #save image
    cv2.imwrite(filename + '.png', np.array(freq_filt_img))

#================================================================
#
# Function: __main__
#
# Description: This function is the python equivalent to a main
#              function in C/C++ (added just for ease of your
#              reading, it has no practical purpose)
#
#================================================================

def __main__(argv):

    #globals
    global rect_selector
    global fequency_representation_shifted
    global fig
    global filename

    #variables that contain the command line switch
    #information
    inPath = "nothing"
    depth = 1
    mode = 1
    intensity = 1
    primary = "nothing"
    filename = "outImage"
    direction = 0

    # get arguments and parse
    try:
      opts, args = getopt.getopt(argv,"h:t:s:")

    except getopt.GetoptError:
            print("freq_filter [-h] -t input_image -s [output_image]")
            print("===========================================================================================================")
            print("-t : Target Image (t)")
            print("-s : Output Image (s)")
            sys.exit(2)
    for opt, arg in opts:

        if opt == ("-h"):
            print("freq_filter [-h] -t input_image -s [output_image]")
            print("===========================================================================================================")
            print("-t : Target Image (t)")
            print("-s : Output Image (s)")
            

        elif opt == ("-m"):
            if (int(arg) < 10 and int(arg) > 0):
                mode = int(arg)
            else:
                print("Invalid Mode Supplied. Only Values 1 through 9 Are Accepted.")

        elif opt == ("-t"):
            primary = arg
        elif opt == ("-s"):
            filename = arg

    #demand images if we are not supplied any
    if (primary == "nothing"):
        print("freq_filter [-h] -t input_image -s [output_image]")
        print("===========================================================================================================")
        print("-t : Target Image (t)")
        print("-s : Output Image (s)")
        sys.exit(2)

    #open the image
    image = grayScaleImage(checkImages(primary))

    #convert to frequency spectrum
    fequency_representation = np.fft.fft2(image)
    fequency_representation_shifted = np.fft.fftshift(fequency_representation)
    magnitude_spectrum = 20*np.log(np.abs(fequency_representation_shifted))

    #better use of matplotlib to show images
    plt.subplots(1, 1, figsize=(10,7)),plt.imshow(image, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    fig, ax = plt.subplots(1, 1, figsize=(10,7))
    plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])

    #set on draw listener
    rect_selector = RectangleSelector(ax, onclick, button=[1])

    #display
    plt.show()

#start main
argv = ""
__main__(sys.argv[1:])