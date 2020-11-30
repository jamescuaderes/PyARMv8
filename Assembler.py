import sys
from Common import Bus
from Common import HexToBin
from ALU import ALU
from Memory import Memory
from Processor import Processor
from Common import locToIndex
from copy import deepcopy

OPCODE_ADDREG = Bus(0, [1,0,0,0,1,0,1,1,0,0,0])
OPCODE_SUBREG = Bus(0, [1,1,0,0,1,0,1,1,0,0,0])
OPCODE_ANDREG = Bus(0, [1,0,0,0,1,0,1,0,0,0,0])
OPCODE_ORRREG = Bus(0, [1,0,1,0,1,0,1,0,0,0,0])
OPCODE_LDUR = Bus(0, [1,1,1,1,1,0,0,0,0,1,0])
OPCODE_STUR = Bus(0, [1,1,1,1,1,0,0,0,0,0,0])
OPCODE_ADDIMM = Bus(0, [1,0,0,1,0,0,0,1,0,0])
OPCODE_SUBIMM = Bus(0, [1,1,0,1,0,0,0,1,0,0])
OPCODE_B = Bus(0, [0,0,0,1,0,1])
OPCODE_CBZ = Bus(0, [1,0,1,1,0,1,0,0])

instructionToOp = {
	"ADD": OPCODE_ADDREG,
	"ADDI": OPCODE_ADDIMM,
	"SUB": OPCODE_SUBREG,
	"SUBI": OPCODE_SUBIMM,
	"AND": OPCODE_ANDREG,
	"ORR": OPCODE_ORRREG,
	"LDUR": OPCODE_LDUR,
	"STUR": OPCODE_STUR,
	"B": OPCODE_B,
	"CBZ": OPCODE_CBZ
}

def parseArgs(line):
	args = []
	
	firstSpaceSeen = False
	temp = ''
	i = 0
	while(i < len(line)):
		char = line[i]
		if(char == ":"):
			#symbol, return nothing because the symbol table has already been created
			return None

		if(char == '\n' or char == ']'):
			break

		if(char == ' ' or char == ','):
			args.append(temp)
			temp = ''
			i += 1
			if(line[i] == '[' or line[i] == ' '):
				i += 1
			if(line[i] == '['):
				i += 1
			continue
		temp += char
		i += 1
	args.append(temp)
	return args

def createRegister(reg):
	if(reg == 'XZR'):
		return Bus(0, [1,1,1,1,1])

	#remove the extra X
	reg = reg[1:]
	binaryReg = bin(int(reg))[2:]
	if(len(binaryReg) > 5):
		print("Reg is too large")
		return Bus(5)

	while(len(binaryReg) < 5):
		binaryReg = '0' + binaryReg

	lstBus = []
	for char in binaryReg:
		lstBus.append(int(char))
	return Bus(0, lstBus)

def createImm(imm):
	#remove the 0x
	imm = imm[2:]
	binImm = ''
	for hexChar in imm:
		binImm += HexToBin('0x' + hexChar)
	lstBus = []
	for char in binImm:
		lstBus.append(int(char))
	return Bus(0, lstBus)

def createImmFromSymbol(iNum, symbTable, symbol, immSize):
	desiredInstruction = symbTable[symbol]
	if(desiredInstruction == iNum):
		print('Error: symbol references current instruction')

	isNeg = False
	diff = desiredInstruction - iNum
	if(diff < 0):
		isNeg = True
	#create a bus of the immediate
	if(isNeg):
		binDiff = bin(diff)[3:]
	else:
		binDiff = bin(diff)[2:]
	lstBus = []
	for bit in binDiff:
		lstBus.append(int(bit))

	#adjust the size of the immediate
	if(len(lstBus) > immSize):
		print("Warning: sybol immediate greater than max immediate size")
	while(len(lstBus) < immSize):
		#sign extend
		lstBus.insert(0, 0)
	while(len(lstBus) > immSize):
		del lstBus[0]
	imm = Bus(0, lstBus)
	if(isNeg):
		twosComp = ALU()
		return twosComp.TwosComp(imm)

	return imm


def createITypeInstruction(args):
	opStr = args[0] + 'I'
	op = deepcopy(instructionToOp[opStr])
	Rd = createRegister(args[1])
	Rn = createRegister(args[2])
	imm = createImm(args[3])

	#correct the length of the immediate
	if(imm.size > 12):
		"Warning: I-type immediate is too large"
	while(imm.size < 12):
		imm.bus.insert(0,0)
		imm.size += 1
	while(imm.size > 12):
		del imm.bus[0]
		imm.size -= 1
	instruction = op + imm
	instruction = instruction + Rn
	instruction = instruction + Rd
	return instruction

