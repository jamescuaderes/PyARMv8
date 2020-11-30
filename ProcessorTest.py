from Processor import Processor
from Common import HexToBin
from Common import Bus
from Common import locToIndex
from Memory import Memory

def constructIMem():
	'''
	/* Test Program 1:
	 * Program loads constants from the data memory. Uses these constants to test
	 * the following instructions: LDUR, ORR, AND, CBZ, ADD, SUB, STUR and B.
	 * 
	 * Assembly code for test:
	 * 
	 * 0: LDUR X9, [XZR, 0x0]    //Load 1 into x9
	 * 4: LDUR X10, [XZR, 0x8]   //Load a into x10
	 * 8: LDUR X11, [XZR, 0x10]  //Load 5 into x11
	 * C: LDUR X12, [XZR, 0x18]  //Load big constant into x12
	 * 10: LDUR X13, [XZR, 0x20]  //load a 0 into X13
	 * 
	 * 14: ORR X10, X10, X11  //Create mask of 0xf
	 * 18: AND X12, X12, X10  //Mask off low order bits of big constant
	 * 
	 * loop:
	 * 1C: CBZ X12, end  //while X12 is not 0
	 * 20: ADD X13, X13, X9  //Increment counter in X13
	 * 24: SUB X12, X12, X9  //Decrement remainder of big constant in X12
	 * 28: B loop  //Repeat till X12 is 0
	 * 2C: STUR X13, [XZR, 0x20]  //store back the counter value into the memory location 0x20
	 * 30: LDUR X13, [XZR, 0x20]
	 */

	63'h000: Data = 32'hF84003E9;
	63'h004: Data = 32'hF84083EA;
	63'h008: Data = 32'hF84103EB;
	63'h00c: Data = 32'hF84183EC;
	63'h010: Data = 32'hF84203ED;
	63'h014: Data = 32'hAA0B014A;
	63'h018: Data = 32'h8A0A018C;
	63'h01c: Data = 32'hB400008C;
	63'h020: Data = 32'h8B0901AD;

	63'h024: Data = 32'hCB09018C;
	63'h028: Data = 32'h17FFFFFD;
	63'h02c: Data = 32'hF80203ED;

	63'h030: Data = 32'hF84203ED;  //One last load to place stored value on memdbus for test checking.

	'''

	memory = [Bus(64) for i in range(13)]

	memory[0] = (Bus(0, list(map(int, HexToBin('0xF84003E9')))))
	memory[1] = (Bus(0, list(map(int, HexToBin('0xF84083EA')))))
	memory[2] = (Bus(0, list(map(int, HexToBin('0xF84103EB')))))
	memory[3] = (Bus(0, list(map(int, HexToBin('0xF84183EC')))))
	memory[4] = (Bus(0, list(map(int, HexToBin('0xF84203ED')))))
	memory[5] = (Bus(0, list(map(int, HexToBin('0xAA0B014A')))))
	memory[6] = (Bus(0, list(map(int, HexToBin('0x8A0A018C')))))
	memory[7] = (Bus(0, list(map(int, HexToBin('0xB400008C')))))
	memory[8] = (Bus(0, list(map(int, HexToBin('0x8B0901AD')))))
	memory[9] = (Bus(0, list(map(int, HexToBin('0xCB09018C')))))
	memory[10] = (Bus(0, list(map(int, HexToBin('0x17FFFFFD')))))
	memory[11] = (Bus(0, list(map(int, HexToBin('0xF80203ED')))))
	memory[12] = (Bus(0, list(map(int, HexToBin('0xF84203ED')))))

	output = Memory(True)
	output.mem = memory
	return output

def constructDMem():
	memory = [Bus(64) for i in range(5)]
	memory[0] = Bus(0, list(map(int, HexToBin('0x0000000000000001'))))
	memory[1] = Bus(0, list(map(int, HexToBin('0x000000000000000A'))))
	memory[2] = Bus(0, list(map(int, HexToBin('0x0000000000000005'))))
	memory[3] = Bus(0, list(map(int, HexToBin('0x123456789ABCEDFA'))))

	output = Memory(False)
	output.mem = memory
	return output

if __name__ == '__main__':
	p = Processor(Bus(64), constructIMem(), constructDMem())
	PC = Bus(64)
	while(locToIndex(PC) < 52):
		print("PC:", end='')
		PC.print('x')
		PC, output = p.runCycle()

	print('\n-----------------------------------------')
	print("Final Output: ")
	output.print()
	print('-----------------------------------------\n')