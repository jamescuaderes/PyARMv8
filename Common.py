def locToIndex(loc):
	index = 0
	count = 0
	for i in range(loc.size):
		if(loc.at(i)):
			index += 2 ** count
		count += 1
	return index

#used for memory efficiency
def indexToInstructionMemAddress(idx):
	#In ARMv8, all instructions are 4 bytes long
	return idx // 4

#used for memory efficiency
def indexToDataMemAddress(idx):
	#assume all data entries are long long int (64 bits or 8 bytes)
	return idx // 8

class Bus:
	def __init__(self, size=64, initializer=[]):
		self.bus = []
		self.size = 0

		if(len(initializer) != 0):
			for i in range(len(initializer)):
				self.bus.append(initializer[i])
				i -= 1
			self.size = len(initializer)

		else:
			self.bus = [0 for i in range(size)]
			self.size = size

	def __eq__(self, bus2):
		if(bus2 == None):
			return False
		return self.bus == bus2.bus

	def __add__(self, bus2):
		for bit in bus2.bus:
			self.bus.append(bit)
			self.size += 1
		return self

	def set(self, idx, val):
		self.bus[self.size - idx - 1] = val

	def at(self, idx):
		return self.bus[self.size - idx - 1]

	def slice(self, end, start):
		size = end - start + 1
		output = Bus(size)
		output.bus = self.bus[self.size-end-1:self.size-start]
		return output

	def getBitString(self):
		newBus = self.bus[:]
		#zero extend to be divisible by 4
		while(len(newBus) % 4 != 0):
			print("Appending zeros")
			newBus.insert(0,0)
		s = ''
		bitArray = []
		i = 0
		while(i < len(newBus)):
			for j in range(4):
				s += str(newBus[i])
				i += 1
			bitArray.append(s)
			s = ''
		return bitArray


	def print(self, format=''):
		bitArray = self.getBitString()

		hexTable = {
			'0000': '0',
			'0001': '1',
			'0010': '2',
			'0011': '3',
			'0100': '4',
			'0101': '5',
			'0110': '6',
			'0111': '7',
			'1000': '8',
			'1001': '9',
			'1010': 'A',
			'1011': 'B',
			'1100': 'C',
			'1101': 'D',
			'1110': 'E',
			'1111': 'F'
		}

		s = ''

		if(format.lower() == 'x'):
			#print in hex format
			s += '0x'
			for hexChar in bitArray:
				s += hexTable[hexChar]
		else:
			for hexChar in bitArray:
				for char in hexChar:
					s += char
				s += ' '
		print(s)

def HexToBin(s):
	table = {
			'0': '0000',
			'1': '0001',
			'2': '0010',
			'3': '0011',
			'4': '0100',
			'5': '0101',
			'6': '0110',
			'7': '0111',
			'8': '1000',
			'9': '1001',
			'A': '1010',
			'B': '1011',
			'C': '1100',
			'D': '1101',
			'E': '1110',
			'F': '1111'
		}

	#remove the 0x
	s = s[2:]
	output = ''
	for char in s:
		output += table[char]
	return output

if __name__ == '__main__':
	b = Bus(8)
	b.set(0, 1)
	b.set(1, 1)
	b.set(2, 0)
	b.set(3, 0)
	b.set(4, 1)
	b.set(5, 1)
	b.set(6, 0)
	b.set(7, 0)
	b.print()

	b2 = Bus(0, [0,0,1,1,0,0,1,1])
	#b2.print()

	newBus = b.slice(7, 0)
	#newBus.print()

	loc = Bus(0, [1,0,1,1])
	#print(locToIndex(loc))

	i = (Bus(0, list(map(int, HexToBin('0xF84003E9')))))
	print(HexToBin('0xF84003E9'))
	i.slice(31,21).print()