from filefifo import Filefifo

class Scaler:
    def __init__(self,frequency, file_number, scale, how_many_seconds_to_read_data, inspect_for_seconds):
        self.scale = scale #Multiplier value with which you can scale your plot being 0 - 1*scaled value
        self.data = Filefifo(10, name = f'capture_250Hz_0{file_number}.txt') #set .txt data into a Filefifo object. (first argument is a dummy)
        self.frequency:int = frequency#Hz (What is the specified frequency that the data is collected with.)
        self.how_many_seconds_to_read_data = how_many_seconds_to_read_data #how many seconds of data will be inspected for getting min+max values from given data.
        self.inspect_for_seconds = inspect_for_seconds #how many seconds of data printed
        
    def execute(self): #Starting function
        #functions executed in order:  GetMinMax() -> ReadData() -> Normalize()
        self.get_min_max() #start code with finding min and max values with this function        
        
    def get_min_max(self):
        #initialize min-max values with first value in the 
        new_value:int = self.data.get()
        min_value:int = new_value
        max_value:int = new_value
        
        for i in range(self.frequency * self.how_many_seconds_to_read_data): #loop data for given amount of seconds (frequency*howManySeconds)
            new_value = self.data.get() #get new value from fifo object
            
            if(new_value < min_value): #if newValue is less than recorded minValue, set new minumum value
                min_value = new_value
            
            if(new_value > max_value): #if newValue is greater than recorded minValue, set new maximum value
                max_value = new_value

        #print("Max value: " + str(self.maxValue) + "\nMin value: " + str(self.minValue))
        self.read_data(min_value, max_value)
            
    def normalize(self, value, min_value, max_value):
        value = (value - min_value)/(max_value-min_value) #normalize value between float (0.0 - 1.0)
        return int(value * self.scale) #return value with scaler (e.g. 0.4 * 100 = 40) (100 = set variable)
    
    def read_data(self, min_value, max_value): #function prints value and makes plotter move
        for i in range(self.frequency * self.inspect_for_seconds): #loop for (frequency * howManySeconds)
            print(self.normalize(self.data.get(), min_value, max_value))
             
scale1 = Scaler(250, 2, 100, 2, 10) #(frequencyOfData, which file to inspect(1-3), scale size, how many seconds to find max-min, how many seconds to print given data scaled)
scale1.execute() #execute