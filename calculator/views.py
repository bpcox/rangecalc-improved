from django.shortcuts import render
import django.template
from calculator.forms import RangeForm

import sys
import os
scriptpath = '../webcalc.py'

sys.path.append(os.path.abspath(scriptpath))

import webcalc

# Create your views here.

def index(request):
    form = RangeForm()
    output = {} 
    mutatedRanges = ''
    if request.method == 'POST':
        form = RangeForm(request.POST)
        if form.is_valid():
            ranges = form.cleaned_data['ranges']
            # do something to it!
            parsedIPv4Input = webcalc.parseIPv4Input(ranges)
            parsedIPv6Input = webcalc.parseIPv6Input(ranges)
            if not parsedIPv4Input:
                mutatedRanges = ''
            else:
                for IP in parsedIPv4Input:
                    mutatedRanges = mutatedRanges + str(IP) + '\n'
               # mutatedRanges = str(parsedIPv4Input)
            if ( parsedIPv4Input and parsedIPv6Input):
                mutatedRanges = mutatedRanges + '\n'
            if not parsedIPv6Input:
                mutatedRanges = mutatedRanges + ''
            else:
                for IP in parsedIPv6Input:
                    mutatedRanges = mutatedRanges + str(IP) + '\n'
            mutatedRanges = mutatedRanges[:-1]
            if (not parsedIPv6Input and not parsedIPv4Input):
                mutatedRanges = ''
            # Put it back in a new form.
            
            form = RangeForm({
                    'ranges': mutatedRanges
            })
            if parsedIPv4Input:
                output['IPv4'] =str( webcalc.calcIPv4Range(parsedIPv4Input[0],parsedIPv4Input[-1]))
                output['IPv4multi'] = str(webcalc.maxsizecalcIPv4(parsedIPv4Input,12))
            if parsedIPv6Input:
                output['IPv6'] = str( webcalc.calcIPv6Range(parsedIPv6Input[0],parsedIPv6Input[-1]))
                output['IPv6multi'] = str(webcalc.maxsizecalcIPv6(parsedIPv6Input,48))
            if not ('IPv4' in output  or 'IPv6' in output):
                output['error'] = 'No valid input recieved! Input IPv4 Addresses & Ranges, and IPv6 Addresses only!'
    finaloutput = {'form':form, 'IPv4simple':output}
    return render(request, "index.html", finaloutput)

def IPv4output(request):
    form = RangeForm()
    if request.method == 'POST':
        form = RangeForm(request.POST)
        if form.is_valid():
            ranges = form.cleaned_data['ranges']
            parsedInput = webcalc.parseIPv4Input(ranges)
            IPv4Range=webcalc.calcIPv4Range(parsedInput[0],parsedInput[-1])
            output = {'output':str(IPv4Range)}
    return render(request, "index.html", {"output": "output"})
	
