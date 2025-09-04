import tensorflow as tf
from keras import Input
import keras.layers as layers

def UNet(input_shape):
    inputs = Input(shape=input_shape)
    
    x = inputs

    filters = [64, 128, 256]
    ec_images = []

    for filter in filters:
        ec_images.append(x)
        x = layers.Conv2D(filters=filter, 
                          kernel_size=(3, 3),  
                          padding='same',
                          activation='relu'
                         )(x)
        x = layers.Conv2D(filters=filter, 
                          kernel_size=(3, 3),  
                          padding='same',
                          activation='relu'
                         )(x)
        x = layers.MaxPooling2D()(x)
        x = layers.BatchNormalization()(x)

    for filter, ec_image in zip(filters[:-1][::-1], ec_images[::-1][:-1]):
        # x = layers.Conv2DTranspose(filter, 3, 2, padding='same')(x)
        x = layers.Conv2DTranspose(filter, 3, 2, padding='same')(x)
        
        x = layers.concatenate([x, ec_image])
        x = layers.Conv2D(filters=filter, 
                         kernel_size=(3, 3),  
                         padding='same',
                         activation='relu'
                         )(x)
        x = layers.Conv2D(filters=filter, 
                         kernel_size=(3, 3),  
                         padding='same',
                         activation='relu'
                         )(x)
        x = layers.BatchNormalization()(x)

    x = layers.Conv2DTranspose(filter, 3, 2, padding='same')(x)
    x = layers.concatenate([x, ec_images[0]])
    x = layers.Conv2D(filters=filter, 
                         kernel_size=(3, 3),  
                         padding='same',
                         activation='relu'
                         )(x)
    outputs = layers.Conv2D(filters=1,
                      kernel_size=(3,3),
                      padding='same',
                      activation='linear'
                     )(x)

    unet_model = tf.keras.Model(inputs, outputs, name='U-net')
    unet_model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return unet_model



def test_loss(X_test, y_test, model, print_loss=True):
    # Prepare test dataset
    test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test))
    test_dataset = test_dataset.batch(4)

    # Evaluate the model on the test dataset
    test_mse, test_mae = model.evaluate(test_dataset)
    if print_loss:
        print(f"Test MSE: {test_mse}")
        print(f"Test MAE: {test_mae}")
    return test_mse, test_mae

    