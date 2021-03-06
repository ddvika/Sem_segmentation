# -*- coding: utf-8 -*-
"""custom_segnet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gbE8758PJFTsQMmvcAFgwL-b4qdWlUq2
"""

import tensorflow.keras.backend as K
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.layers import *
from tensorflow.compat.v1.layers import conv2d_transpose

def convBnRelu(x, filters):
    
    x = Conv2D(filters, kernel_size = (2,2), padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation(activation='relu')(x)
    
    return x

def custom_segnet(input_shape=(256,256,1),nb_classes = 1, filters = 16 ):
    inputs = Input((input_shape))
    
    #Encoders
    x = convBnRelu(inputs, filters=filters*1)
    x = convBnRelu(x, filters=filters*1)
    x = MaxPooling2D(pool_size=(2,2))(x)
        
    x = convBnRelu(x, filters=filters*2)
    x = convBnRelu(x, filters=filters*2)
    x = MaxPooling2D(pool_size=(2,2))(x)
    
    
    x = convBnRelu(x, filters=filters*4)
    x = convBnRelu(x, filters=filters*4)
    x = convBnRelu(x, filters=filters*4)
    x = MaxPooling2D(pool_size=(2,2))(x)
    
    x = convBnRelu(x, filters=filters*8)
    x = convBnRelu(x, filters=filters*8)
    x = convBnRelu(x, filters=filters*8)
    x = MaxPooling2D(pool_size=(2,2))(x)
    
    #Decoder
    x = UpSampling2D(size=(2,2))(x)
    x = convBnRelu(x, filters=filters*8)
    x = convBnRelu(x, filters=filters*8)
    x = convBnRelu(x, filters=filters*8)
        
    x = UpSampling2D(size=(2,2))(x)
    x = convBnRelu(x, filters=filters*4)
    x = convBnRelu(x, filters=filters*4)
    x = convBnRelu(x, filters=filters*4)
    
    x = UpSampling2D(size=(2,2))(x)
    x = convBnRelu(x, filters=filters*2)
    x = convBnRelu(x, filters=filters*2)
    
    x = UpSampling2D(size=(2,2))(x)
    x = convBnRelu(x, filters=filters*1)
    x = convBnRelu(x, filters=filters*1)
    
    x = Conv2D(nb_classes, (1,1), activation='sigmoid', padding='same', name='output')(x)

    model = Model(inputs=inputs, outputs=x)

    return model

