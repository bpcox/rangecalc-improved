#! /usr/bin/env python3.4

#Written by User:NativeForeigner/Brian Cox
#All rights reserved (so far)
#Feel free to modify or suggest any positive changes though, I'm all ears

import ipaddress
import re


#takes input from input(), parses for IPv4 addresses
def parseIPv4Input(rawinput):
	IPv4regex = re.compile(r'[0-9]+(?:\.[0-9]+){3}')
	IPv4output = re.findall(IPv4regex, rawinput )

	IPv4Listing = set()
#looks through potential matches. filters false positives with ValueError
	for rawIP in IPv4output:
		try:
			tempAddress=ipaddress.IPv4Address(rawIP)
			IPv4Listing.add(tempAddress)
		except ValueError:
			continue
#then looks for ranges
	IPv4rangeregex = re.compile(r'[0-9]+(?:\.[0-9]+){3}/[0-9]{1,2}')
	IPv4rangeoutput = re.findall(IPv4rangeregex, rawinput)

#same method as above
	for rawIPnetwork in IPv4rangeoutput:
		try:
			tempRange=ipaddress.IPv4Network(rawIPnetwork)
			IPv4Listing.add(tempRange[0])
			IPv4Listing.add(tempRange[-1])
		except ValueError:
			continue

	IPv4Listing=list(IPv4Listing)
	IPv4Listing.sort(key=int)
	return IPv4Listing

#looks for IPv6 addresses
#TODO implement IPv6 range support
def parseIPv6Input(rawinput):

	ipv6regex=re.compile('(?<![:.\w])(?:(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}|(?=(?:[A-F0-9]{0,4}:){0,7}[A-F0-9]{0,4}(?![:.\w]))(?:(?:[0-9A-F]{1,4}:){1,7}|:)(?:(?::[0-9A-F]{1,4}){1,7}|:)|(?:[A-F0-9]{1,4}:){7}:|:(?::[A-F0-9]{1,4}){7})(?![:.\w])',re.IGNORECASE)
	ipv6output=re.findall(ipv6regex, rawinput)

	IPv6Listing = set()

	for rawIP in ipv6output:
		try:
			tempAddress=ipaddress.IPv6Address(rawIP)
			IPv6Listing.add(tempAddress)
		except ValueError:
			continue
	IPv6Listing=list(IPv6Listing)
	IPv6Listing.sort(key=int)
	return IPv6Listing
#returns rangesize
def CIDRcalc(xorranges,version):
#ipv4
	if version==4:
		#if identical is a /32
		if xorranges==0:
			CIDR = 32
			return CIDR
		#otherwise, the value is 32 -(number of 0s + number of 1s - 1)
		#this is because python cuts off the leading 0s, and the -1 compensates for
		#the 0, in the 0b which prefixes the binary text
		CIDR = (32-(bin(xorranges).count('0') + bin(xorranges).count('1')-1))
		return CIDR
#ipv6
	if version==6:
		#if identical /128
		if xorranges==0:
			CIDR = 128
			return CIDR

		CIDR = (128-(bin(binaryxor).count('0') + bin(binaryxor).count('1')-1))
		return CIDR

#given CIDR size, and IPv4vs IPv6 returns integer bitmask
def generateBitmask(CIDR,version):
	if version==4:
		rangemaskstr = '1'*CIDR + '0'*(32-CIDR)
		rangemask = int(rangemaskstr,2)
		return rangemask

	if version==6:
		rangemaskstr = '1'*CIDR + '0'*(128-CIDR)
		rangemask = int(rangemaskstr,2)
		return rangemask
#core calculation, returns range given two IP addresses
def calcIPv4Range(start,end):
	binarystart = int(start)
	binaryend = int(end)

        #run exclusive or on them to check for similarities
	binaryxor = binarystart ^ binaryend

	CIDRrangesize = CIDRcalc(binaryxor,4)

	rangemask = generateBitmask(CIDRrangesize,4)
        #implement masking
	finalrangeint = binarystart & rangemask

        #take this masked number, and convert back into IP, with IPv4address 
        #constructor
	finalrangeobject = ipaddress.IPv4Address(finalrangeint)

	IPv4result= ipaddress.IPv4Network("/".join([str(finalrangeobject),str(CIDRrangesize)]))
	return IPv4result
