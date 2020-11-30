from Common import Bus
from ALU import ALU
from SignExtender import SignExtender
from RegisterFile import RegisterFile
from Control import Control
from NextPCLogic import NextPCLogic
from Memory import Memory
from copy import deepcopy

class Processor:
	def __init__(self, initialPC=Bus(64), IMem=Memory(True), DMem=Memory(False)):
		self.ALU = ALU()
		self.IMem = IMem
		self.DMem = DMem
		self.signExtender = SignExtender()
		self.regFile = RegisterFile()
		self.Control = Control()
		self.nextPCLogic = NextPCLogic()
		self.PC = initialPC
		self.aluZero = 0

	def runCycle(self):
		#fetch the instruction from IMem
		instruction = self.IMem.performOp(self.PC, None, 1, 0)

		#get control signals
		self.Control.performOp(instruction.slice(31, 21))
		
		#reg file
		Source1Loc = instruction.slice(9, 5)
		Source2UpperBound = [20]
		Source2LowerBound = [16]
		if(self.Control.reg2loc):
			Source2UpperBound = [4]
			Source2LowerBound = [0]
		Source2Loc = instruction.slice(Source2UpperBound[0], Source2LowerBound[0])
		Source1, Source2 = self.regFile.performOp(0, Source1Loc, Source2Loc, None, None)

		#sign extension
		Imm26 = instruction.slice(25, 0)
		extendedImmediate = self.signExtender.performOp(self.Control.signop, Imm26)

		#ALU
		writeData = deepcopy(Source2)
		if(self.Control.alusrc):
			Source2 = extendedImmediate
		ALUOutput, self.aluZero = self.ALU.performOp(self.Control.aluop, Source1, Source2)

		#DMem
		DMemOutput = self.DMem.performOp(ALUOutput, writeData, self.Control.memread, self.Control.memwrite)

		#Write back to reg file
		writeReg = instruction.slice(4, 0)
		writeData = ALUOutput
		if(self.Control.mem2reg):
			writeData = DMemOutput
		self.regFile.performOp(self.Control.regwrite, Bus(5), Bus(5), writeReg, writeData)

		#NextPC
		self.PC = self.nextPCLogic.performOp(self.Control.uncondbranch, self.Control.branch, self.aluZero, extendedImmediate, self.PC)

		return (self.PC, DMemOutput)