import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop, SGD, Adam
try:
    import Image
except ImportError:
    from PIL import Image
from pytesseract import image_to_string
#u ready for some neural nets?


# Get labeled meme data

print(image_to_string(Image.open('MEMES/SEX/15_Image_15.jpg')))

# Break into training, test, and validation sets

X_train = None
X_val = None
X_test = None
Y_train = None
Y_val = None
Y_test = None

# Set some parameters before we make and train the net

batch_size = 2048
epochs = 5
input_size = None
output_categories = None
hidden_size = None
dropout_rate = 0.1
num_layers = 10
hidden_act_type = 'relu'


model = Sequential()
model.add(Dense(activation='relu', input_shape=(input_size,), units=hidden_size))
for i in range(num_layers):
    model.add(Dropout(dropout_rate))
    model.add(Dense(activation=hidden_act_type, units=hidden_size))
model.add(Dense(activation='softmax', units=output_categories))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=Adam(),
              metrics=['accuracy'])

history = model.fit(X_train, Y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(X_val, Y_val))
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])