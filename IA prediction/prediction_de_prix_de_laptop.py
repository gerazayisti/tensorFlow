# -*- coding: utf-8 -*-
"""Prediction de prix de laptop.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_Yz1gIvnWXopX8DwBV_xwyjAJeLRl1-V
"""



"""importation des bibliothéques pour notre trvail de prediction de prix d'ordinateurs"""

import tensorflow as tf
import pandas as pd
import seaborn as sea
from tensorflow.keras.layers import Normalization, Dense, InputLayer
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError, MeanAbsoluteError, Huber
from tensorflow.keras.metrics import RootMeanSquaredError
import matplotlib.pyplot as plt
import numpy as np

"""**Preparation des données**

1- *assignation a une variables*
"""

donnee = pd.read_csv("laptop_data_cleaned.csv",",")
donnee.head()

"""verification de l'etendu des données (inspection des données)"""

donnee.shape

"""dans cette section on ne vas que utilisé les colonne ayant des valeurs etant des chiffres."""

entree = donnee[['Ram', 'Weight', 'Price', 'TouchScreen', 'Ips', 'Ppi','HDD', 'SSD']]
sea.pairplot(entree, diag_kind ='hist')

entree.head()

entree.shape

"""conversion de nos données en tenseur"""

tenseur_donnee = tf.constant(entree)
tenseur_donnee = tf.cast(tenseur_donnee, tf.float32)
print(tenseur_donnee)

"""À present veuillons mellez nos données"""

tenseur_donnee = tf.random.shuffle(tenseur_donnee)
X = tenseur_donnee[:,]
Y = tenseur_donnee[:,2]
Y = tf.expand_dims(Y, axis = -1)
print(X.shape, Y.shape)
print(X[:5], Y[:5])

"""*division des données (donnee entrainenement 80%, donee de validation 10%, donnee de test 10%)* ET ATTRIBUTION DE NOUVEAU JEUX DE DONNEE"""

TRAIN_RATIO = 0.8
VALID_RATIO = 0.1
TEST_RATIO = 0.1
DATASET_SIZE = len(X)

X_train= X[:int(DATASET_SIZE*TRAIN_RATIO)]
y_train= Y[:int(DATASET_SIZE*TRAIN_RATIO)]

X_valid= X[int(DATASET_SIZE*TRAIN_RATIO):int(DATASET_SIZE*(VALID_RATIO+TRAIN_RATIO))]
y_valid= Y[int(DATASET_SIZE*TRAIN_RATIO):int(DATASET_SIZE*(VALID_RATIO+TRAIN_RATIO))]

X_test= X[int(DATASET_SIZE*(VALID_RATIO+TRAIN_RATIO)):]
y_test= Y[int(DATASET_SIZE*(VALID_RATIO+TRAIN_RATIO)):]

print('DONNEES D\'ENTRAINEMENT D\'ENTREE= ',X_train.shape)
print('DONNEE D\'ENTRAINEMENT DE SORTIE=',y_train.shape)

print('DONNEE DE VALIDATION D\'ENTREE=',X_valid.shape)
print('DONNEE DE VALIDATION DE SORTIE=',y_valid.shape)

print('DONNEE DE TEST D\'ENTREE=',X_test.shape)
print('DONNEE DE TEST DE SORTIE=',y_test.shape)

"""configuration afin d'eviter les overflows"""

train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
train_dataset = train_dataset.shuffle(buffer_size = 8, reshuffle_each_iteration=True).batch(16).prefetch(tf.data.AUTOTUNE)
valid_dataset = tf.data.Dataset.from_tensor_slices((X_valid, y_valid))
valid_dataset = valid_dataset.shuffle(buffer_size = 8, reshuffle_each_iteration=True).batch(16).prefetch(tf.data.AUTOTUNE)
test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test))
test_dataset = test_dataset.shuffle(buffer_size = 8, reshuffle_each_iteration=True).batch(16).prefetch(tf.data.AUTOTUNE)

"""**NORMALISATION DES DONNEES**"""

normalisation_x = Normalization()
normalisation_x.adapt(X_train)
normalisation_x(X_train)

"""**MODELISATION DU SYSTEM**"""

model_1 = tf.keras.Sequential([
                     InputLayer(input_shape =(8,)),
                     normalisation_x,
                     Dense(84, activation='relu'),
                     Dense(84, activation='relu'),
                     Dense(84, activation='relu'),
                     Dense(1)
 ])
 model_1.summary()

tf.keras.utils.plot_model(model_1, to_file ="Regression_L(84).png", show_shapes=True)

for x, y in test_dataset:
  print(x,y)
  break

"""
**Optimisation, fonction de perte(loss) et mesure des performances**
"""

model_1.compile( optimizer = Adam(learning_rate = 0.1),
               loss = MeanAbsoluteError(),
               metrics = RootMeanSquaredError() )

"""ENTRAINEMENT DU MODEL 1 PROPREMENT DITES"""

history = model_1.fit(train_dataset, validation_data=valid_dataset, epochs = 100, verbose = 1)



"""evaluation du model (perte et performances)"""

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'])
plt.show()

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model performance')
plt.ylabel('rmse')
plt.xlabel('epoch')
plt.legend(['train', 'val'])
plt.show()

model_1.evaluate(X_test,y_test)

"""**test de prediction**"""

model_1.predict(tf.expand_dims(X_test[1], axis=0))

y_test[1]

y_pred= list(model_1.predict(X_test)[:,0])
y_true = list(y_test[:,0].numpy())

ind = np.arange(128)
plt.figure(figsize = (40, 20))

width = 0.4

plt.bar(ind,
        y_pred,
        width,
        label='prediction du model')
plt.bar(ind + width, y_true, width, label='prix actuel du pc')

plt.xlabel('Actuel vs Prix prédit')
plt.ylabel('prix de du pc')

plt.show()