#calculate IPv6 range given highest and lowest IPs
def calcIPv6Range(start,end):
 #convert IP object to int such that binary operations can be applieed
	binarystart = int(start)
	binaryend = int(end)

        #run exclusive or on them to check for similarities
	binaryxor = binarystart ^ binaryend

        #if they are identical, the IP is the same, hence the ipv6 IP is a /128
	CIDRrangesize = CIDRcalc(binaryxor,6)


        #converts from binary string to int for masking
	rangemask = generateBitmask(CIDRrangesize,6)

        #bitmask off the right digits, outside of the common range
	finalrangeint = binarystart & rangemask
        #create IP address which forms base of IP range
	finalrangeobject = ipaddress.IPv6Address(finalrangeint)
	#print(finalrangeobject)

        #make IPv6Network object which represents the result
	IPv6result =ipaddress.IPv6Network("/".join([str(finalrangeobject), str(CIDRrangesize)]))
	return IPv6result

#outputs overall result
def outputIPv4(IPv4Block):
	print("IPv4 Range is " + str(IPv4Block))
	print("Size of Range is " + str(IPv4Block.num_addresses))

#outputs overall result
def outputIPv6(IPv6Block):
	print("IPv6 Range is " + str(IPv6Block))
	print("Size of Range is " + str(IPv6Block.num_addresses))

#loops through, sorts IP ranges from IPs
def outputIPmulti(subranges,version):
	if version ==4:	
		IPlist = list()
		for IPrange in subranges:
			if IPrange.prefixlen<32:
				print(str(IPrange))
			else:
				IPlist.append(IPrange[0])
		for IPaddress in IPlist:
			print(str(IPaddress))

	if version==6:
		IPlist = list()
		for IPrange in subranges:
			if IPrange.prefixlen<128:
				print(str(IPrange))
			else:
				IPlist.append(IPrange[0])

		for IPaddress in IPlist:
			print(str(IPaddress))

#calculates (potentially) multiple ranges, with a cap in size (maximum)
#allows for output that appears intelligent
def maxsizecalcIPv4(IPv4List,maximum):
	baseIP = IPv4List[0]
	resultList = list()
	for prevIP, IP in zip(IPv4List,IPv4List[1:]):
		binaryxor = int(baseIP) ^ int(IP)
		if CIDRcalc(binaryxor,4) < maximum:
			resultList.append(calcIPv4Range(baseIP,prevIP))
			baseIP = IP
	resultList.append(calcIPv4Range(baseIP,IPv4List[-1]))

	return resultList

#calculates (potentially) multiple ranges, with a cap in size (maximum)
#allows for output which appears intelligent
def maxsizecalcIPv6(IPv6List,maximum):
	baseIP = IPv6List[0]
	resultList = list()
	for prevIP, IP in zip(IPv6List,IPv6List[1:]):
		binaryxor = int(baseIP) ^ int(IP)
		if CIDRcalc(binaryxor,6) < maximum:
			resultList.append(calcIPv6Range(baseIP,prevIP))
			baseIP = IP
	resultList.append(calcIPv6Range(baseIP,IPv6List[-1]))

	return resultList



rawinput = input("Enter raw IP information: ")


IPv4List = parseIPv4Input(rawinput)
IPv6List = parseIPv6Input(rawinput)

#Allow for dynamic changes to the max size of ranges portion
#if IPv4List:
#	maxIPv4size = input("Would you like to enable IPv4 subranges? Press enter if no, enter a number from 8 to 32 otherwise: ")
#if IPv6List:
#	maxIPv4size = input("Would you like to enable IPv6 subranges? Press enter from no, enter a number 16 to 128 otherwise: ")

if IPv4List:
	start=IPv4List[0]
	end=IPv4List[-1]
	IPv4Block=calcIPv4Range(start,end)
	outputIPv4(IPv4Block)
	outputIPmulti(maxsizecalcIPv4(IPv4List,12),4)

if IPv6List:
	start=IPv6List[0]
	end=IPv6List[-1]
	IPv6Block=calcIPv6Range(start,end)
	outputIPv6(IPv6Block)
	outputIPmulti(maxsizecalcIPv6(IPv6List,48),6)

if not(IPv6List or IPv4List):
	print("Sorry, no valid IP address input")
	
