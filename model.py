import csv
import cv2
import numpy as np

st='trun'
lines=[]
with open('./'+st+'/driving_log.csv') as csvfile:
	reader=csv.reader(csvfile)
	for line in reader:
		lines.append(line)



from keras.models import Sequential
from keras.layers import Flatten,Dense,Lambda
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.layers import Cropping2D
from keras.layers import BatchNormalization 


#//build model
model=Sequential()

#model.add(Lambda(lambda x: (x / 255.0) - 0.5,input_shape=(160,320,3)))
model.add(Cropping2D(cropping=((0,0), (0,0)),input_shape=(160,320,3)))
model.add(BatchNormalization())

model.add(Convolution2D(24,5,5,subsample=(2,2), activation='relu'))
#model.add(MaxPooling2D())
model.add(Convolution2D(36,5,5,subsample=(2,2), activation='relu'))
model.add(Convolution2D(48,5,5,subsample=(2,2), activation='relu'))
model.add(Convolution2D(64,3,3, activation='relu'))
model.add(Convolution2D(64,3,3, activation='relu'))
#model.add(MaxPooling2D())

model.add(Flatten())

model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))

model.compile(loss='mse',optimizer='adam')

for i in range(1):
	images=[]
	measurements=[]
	images_flipped=[]
	measurements_flipped=[]
	for line in lines:
		source_path=line[i]
		filename=source_path.split('/')[-1]
		current_path='./'+st+'/IMG/'+filename
		image=cv2.imread(current_path)
		images.append(image)

		measurement=float(line[3])
		if i==1:
			measurement=(measurement+0.2)
		if i==2:
			measurement=(measurement-0.2)
		measurements.append(measurement)

		image_flipped = np.fliplr(image)
		images_flipped.append(image_flipped)

		measurement_flipped = -measurement
		measurements_flipped.append(measurement_flipped)


	X_train=np.array(images)
	Y_train=np.array(measurements)
	model.fit(X_train,Y_train,validation_split=0.1,shuffle=True,nb_epoch=7)

	
	X_train=np.array(images_flipped)
	Y_train=np.array(measurements_flipped)
	model.fit(X_train,Y_train,validation_split=0.1,shuffle=True,nb_epoch=7)

model.save('model.h5')
exit()

