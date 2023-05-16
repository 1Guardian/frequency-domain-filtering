# Frequency Domain Filtering
This project implements a method to convert an image into frequency domain and then applies a filter to remove specific frequencies depending on where the user selects in the frequency representation of the original image.

## Notes
This project uses matplotlib to render the images instead of the standard opencv or tkinter libraries that I usually employ. Because of this, matplotlib will also be needed to use this project.

## Usage:
User Interface for frequency selection and filtering:
<pre>
freq_filter [-h] -t input_image -s [output_image]
            -t : Target Image (t)
            -s : Output Image (s)
            </pre>
