from django.shortcuts import render

from calculator.forms import RangeForm

import sys
import os
scriptpath = '../combinedcalc.py'

sys.path.append(os.path.abspath(scriptpath))

import combinedcalc

# Create your views here.

def index(request):
    form = RangeForm()
    if request.method == 'POST':
        form = RangeForm(request.POST)
        if form.is_valid():
            ranges = form.cleaned_data['ranges']
            # do something to it!
            mutatedRanges = combinedcalc.parseIPv4Input(ranges)
            # Put it back in a new form.
            form = RangeForm({
                    'ranges': mutatedRanges
            })
    return render(request, "index.html", {"form": form})

