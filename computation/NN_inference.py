#Making one module visible to another
import sys
sys.path.append('../')



# A Computation which should eventually run on any device self.
# At present a dummy computation

class NN_inference:
    # Initializer
    def __init__(self):
        pass

    def initData(self, data):
        self.data=data

    def initComputation(self, model):
        self.model=model

    def runCompute(self):
        self.result=self.model.predict(self.data)

        return self.result

    def getInfo(self):
        print(self.model.summary())
        info="NN-Inference"
        return info
