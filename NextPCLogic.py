from Common import Bus
from ALU import ALU

class NextPCLogic:

	def __init__(self):
		self.adder = ALU()
		self.nextPC = None

	def performOp(self, uncondbranch, branch, aluZero, imm, currPC):
		if(uncondbranch or (branch and aluZero)):
			shiftedImm = self.shiftImm(imm)
			self.nextPC = self.adder.add(currPC, shiftedImm)[0]
		else:
			self.nextPC = self.adder.add(currPC, self.generateFour())[0]

		return self.nextPC 

	def generateFour(self):
		return Bus(0, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0
		])
		

	def shiftImm(self, imm):
		newImm = Bus(64)
		newImm.set(0, 0)
		newImm.set(1, 0)

		i = 2
		while(i < 64):
			newImm.set(i, imm.at(i-2))
			i += 1
		return newImm

if __name__ == '__main__':
	
	npl = NextPCLogic()

	#shiftedImm = 0x8
	imm = Bus(0, [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
	])

	#currPC = 0x8
	currPC = Bus(0, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0
	])

	npl.performOp(1, 0, 1, imm, currPC).print('x')
	npl.performOp(0, 1, 1, imm, currPC).print('x')
	npl.performOp(0, 1, 0, imm, currPC).print('x')

	alu = ALU()
	four = npl.generateFour()
	zero = Bus(64)
	minusFour = alu.performOp(Bus(0, [0,0,1,1]), zero, four)[0]

	npl.performOp(1, 0, 0, minusFour, currPC).print('x')