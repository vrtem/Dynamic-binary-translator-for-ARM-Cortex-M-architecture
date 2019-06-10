#!/usr/bin/python2
import re, subprocess, sys, shlex, binascii, textwrap
import json
import time

start_time = time.time()

if __name__ == '__main__':
	with open("dictionary.json", "r") as read_file:
		bits_dict = json.load(read_file)

	if len(sys.argv) > 2:
		print "Usage: %s <file>" % sys.argv[0]
	
	cmd = "arm-none-eabi-objdump -d " + sys.argv[1] + " | sed '/<main>:/,/^$/!d'"
	ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output = ps.communicate()[0]

	bytes = []
	bin_bytes = []
	bin_file = open("BinCodes.txt","w+")

	for x in output.split():
		parsed_bytes = ''.join(re.findall('^[0-9a-f][0-9a-f][0-9a-f][0-9a-f]$', x))
		if parsed_bytes is not '':
			bytes.append(parsed_bytes)
	
	for byte in bytes:
		bin_bytes.append(bin(int(byte, 16))[2:].zfill(8))

	for x in bin_bytes:		
		bin_file.write((str(x)).zfill(16) + '\n')

	bin_file.close()	
		
	print '[**] HEX codes [**]'
	print bytes
	print '[**] BIN codes [**]'
	print bin_bytes
	
	
	sep_bytes = []

	for x in range(len(bin_bytes)):
		sep_bytes.append(textwrap.wrap(bin_bytes[x],1))

	print 'Test:'
	for x in range(len(sep_bytes)):
		
		print sep_bytes[x]
		counter = 0
		#here we counting from left side and from 1
		#16 bits
		allBits = ''.join(sep_bytes[x][:16])
		#16,15,14,13 bits
		firstFourBits = ''.join(sep_bytes[x][:4])
		#12 bit
		fifthBit =''.join(sep_bytes[x][4])
		#12,11,10 bits
		fifthToSeventhBits =''.join(sep_bytes[x][4:7])
		#12,11,10,9 bits
		fifthToEighthBits =''.join(sep_bytes[x][4:8])
		#9 bit
		eighthBit =''.join(sep_bytes[x][7])
		#10 bit
		ninethBit =''.join(sep_bytes[x][8])
		#12,11,10,9,8 bits
		fifthToNinethBits =''.join(sep_bytes[x][4:9])
		#7th bit
		ninethBit =''.join(sep_bytes[x][9])
		#'0010' or '0011' or '1001' 11,10,9 bits
		sixthToEighthBits =''.join(sep_bytes[x][5:8])
		ninethTo16Bits =''.join(sep_bytes[x][8:16])
		ninethTo11Bits =''.join(sep_bytes[x][9:12])
		tenthTo16Bits =''.join(sep_bytes[x][9:16])
		eighthTo11Bits =''.join(sep_bytes[x][7:10])
		eleventhTo13Bits =''.join(sep_bytes[x][10:13])
		thirteenthTo16Bits =''.join(sep_bytes[x][11:])
		six2ten =''.join(sep_bytes[x][6:10])
		six28 =''.join(sep_bytes[x][6:9])

		#result of passing 13-16 bits (counted from 1) to dictionary
		result1 = bits_dict.get(firstFourBits)

		#here we're checking if our string of bits is NOP
		if allBits == '1011111100000000':
			result = 'nop'
		#here is the special check for the pop R/pop LR
		elif firstFourBits == '1011':
			result = result1.get(fifthToSeventhBits)
			if fifthToSeventhBits == '000':
				result = result.get(ninethBit)
				offset = str(int((str(tenthTo16Bits) + '00'), 2))
				result = result + ' #' + offset

			else:	
				result = result.get(eighthBit)
				for t in ninethTo16Bits:
					if t == '1':
						result = result + ' #' + str(7 - counter)
					counter += 1

		#here is the special check for the branch conditional
		elif firstFourBits == '1101':
			result = result1 + ' #' + str(int(fifthToEighthBits, 2)) + ' #' + str(int(ninethTo16Bits, 2))

		#here is the special check for the bx low/high
		elif firstFourBits == "0100":
			result = result1.get(fifthToNinethBits)
			result = result.get(ninethBit)

		elif firstFourBits == '1100':
			result = result1.get(fifthBit)
			if six28 == '001':
				baseReg = ' r3'
			else:
				baseReg = ' r'
			destReg = ' r' + str(int(ninethTo11Bits,2))
			offset = ' #' + str(int(thirteenthTo16Bits,2)+1)
			result = result + baseReg + destReg + offset
		
		elif firstFourBits == '1000':
			result = result1.get(fifthBit)
			baseReg = ' r' + str(int(eleventhTo13Bits,2))
			destReg = ' r' + str(int(thirteenthTo16Bits,2))
			offset = ' #' + str(int((str(six2ten)+'0'),2))
			result = result + baseReg + destReg + offset

		else:
			result = result1.get(fifthBit)

		if firstFourBits == '1010':
			result = result + ' r' + str(int(sixthToEighthBits, 2))
			result = result + ' #' + str(int(ninethTo16Bits,2))
		
		if firstFourBits == '0010':
			result = result + ' r' + str(int(sixthToEighthBits, 2))
			result = result + ' #' + str(int(ninethTo16Bits,2))

		if firstFourBits == '0011':
			result = result + ' r' + str(int(sixthToEighthBits, 2))
			result = result + ' #' + str(int(ninethTo16Bits,2))
		
		if firstFourBits == '1001':
			result = result + ' r' + str(int(sixthToEighthBits, 2))
			result = result + ' #' + str(int(ninethTo16Bits,2))

		if firstFourBits == '0101':
			result = result + ' r' + str(int(eighthTo11Bits, 2))
			result = result + ' [r' + str(int(eleventhTo13Bits,2))
			result = result + ', r' + str(int(thirteenthTo16Bits,2)) + ']'


		print result

timeOfAlgorithm = "--- %s seconds --- \n" % (time.time() - start_time)
print timeOfAlgorithm
results_filename = 'result_' + str(sys.argv[1]) +'_.txt'
resultsFile=open(results_filename, "a+")
resultsFile.write(timeOfAlgorithm)
resultsFile.close()

		


