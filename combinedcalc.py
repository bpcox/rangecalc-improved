#! /usr/bin/env python3.4

#Written by User:NativeForeigner/Brian Cox
#All rights reserved (so far)
#Feel free to modify or suggest any positive changes though, I'm all ears

import ipaddress
import re

def parseIPv4Input(rawinput):
	IPv4regex = re.compile(r'[0-9]+(?:\.[0-9]+){3}')
	IPv4output = re.findall(IPv4regex, rawinput )

	IPv4List = list()

	for rawIP in IPv4output:
		try:
			tempAddress=ipaddress.IPv4Address(rawIP)
			IPv4List.append(tempAddress)
		except ValueError:
			continue
	IPv4List.sort(key=int)
	return IPv4List


def parseIPv6Input(rawinput):

	ipv6regex=re.compile('(?<![:.\w])(?:(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}|(?=(?:[A-F0-9]{0,4}:){0,7}[A-F0-9]{0,4}(?![:.\w]))(?:(?:[0-9A-F]{1,4}:){1,7}|:)(?:(?::[0-9A-F]{1,4}){1,7}|:)|(?:[A-F0-9]{1,4}:){7}:|:(?::[A-F0-9]{1,4}){7})(?![:.\w])',re.IGNORECASE)
	ipv6output=re.findall(ipv6regex, rawinput)

	IPv6List = list()

	for rawIP in ipv6output:
		try:
			tempAddress=ipaddress.IPv6Address(rawIP)
			IPv6List.append(tempAddress)
		except ValueError:
			continue

	IPv6List.sort(key=int)
	return IPv6List

def CIDRcalc(xorranges,version):

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
	if version==6:
		#if identical /128
		if xorranges==0:
			rCIDR = 128
			return CIDR

		CIDR = (128-(bin(binaryxor).count('0') + bin(binaryxor).count('1')-1))
		return CIDR

def generateBitmask(CIDR,version):
	if version==4:
		rangemaskstr = '1'*CIDR + '0'*(32-CIDR)
		rangemask = int(rangemaskstr,2)
		return rangemask

	if version==6:
		rangemaskstr = '1'*CIDR + '0'*(128-CIDR)
		rangemask = int(rangemaskstr,2)
		return rangemask

def calcIPv4Range(start,end):
	binarystart = int(start)
	binaryend = int(end)

        #run exclusive or on them to check for similarities
	binaryxor = binarystart ^ binaryend

	CIDRrangesize = CIDRcalc(binaryxor,4)


        #now, create a string which can be used to bitmask off the rightmost digits,
        #outside of the common range size


        #debug message meant to check bitmask is correct
        #print(rangemaskstr)

        #convert from string (easier to generate) to binary number
	rangemask = generateBitmask(CIDRrangesize,4)
        #implement masking
	finalrangeint = binarystart & rangemask

        #take this masked number, and convert back into IP, with IPv4address 
        #constructor
	finalrangeobject = ipaddress.IPv4Address(finalrangeint)
	#print(finalrangeobject)

	IPv4result= ipaddress.IPv4Network("/".join([str(finalrangeobject),str(CIDRrangesize)]))
	return IPv4result

def calcIPv6Range(start,end):
 #convert IP object to int such that binary operations can be applieed
	binarystart = int(start)
	binaryend = int(end)

        #run exclusive or on them to check for similarities
	binaryxor = binarystart ^ binaryend

        #if they are identical, the IP is the same, hence the ipv6 IP is a /128
	CIDRrangesize = CIDRcalc(binaryxor,6)

        #debug message, prints out size of range
        #print(rangesize)

        #create a string which can be converted into a bitmask for the rightmost digits    


        #debug message which prints rangemask
        #print(rangemaskstr)

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

def outputIPv4(IPv4Block):
	print("IPv4 Range is " + str(IPv4Block))
	print("Size of Range is " + str(IPv4Block.num_addresses))

def outputIPv6(IPv6Block):
	print("IPv6 Range is " + str(IPv6Block))
	print("Size of Range is " + str(IPv6Block.num_addresses))



rawinput = input("Enter raw IP information: ")

IPv4List = parseIPv4Input(rawinput)
IPv6List = parseIPv6Input(rawinput)



if IPv4List:
	start=IPv4List[0]
	end=IPv4List[-1]
	IPv4Block=calcIPv4Range(start,end)
	outputIPv4(IPv4Block)

if IPv6List:
	start=IPv6List[0]
	end=IPv6List[-1]
	IPv6Block=calcIPv6Range(start,end)
	outputIPv6(IPv6Block)

if not(IPv6List or IPv4List):
	print("Sorry, no valid IP address input")
	
