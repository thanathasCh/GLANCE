# GLANCE

This project is developed as a part of my senior project. It is computer vision service aims to help auditor perform product stock checking faster with AI.
The repository is not a standalone project, it requires front-end as well. However, the front-end part was developed by my friend, so it won't be included in this repository.


# Project Structure

This project consists of multiple components such as backend service, ai module and image processing module.

# How to install the project (Windows)

2. Make sure you add anaconda into your PATH by 
   - type ```Edit the System Environment variables``` in your window search bar
   - Click on ```Environment variables```
   - Click on ```Path```
   - Click on the new empty block and put the anaconda's file location. For example, use ```C:\Users\your_name\anaconda3\Scripts``` if you installed it in default location
   - Click Ok and lauch your cmd or terminal again
   - Type ```conda init``` it should show something if you installed it correctly
   - Close your cmd or terminal and open it again 
   - Type ```conda activate```
3. Use ```git clone``` to clone this project to your PC
4. Edit the last section in ```environment.yml``` called prefix to path to anaconda in your computer
4. Run ```conda env create -f environment.yml``` to create enviroment called 'glance-dev'
5. Wait for the install to finish (this may take a while)
6. After everything is finished, type ```python app.py``` to run the program


## Developing

This project has been sepearted into modules by their functionalities.

1. common - this is all common components used across project.
2. cv - all computer vision and ai will  be stored in this module, including ANNOY, YOLOv4 and ORB + FLANN detector. However, all models (details in models section) are not included in this project due to its size and my credential. But you can contact me for the model, if I see fit.
3. Utility - basic function used across project.
4. app.py - base program.


## Models

This project contains multiple models, their structure may be existed in this project, but their weights and biases are not. There are 3 models 
1. Product detection models - I used YOLOv4 from Darknet and SKU-110K dataset to train this model.
2. Product feature extraction model - I trained it based on ResNet50 architecture with Imagenet weights and biases along with my personal dataset to train with triplet loss function.
3. Product searching model - I used [ANNOY](https://github.com/spotify/annoy) to construct product searching model.
4. ORB detector and FLANN matcher - These models are open source from opencv. You can find out more in their [document](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html).