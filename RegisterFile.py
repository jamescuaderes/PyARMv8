from Common import Bus
from Common import locToIndex

class RegisterFile:
	def __init__(self, width=32):
		self.width = width
		self.file = [Bus(64) for i in range(width)]

	def performOp(self, regwrite, loc1, loc2, writeLoc, writeData):
		#assume that we cannot write and read at the same time
		#the regwrite signal indicates whether we are writing or reading to the reg file
		if(regwrite):
			index = locToIndex(writeLoc)
			#preserve XZR
			if(index != 31):
				self.file[locToIndex(writeLoc)] = writeData
			return (Bus(64), Bus(64))
		else:
			return1 = self.file[locToIndex(loc1)]
			return2 = self.file[locToIndex(loc2)]

			return (return1, return2)

	def printRegFile(self, format=''):
		for i in range(self.width):
			print('[', i, '] ', sep='', end='')
			self.file[i].print(format)

if __name__ == '__main__':
	rf = RegisterFile(8)
	rf.printRegFile('x')

	bus = Bus(0, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
	])

	loc = Bus(4)
	loc.set(2,1)
	print()
	rf.performOp(1, Bus(4), Bus(4), loc, bus)

	trash, newBus = rf.performOp(0, Bus(4), loc, Bus(4), Bus(64))

	newBus.print('x')