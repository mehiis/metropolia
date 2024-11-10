from filefifo import Filefifo

class FindPositivePeaks:
    def __init__(self, frequency, fileNumber, howManyPeaksToInspect):
        self.frequency:int = frequency#Hz (What is the specified frequency that the data is collected with.)
        self.data = Filefifo(10, name = f'capture_250Hz_0{fileNumber}.txt') #set .txt data into a Filefifo object. (first argument is a dummy)
        self.how_many_peak_to_peaks:int = howManyPeaksToInspect #how many peaks 
        
        self.samples:int = 0 #this variable holds current calculated samples
        self.peaks_detected:int = 0 #variable checks how many peaks has been already detected.
        self.rising:bool = False #checks if edge is rising or falling
        self.previous_value:int = 0 #saves the previous edge value for checking the peak

    def peak_detected(self, samples):
        self.rising = False 
        seconds = samples/self.frequency #we calculate seconds from collected samples and dividing it by our set frequency
        freq = 1/seconds #frequency = 1/time in secods

        if(self.peaks_detected > 0): #Skip the first peak because the measurement will most likely not provide accurate result of peaks.
            print("\nPeak at value: " + str(self.previous_value) + "\nAmount of samples: " + str(samples) + "\nTime between peaks: " + str(seconds) + "s\nPeak to peak frequency: " + str(freq) + "Hz")
            
        self.samples = 0 #reset samples back to 0
        self.peaks_detected += 1 #we have succesfully detected a peak
        
    def execute(self):
        while (self.peaks_detected < self.how_many_peak_to_peaks + 1):
            self.samples += 1
            
            current_value = self.data.get()
            difference = (current_value-self.previous_value)
            self.previous_value = current_value
            
            if(difference < 0 and self.rising):          
                self.peak_detected(self.samples)
            elif(difference > 0 and not self.rising):
                self.rising = True
                    
peakOne = FindPositivePeaks(250, 1, 3) #(Frequency of data, which .txt file (1-3), how many peaks to print)
peakOne.execute() #Run the loop.
