import mnist
import numpy as np
from conv import Conv3x3
from maxpool import MaxPool2
from softmax import Softmax

"""
Heavily adapted from: https://victorzhou.com/blog/intro-to-cnns-part-1/
[CREDIT TO VICTOR ZHOU]
Simple Personal Project using a CNN to evaluate a number from images WITHOUT TRAINING/BACK PROP.
Showcases use of Convolutional Neural Network WITHOUT training as there is a ~10% accuracy regarding guessing
"""

test_images = mnist.train_images()[:1000]
test_labels = mnist.train_labels()[:1000]

conv = Conv3x3(8)
pool = MaxPool2()
softmax = Softmax(13 * 13 * 8, 10)


def forward(image, label):
    out = conv.forward((image / 255) - 0.5)
    out = pool.forward(out)
    out = softmax.forward(out)

    loss = -np.log(out[label])
    acc = 1 if np.argmax(out) == label else 0

    return out, loss, acc


print("MNIST CNN Initialized")

loss = 0
num_correct = 0
for i, (im, label) in enumerate(zip(test_images, test_labels)):
    _, l, acc = forward(im, label)
    loss += l
    num_correct += acc

    if i % 100 == 99:
        print(
            "[Step %d] Past 100 steps: Average Loss %.3f | Accuracy %d%%"
            % (i + 1, loss / 100, num_correct)
        )
        loss = 0
        num_correct = 0
