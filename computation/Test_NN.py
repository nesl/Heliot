from NN_inference import NN_inference

inference=NN_inference()


#Load a NN model in Keras
model_path='/media/sandeep/43f108db-7642-4e01-b534-59eca3dd838f/Research/vEdge/Trained_models/MNIST_model-1.h5'
from keras.models import load_model
model = load_model(model_path)


#Load MNIST data in keras
import keras
from keras.datasets import mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_test = x_test.reshape(10000, 784)
x_test = x_test.astype('float32')



inference.initComputation(model)
inference.initData(x_test)

result=inference.runCompute()

print(result.shape)
