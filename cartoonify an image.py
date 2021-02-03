import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path

import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image


#Making the main window
top=tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image !')
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)


def cartoonify(ImagePath):
    # read the image
    #Imread is a method in cv2 which is used to store images in the form of numbers.
    #This helps us to perform operations according to our needs. 
    #The image is read as a numpy array, in which cell values depict R, G, and B values of a pixel.
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    #print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

#We resize the image after each transformation to display all the images on a similar scale at last.
    ReSized1 = cv2.resize(originalmage, (960, 540))
    #plt.imshow(ReSized1, cmap='gray')


#cvtColor(image, flag) is a method in cv2 which is used to transform an image into the colour-space mentioned as ‘flag’.
#our first step is to convert the image into grayscale. 
#Thus, we use the BGR2GRAY flag. This returns the image in grayscale.
#A grayscale image is stored as grayScaleImage.

#After each transformation, we resize the resultant image using the resize() method in cv2 and display it using imshow() method.
#This is done to get more clear insights into every single transformation step.

    #converting an image to grayscale
    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))
    #plt.imshow(ReSized2, cmap='gray')


#To smoothen an image, we simply apply a blur effect. This is done using medianBlur() function. 
#Here, the center pixel is assigned a mean value of all the pixels which fall under the kernel. In turn, creating a blur effect.



    #applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    #plt.imshow(ReSized3, cmap='gray')

# Here, we will try to retrieve the edges and highlight them.
#This is attained by the adaptive thresholding technique.
#The threshold value is the mean of the neighborhood pixel values area minus the constant C.
#C is a constant that is subtracted from the mean or weighted sum of the neighborhood pixels.
#Thresh_binary is the type of threshold applied, and the remaining parameters determine the block size.



    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (960, 540))
    #plt.imshow(ReSized4, cmap='gray')

    #applying bilateral filter to remove noise 
    #and keep edge sharp as required
    
    #We prepare a lightened color image that we mask with edges at the end to produce a cartoon image.
    #We use bilateralFilter which removes the noise.
    #It can be taken as smoothening of an image to an extent.
    #The third parameter is the diameter of the pixel neighborhood, i.e, the number of pixels around a certain pixel which will determine its value.
    #The fourth and Fifth parameter defines signmaColor and sigmaSpace.
    #These parameters are used to give a sigma effect, i.e make an image look vicious and like water paint, removing the roughness in colors.
    
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)    #second parameter-block size
    ReSized5 = cv2.resize(colorImage, (960, 540))
    #plt.imshow(ReSized5, cmap='gray')


    #masking edged image with our "BEAUTIFY" image
    #We perform bitwise and on two images to mask them. Remember, images are just numbers?
    #So, let’s combine the two specialties. This will be done using MASKING.
    
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (960, 540))
    #plt.imshow(ReSized6, cmap='gray')

    # Plotting the whole transition
    
    #To plot all the images, we first make a list of all the images.
    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]


#Now, we create axes like subl=plots in a plot and display one-one images in each block on the axis using imshow() method.

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

#Making a Save button in the main window
    save1=Button(top,text="Save cartoon image",command=lambda: save(ReSized6, ImagePath),padx=30,pady=5)
    save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)
    
    #plt.show() plots the whole plot at once after we plot on each subplot.
    plt.show()
    
    
def save(ReSized6, ImagePath):
    #saving an image using imwrite()
    
    #Here, the idea is to save the resultant image. 
    #For this, we take the old path, and just change the tail (name of the old file) to a new name and store the cartoonified image with a new name in the same folder by appending the new name to the head part of the file.
    newName="cartoonified_Image"
    
    #For this, we extract the head part of the file path by os.path.dirname() method.
    path1 = os.path.dirname(ImagePath)
    
    #Similarly, os.path.splitext(ImagePath)[1] is used to extract the extension of the file from the path.
    extension=os.path.splitext(ImagePath)[1]
    
    #Here, newName stores “Cartoonified_Image” as the name of a new file.
    #os.path.join(path1, newName + extension) joins the head of path to the newname and extension. This forms the complete path for the new file.
    path = os.path.join(path1, newName+extension)
    
    #imwrite() method of cv2 is used to save the file at the path mentioned.
    #cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR) is used to assure that no color get extracted or highlighted while we save our image.
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    
    #Thus, at last, the user is given confirmation that the image is saved with the name and path of the file.
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)
    
#Making the Cartoonify button in the main window
upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)


#Main function to build the tkinter window
top.mainloop()



