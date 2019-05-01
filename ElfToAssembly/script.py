#!/usr/bin/python2
import re, subprocess, sys, shlex, binascii

if __name__ == '__main__':
	if len(sys.argv) > 2:
		print "Usage: %s <file>" % sys.argv[0]
	
	#stdout = subprocess.check_output(['/usr/bin/arm-none-eabi-objdump', '-D', sys.argv[1]])
	cmd = "arm-none-eabi-objdump -d " + sys.argv[1] + " | sed '/<main>:/,/^$/!d'"
	ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output = ps.communicate()[0]
	#print output

	bytes = []
	bin_bytes = []
	bin_file = open("BinCodes.txt","w+")

	for x in output.split():
		parsed_bytes = ''.join(re.findall('^[0-9a-f][0-9a-f][0-9a-f][0-9a-f]$', x))
		if parsed_bytes is not '':
			bytes.append(parsed_bytes)
	
	for byte in bytes:
		#hex2bin_bytes = binascii.unhexlify(byte)
		#bin_bytes.append(hex2bin_bytes.fromhex())
		bin_bytes.append(bin(int(byte, 16))[2:].zfill(8))

	for x in bin_bytes:		
		bin_file.write(str(x) + '\n')

	bin_file.close()	
		
	print '[**] HEX codes [**]'
	print bytes
	print '[**] BIN codes [**]'
	print bin_bytes
	
	
