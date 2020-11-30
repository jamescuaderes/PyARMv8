from Common import Bus
from Common import locToIndex
from Common import indexToInstructionMemAddress
from Common import indexToDataMemAddress

class Memory:
	def __init__(self, isIMem, size=64):
		self.size = size
		self.mem = [Bus(64) for i in range(size)]
		self.isIMem = isIMem

	def performOp(self, addr, writeData, memread, memwrite):
		index = 0
		if(self.isIMem):
			index = indexToInstructionMemAddress(locToIndex(addr))
		else:
			index = indexToDataMemAddress(locToIndex(addr))

		if(memread and memwrite):
			print("Error, cannot read and write at the same time")

		elif(memread):
			return self.mem[index]

		elif(memwrite):
			self.mem[index] = writeData

		return Bus(64)