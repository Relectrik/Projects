# Valorant Role Predictor Project

A quick neural network I wanted to experiment with in Tensorflow! Essentially, it involves taking the various roles that agents can possess in Valorant (Sentinel, Controller, Initiator and Duelist), which all have their strengths and weaknesses which are tailored to do specific things in the game. It assigns these roles as labels to images that pertain to the agents' ability icons in the game. I wanted to train a convolutional Neural Network to predict the role of an agent given its ability icon.

I utilized the Valorant API, as seen in the download_images.py file along with pillow to resize and download the training data necessary (ability icons) for training. After sorting these manually into training and validation sets in their respective folders as seen in icons, I imported these image sets and utilized one of Tensorflow's example sequence of layers to try and predict an agent's role from its icon.

It ended up having around a 66.6% accuracy, but I realized that the model keeps predicting the validation set as an Initiator, so I will open an issue for me to solve this at some point. At first glance, I suspect this issue may be related to how the input data is currently being fed in. 

From a human's perspective, there does not seem to be a correlation between the agent's role and how the ability will look, so hopefully this convolutional neural network will learn something that I myself cannot see.  