from Common import Bus

AND = Bus(0, [0,0,0,0])
ORR = Bus(0, [0,0,0,1])
ADD = Bus(0, [0,0,1,0])
SUB = Bus(0, [0,0,1,1])
PASSSB = Bus(0, [0,1,0,0])

class ALU:

	def __init__(self):
		#flags will be implemented later, for now the only relevant flag is Zero
		self.zero = 0

	def add(self, s1, s2):
		cin = 0
		outputBus = Bus(s1.size)
		zero = 1
		for i in range(s1.size):
			bit1 = s1.at(i)
			bit2 = s2.at(i)

			if(bit1 and bit2):
				if(cin):
					outputBus.set(i, 1)
					cin = 1
					zero = 0
				else:
					outputBus.set(i, 0)
					cin = 1
			elif((bit1 and not bit2) or (not bit1 and bit2)):
				if(cin):
					outputBus.set(i, 0)
					cin = 1
				else:
					outputBus.set(i, 1)
					cin = 0
					zero = 0
			else:
				if(cin):
					outputBus.set(i, 1)
					cin = 0
					zero = 0
				else:
					outputBus.set(i, 0)
					cin = 0

		return outputBus, zero

	def TwosComp(self, source):
		one = Bus(source.size)
		invertedSource = Bus(source.size)

		for i in range(source.size):
			invertedSource.set(i, not source.at(i))
			if(i == 0):
				one.set(0, 1)
			else:
				one.set(i, 0)
		outputBus, trash = self.add(invertedSource, one)
		return outputBus	


	def performOp(self, aluop, s1, s2, setFlags=False):
		outputBus = Bus(s1.size)
		zero = [1]
		if(aluop == AND):
			for i in range(s1.size):
				newBit = s1.at(i) and s2.at(i)
				if(newBit and zero):
					zero[0] = 0 
				outputBus.set(i, newBit)
				i -= 1
		elif(aluop == ORR):
			for i in range(s1.size):
				newBit = s1.at(i) or s2.at(i)
				if(newBit and zero):
					zero[0] = 0 
				outputBus.set(i, newBit)
				i -= 1
		elif(aluop == ADD):
			outputBus, zero[0] = self.add(s1, s2)
		elif(aluop == SUB):
			outputBus, zero[0] = self.add(s1, self.TwosComp(s2))
		elif(aluop == PASSSB):
			outputBus = s2
			for i in range(s2.size):
				if(s2.at(i)):
					zero[0] = 0
					break
		else:
			print("Error with aluop")
			zero[0] = 0 
		return outputBus, zero[0]

	def runALU(aluop, s1, s2, setFlags=False):
		outputBus = Bus(s1.size)
		zero = 1
		outputBus, zero = self.performOp(aluop, Source1, Source2)
		self.zero = zero
		return outputBus, zero

if __name__ == '__main__':
	bus1 = Bus(0, [0,1,0,1])
	bus2 = Bus(0, [0,0,0,1])
	bus3 = Bus(0, [1,0,0,1])

	alu = ALU()
	outputBus, trash = alu.performOp(AND, bus3, bus2)
	outputBus.print()
	outputBus, trash = alu.performOp(ORR, bus1, bus3)
	outputBus.print()
	outputBus, trash = alu.performOp(SUB, bus1, bus2)
	outputBus.print()
	alu.performOp(ADD, bus1, bus2)[0].print()