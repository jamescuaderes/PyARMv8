from Common import Bus

ITYPE = Bus(0, [0,0,0])
DTYPE = Bus(0, [0,0,1])
CBTYPE = Bus(0, [0,1,0])
BTYPE = Bus(0, [0,1,1])
MOVZ = Bus(0, [1,0,0])

class SignExtender:
	def performOp(self, signop, Imm26):
		extBit = []
		extensionIndex = []
		outputBus = Bus(64)

		if(signop == ITYPE):
			extBit.append(0)
			i = 10
			j = 0
			extensionIndex.append(12)
			while(i <= 21):
				outputBus.set(j, Imm26.at(i))
				i += 1
				j += 1
		elif(signop == DTYPE):
			extBit.append(Imm26.at(20))
			i = 12
			j = 0
			extensionIndex.append(9)
			while(i <= 20):
				outputBus.set(j, Imm26.at(i))
				i += 1
				j += 1
		elif(signop == CBTYPE):
			extBit.append(Imm26.at(23))
			i = 5
			j = 0
			extensionIndex.append(19)
			while(i <= 23):
				outputBus.set(j, Imm26.at(i))
				i += 1
				j += 1
		elif(signop == BTYPE):
			extBit.append(Imm26.at(25))
			i = 0
			extensionIndex.append(25)
			while(i <= 25):
				outputBus.set(i, Imm26.at(i))
				i += 1
		else:
			print("Error in sign extender")

		i = extensionIndex[0]
		while(i < 64):
			outputBus.set(i, extBit[0])
			i += 1

		return outputBus

if __name__ == '__main__':
	busI = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,
			0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0
	]

	busD = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,
			0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0
	]

	busB = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
	]

	busCB = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0
	] 

	se = SignExtender()		
	se.performOp(ITYPE, Bus(0, busI)).print()

	se.performOp(DTYPE, Bus(0, busD)).print()

	se.performOp(BTYPE, Bus(0, busB)).print()

	se.performOp(CBTYPE, Bus(0, busCB)).print()