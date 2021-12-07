#!/usr/bin/env python
import threading

class WorkClass:
    """This class provides a place for the main processing of the 
    component to reside."""

    def __init__(self, __CLASS_NAME___ref, buffer_size):
        '''Initialization.  Sets a reference to parent.  
        Initializes the buffer.  Starts the Process data
        thread, which waits for data to be added to the buffer'''

        self.__CLASS_NAME___ref = __CLASS_NAME___ref
        self.buffer_size = buffer_size
	
        self.data_queue = []
        self.data_queue_lock = threading.Lock()
        self.data_signal = threading.Event()

        self.is_running = True

        self.process_thread = threading.Thread(target=self.Process)
        self.process_thread.start()
	
    def __del__(self):
        '''Destructor'''
        pass
	
    def AddData(self, I, Q):
        '''Generally called by parent.  Adds data to a buffer.
        The Process() method will wait for this buffer to be set.
        '''
        self.data_queue_lock.acquire()
        self.data_queue.insert(0, (I,Q))
        self.data_queue_lock.release()
        self.data_signal.set()
    	
    def Release(self):
        self.is_running = False
        self.data_signal.set()
		
    def Process(self):
        while self.is_running:
            self.data_signal.wait()  # wait for data to be aded to the 
                                     # buffer in self.AddData()
            while len(self.data_queue) > 0:
                # get the data from the buffer:
                self.data_queue_lock.acquire()
                new_data = self.data_queue.pop()
                self.data_queue_lock.release()
				
                # get data out of tuple
                I = new_data[0]
                Q = new_data[1]
				
                newI = [0 for x in range(len(I))]
                newQ = [0 for x in range(len(Q))]
		
		
                # Insert code here to do work
                # Example:
                #for x in range(len(I)):
                #    newI[x] = I[x]
                #    newQ[x] = Q[x]

					
                # Output the new data
                __SEND_TO_USES_PORTS__

            self.data_signal.clear()  # done reading the buffer
				

