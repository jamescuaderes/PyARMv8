from Common import Bus

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

class Control:

	def __init__(self):
		self.branch = 0
		self.uncondbranch = 0
		self.memread = 0
		self.memwrite = 0
		self.mem2reg = 0
		self.reg2loc = 0
		self.aluop = Bus(4)
		self.signop = Bus(3)
		self.regwrite = 0
		self.alusrc = 0

	def performOp(self, opcode):
		if(opcode == OPCODE_ADDREG):
			self.branch = 0
			self.uncondbranch = 0
			self.memread = 0
			self.memwrite = 0
			self.mem2reg = 0
			self.reg2loc = 0
			self.aluop = Bus(0, [0,0,1,0])
			self.signop = Bus(3)
			self.regwrite = 1
			self.alusrc = 0
			
		elif(opcode == OPCODE_SUBREG):
			self.branch = 0
			self.uncondbranch = 0
			self.memread = 0
			self.memwrite = 0
			self.mem2reg = 0
			self.reg2loc = 0
			self.aluop = Bus(0, [0,0,1,1])
			self.signop = Bus(3)
			self.regwrite = 1
			self.alusrc = 0

		elif(opcode == OPCODE_ANDREG):
			self.branch = 0
			self.uncondbranch = 0
			self.memread = 0
			self.memwrite = 0
			self.mem2reg = 0
			self.reg2loc = 0
			self.aluop = Bus(0, [0,0,0,0])
			self.signop = Bus(3)
			self.regwrite = 1
			self.alusrc = 0

		elif(opcode == OPCODE_ORRREG):
			self.branch = 0
			self.uncondbranch = 0
			self.memread = 0
			self.memwrite = 0
			self.mem2reg = 0
			self.reg2loc = 0
			self.aluop = Bus(0, [0,0,0,1])
			self.signop = Bus(3)
			self.regwrite = 1
			self.alusrc = 0

		elif(opcode == OPCODE_LDUR):
			self.branch = 0
			self.uncondbranch = 0
			self.memread = 1
			self.memwrite = 0
			self.mem2reg = 1
			self.reg2loc = 1
			self.aluop = Bus(0, [0,0,1,0])
			self.signop = Bus(0, [0,0,1])
			self.regwrite = 1
			self.alusrc = 1

		elif(opcode == OPCODE_STUR):
			self.branch = 0
			self.uncondbranch = 0
			self.memread = 0
			self.memwrite = 1
			self.mem2reg = 0
			self.reg2loc = 1
			self.aluop = Bus(0, [0,0,1,0])
			self.signop = Bus(0, [0,0,1])
			self.regwrite = 0
			self.alusrc = 1

		elif(opcode.slice(10,1) == OPCODE_ADDIMM):
			self.branch = 0
			self.uncondbranch = 0
			self.memread = 0
			self.memwrite = 0
			self.mem2reg = 0
			self.reg2loc = 0
			self.aluop = Bus(0, [0,0,1,0])
			self.signop = Bus(3)
			self.regwrite = 1
			self.alusrc = 1

		elif(opcode.slice(10,1) == OPCODE_SUBIMM):
			self.branch = 0
			self.uncondbranch = 0
			self.memread = 0
			self.memwrite = 0
			self.mem2reg = 0
			self.reg2loc = 0
			self.aluop = Bus(0, [0,0,1,1])
			self.signop = Bus(3)
			self.regwrite = 1
			self.alusrc = 1

		elif(opcode.slice(10,5) == OPCODE_B):
			self.branch = 0
			self.uncondbranch = 1
			self.memread = 0
			self.memwrite = 0
			self.mem2reg = 0
			self.reg2loc = 0
			self.aluop = Bus(4)
			self.signop = Bus(0, [0,1,1])
			self.regwrite = 0
			self.alusrc = 0

		elif(opcode.slice(10,3) == OPCODE_CBZ):
			self.branch = 1
			self.uncondbranch = 0
			self.memread = 0
			self.memwrite = 0
			self.mem2reg = 0
			self.reg2loc = 1
			self.aluop = Bus(0, [0,1,0,0])
			self.signop = Bus(0, [0,1,0])
			self.regwrite = 0
			self.alusrc = 0

		else:
			print("Error in control block")
			opcode.print()
			self.branch = 0
			self.uncondbranch = 0
			self.memread = 0
			self.memwrite = 0
			self.mem2reg = 0
			self.reg2loc = 0
			self.aluop = Bus(4)
			self.signop = Bus(3)
			self.regwrite = 0
			self.alusrc = 0