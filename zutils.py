import time
import threading

class DoAfterTrigger():
	def __init__(self, dofunc, after = None):
		self.timer = None
		self.trigtime = None
		self.dofunc = dofunc
		self.wakeat = None
		
		if after is not None:
			self.trigger(after)
	
	def _triggered(self):
		if time.time() <= self.wakeat:
			self._wait()
		else:
			self.dofunc()
	
	def _wait(self):
		if self.timer:
			self.timer.cancel()
	 	self.timer = threading.Timer(self.wakeat - time.time(), self._triggered)
		self.timer.start();
	
	def trigger(self, after):
		self.wakeat = time.time() + after
		self._wait()
		return self

def runTests():
	def dome():
		print("dome")
	DoAfterTrigger(dome, 3.0)

	def dome2():
		print("dome2")
	DoAfterTrigger(dome2).trigger(2.0)

	def dome3():
		print("dome3")
	x = DoAfterTrigger(dome3)
	x.trigger(1.0)
	x.trigger(4.0)

if __name__=='__main__':
	runTests()
