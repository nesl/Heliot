#Making one module visible to another
import sys
sys.path.append('../')

from main.Slave import Slave
import rpyc


class SlaveRpc(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        print('Slave RPC on_connect')
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        print('Slave RPC on_disconnect')
        pass

    def exposed_initialize(self):
        self.slave=Slave()

    def exposed_setSlave(self,slave):
        self.slave=slave
        print('in exposed_setSlave')

    def exposed_updateSlave_data_from_sensor(self):
        self.slave.updateComputeDataFromSensor()
        print('in exposed_updateSlave_data_from_sensor')


    def exposed_update_compute(self,compute):
        self.slave.setCompute(compute)


    def exposed_update_data(self,data):
        self.slave.updateComputeData(data)

    def exposed_run_compute(self):
        return self.slave.runCompute()


    def exposed_print_details(self):
        pass
        #print(self.slave.printCompute())
        #print(self.slave.printSensor())


s=SlaveRpc()


##Making a sample Compute
#importing the inference module
# from computation.NN_inference import NN_inference
#
# inference=NN_inference()
# #Load a NN model in Keras
# model_path='/media/sandeep/43f108db-7642-4e01-b534-59eca3dd838f/Research/vEdge/Trained_models/MNIST_model-1.h5'
# from keras.models import load_model
# model = load_model(model_path)
# inference.initComputation(model)
# s.on_connect("")
# s.exposed_update_compute(inference)
