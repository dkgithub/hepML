from keras.models import Sequential
from keras.layers import Dense
from MlClasses.PerformanceTests import rocCurve

def findLayerSize(layer,refSize):

    if isinstance(layer, float):
        return int(layer*refSize)
    elif isinstance(layer, int):
        return layer
    else:
        print 'WARNING: layer must be int or float'
        return None

class Dnn(object):

    def __init__(self,data,output=None):
        self.data = data
        self.output = output

    def setup(self,hiddenLayers=[1.0]):

        '''Setup the neural net. Input a list of hiddenlayers
        if you fill float takes as fraction of inputs+outputs
        if you fill int takes as number. 
        E.g.:  hiddenLayers=[0.66,20] 
        has two hidden layers, one with 2/3 of input plus output 
        neurons, second with 20 neurons.
        All the layers are fully connected (dense)
        ''' 

        inputSize=len(self.data.X_train.columns)

        #Find number of unique outputs
        outputSize = len(self.data.y_train.iloc[:,0].unique())
        refSize=inputSize+outputSize

        self.model = Sequential()

        assert len(hiddenLayers)>=1, 'Need at least one hidden layer'

        #Add the first layer, taking the inputs
        self.model.add(Dense(units=findLayerSize(hiddenLayers[0],refSize), 
            activation='relu', input_dim=inputSize))

        #Add the extra hidden layers
        for layer in hiddenLayers[1:]:
            self.model.add(Dense(units=findLayerSize(hiddenLayers[0],refSize), 
                activation='relu'))

        #Add the output layer and choose the type of loss function
        #Choose the loss function based on whether it's binary or not
        if outputSize==2: 
            #It's better to choose a sigmoid function and one output layer for binary
            # This is a special case of n>2 classification
            model.add(Dense(1, activation='sigmoid'))
            loss = 'binary_crossentropy'
        else: 
            #Softmax forces the outputs to sum to 1 so the score on each node
            # can be interpreted as the probability of getting each class
            model.add(Dense(outputSize, activation='softmax'))
            loss = 'categorical_crossentropy'

        #After the layers are added compile the model
        self.model.compile(loss=loss,
            optimizer='adam',metrics=['accuracy'])

    def fit(self):

        self.model.fit(self.data.X_train, self.data.Y_train, 
                epochs=5, batch_size=32)

    def classificationReport(self):

        self.report = model.evaluate(self.data.X_test, self.data.Y_test, batch_size=128)

        if not os.path.exists(self.output): os.makedirs(self.output)
        f=open(os.path.join(self.output,'classificationReport.txt'),'w')
        f.write( 'Performance on test set:')
        f.write(self.report)

    def rocCurve(self):

        rocCurve(self.model.predict(self.data.X_test), batch_size=128),self.data.X_test,self.data.y_test,self.output)
        rocCurve(self.model.predict(self.data.X_test),self.data.X_train,self.data.y_train,self.output,append='_train')

    def diagnostics(self):
        self.classificationReport()
        self.rocCurve()