def createRTypeInstruction(args):
	op = deepcopy(instructionToOp[args[0]])
	Rd = createRegister(args[1])
	shamt = Bus(6)
	Rn = createRegister(args[2])
	Rm = createRegister(args[3])
	instruction = op + Rm
	instruction = instruction + shamt
	instruction = instruction + Rn
	instruction = instruction + Rd
	return instruction

def createDTypeInstruction(args):
	op = deepcopy(instructionToOp[args[0]])
	Rt = createRegister(args[1])
	Rn = createRegister(args[2])
	imm = createImm(args[3])
	#correct the length of the immediate
	if(imm.size > 9):
		"Warnging: D-type immediate is too large"
	while(imm.size < 9):
		imm.bus.insert(0,0)
		imm.size += 1
	while(imm.size > 9):
		del imm.bus[0]
		imm.size -= 1
	extra = Bus(2)

	instruction = op + imm
	instruction = instruction + extra
	instruction = instruction + Rn
	instruction = instruction + Rt
	return instruction

def createBTypeInstruction(args, symbolTable, instructionNumber):
	op = deepcopy(instructionToOp[args[0]])
	imm = createImmFromSymbol(instructionNumber, symbolTable, args[1], 26)
	instruction = op + imm
	return instruction

def createCBTypeInstruction(args, symbolTable, instructionNumber):
	op = deepcopy(instructionToOp[args[0]])
	imm = createImmFromSymbol(instructionNumber, symbolTable, args[2], 19)
	Rt = createRegister(args[1])

	instruction = op + imm
	instruction = instruction + Rt
	return instruction

def parseLine(line, instructionNumber, symbolTable):
	args = parseArgs(line)
	if(args == None):
		#symbol
		return None

	if(args[0] == "ADD"):
		#scan for ADD or ADDI
		isAddI = False
		for arg in args:
			if(arg[0:2] == '0x'):
				isAddI = True
		if(isAddI):
			return createITypeInstruction(args)
		else:
			return createRTypeInstruction(args)

	elif(args[0] == 'SUB'):
		#scan for SUB or SUBI
		isSubI = False
		for arg in args:
			if(arg[0:2] == '0x'):
				isSubI = True
		if(isSubI):
			return createITypeInstruction(args)
		else:
			return createRTypeInstruction(args)

	elif(args[0] == 'AND'):
		return createRTypeInstruction(args)

	elif(args[0] == "ORR"):
		return createRTypeInstruction(args)

	elif(args[0] == "LDUR"):
		return createDTypeInstruction(args)

	elif(args[0] == "STUR"):
		return createDTypeInstruction(args)

	elif(args[0] == 'B'):
		return createBTypeInstruction(args, symbolTable, instructionNumber)

	elif(args[0] == "CBZ"):
		return createCBTypeInstruction(args, symbolTable, instructionNumber)

	else:
		print('Could not interpret the opcode')
		return Bus(32)

#step 1: create symbol table
#step 2: create instructions
#step 3: place instruction into memory
#step 4: execute

if __name__ == '__main__':
	args = sys.argv

	if(len(args) != 2):
		print("Error in command line args")
		sys.exit()

	file = open(args[1])
	lines = file.readlines()
	file.close()

	iNum = 0
	instructions = []
	symbolTable = {}

	#create the symbol table
	iCount = 0
	newLines = []
	for line in lines:
		if(':' in line):
			symbolTable[line[0:len(line)-2]] = iCount
		else:
			iCount += 1
			newLines.append(line)

	#parse the lines and create the instuctions
	print('\n')
	print("Hex Instructions: ")
	for line in newLines:
		instruction = parseLine(line, iNum, symbolTable)
		if(instruction == None):
			continue
		iNum += 1
		instruction.print('x')
		instructions.append(instruction)

	#place the instructions into Instruction Memory
	IMem = Memory(True, iCount)
	for i in range(iCount):
		IMem.mem[i] = instructions[i]

	#execute the instructions
	proc = Processor(Bus(64), IMem)
	DMemOut = Bus(1)
	print('\n')
	print("Execution of program: ")
	while(locToIndex(proc.PC) < (iCount * 4)):
		print('PC: 0x', locToIndex(proc.PC), sep='')
		trash, DMemOut = proc.runCycle()

	print('\n-----------------------------------------')
	print("Final Output: ")
	DMemOut.print()
	print('-----------------------------------------\n')