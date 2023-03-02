#==============================================================================
#
# Class : CS 6420
#
# Author : Tyler Martin
#
# Project Name : Project 2 | Frequency Domain Filtering
# Date: 3/1/2023
#
# Description: This project implements a filter in the frequency domain
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
image = None
magnitude_spectrum = None
freq_filt_img = None
reset = False

#================================================================
#
# Function: key(event)
#
# Description: This function simply listens for key events and
#              either saves the image, resets the canvas, or 
#              quits the program based on which valid key is passed
#
#================================================================
def key(event):

    global magnitude_spectrum
    global filename
    global freq_filt_img
    global reset

    if event.key == 'r' and reset:
        plt.close('all')
        reset = False
    elif event.key == 'w' and reset:
        plt.imsave(filename + '.png', freq_filt_img, cmap = 'gray')
    elif event.key == 'q':
        sys.exit(0)

#================================================================
#
# Function: onclick(eclick, erelease)
#
# Description: This function listens for the drawing of the bounding
#              rect and then makes the mask and applies it to the 
#              image before performing idft and displaying the 
#              result.
#
#================================================================
def onclick(eclick, erelease):

    #globals
    global rect_selector
    global fequency_representation_shifted
    global fig
    global image
    global freq_filt_img
    global reset

    #make copy of frequency
    row, column = image.shape
    fequency_representation_shifted_copy = np.copy(fequency_representation_shifted)
    fequency_representation_shifted_mask = np.ones((row, column, 2), np.uint8)

    #draw the cutout
    fequency_representation_shifted_mask[int(rect_selector.extents[2]):int(rect_selector.extents[3]), int(rect_selector.extents[0]):int(rect_selector.extents[1])] = 0

    #get reverse coords 
    rect_selector_mirror = np.asarray(rect_selector.extents)
    rect_selector_mirror[0] = fequency_representation_shifted_mask.shape[1] - rect_selector_mirror[0]
    rect_selector_mirror[1] = fequency_representation_shifted_mask.shape[1] - rect_selector_mirror[1]
    rect_selector_mirror[2] = fequency_representation_shifted_mask.shape[0] - rect_selector_mirror[2]
    rect_selector_mirror[3] = fequency_representation_shifted_mask.shape[0] - rect_selector_mirror[3]

    fequency_representation_shifted_mask[int(rect_selector_mirror[3]):int(rect_selector_mirror[2]), int(rect_selector_mirror[1]):int(rect_selector_mirror[0])] = 0

    #reverse the fft
    fequency_representation_shifted_copy = fequency_representation_shifted_copy * fequency_representation_shifted_mask
    freq_filt_img = np.fft.ifftshift(np.float32(fequency_representation_shifted_copy))
    freq_filt_img = cv2.idft(freq_filt_img)
    freq_filt_img = cv2.magnitude(freq_filt_img[:,:,0], freq_filt_img[:,:,1])

    #show the new image
    reset = True
    plt.title('Altered Image\n[press \'w\' to save the image, \'r\' to reset the board, or \'q to quit\']'), plt.xticks([]), plt.yticks([])
    plt.imshow(freq_filt_img, cmap = 'gray')


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
    global image
    global magnitude_spectrum

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
    fequency_representation = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    fequency_representation_shifted = np.fft.fftshift(fequency_representation)
    magnitude_spectrum = 20*np.log(cv2.magnitude(fequency_representation_shifted[:,:,0], fequency_representation_shifted[:,:,1]))

    #keep windows reseeting upon request
    while (1):
        
        #better use of matplotlib to show images
        plt.subplots(1, 1, figsize=(10,7))
        plt.imshow(image, cmap = 'gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])

        fig, ax = plt.subplots(1, 1, figsize=(10,7))
        plt.imshow(magnitude_spectrum, cmap = 'gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        fig.canvas.mpl_connect('key_press_event', key)

        #set on draw listener
        rect_selector = RectangleSelector(ax, onclick, button=[1])

        #display
        plt.show()

#start main
argv = ""
__main__(sys.argv[1:])