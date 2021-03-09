from __future__ import absolute_import, print_function, unicode_literals
import subprocess, sys
import os
import requests
import argparse
import audioop
import json
import math
import multiprocessing
import os
import requests
import subprocess
import sys
import tempfile
import wave
import re
def percentile(arr, percent):
    arr = sorted(arr)
    k = (len(arr) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c: return arr[int(k)]
    d0 = arr[int(f)] * (c - k)
    d1 = arr[int(c)] * (k - f)
    return d0 + d1
def speech_regions(filename, frame_width=4096, min_region_size=0, max_region_size=6):
    reader = wave.open(filename)
    print ("--->inside speech",reader)
    sample_width = reader.getsampwidth()
    rate = reader.getframerate()
    n_channels = reader.getnchannels()
    chunk_duration = float(frame_width) / rate

    n_chunks = int(math.ceil(reader.getnframes()*1.0 / frame_width))
    energies = []

    for i in range(n_chunks):
        chunk = reader.readframes(frame_width)
        energies.append(audioop.rms(chunk, sample_width * n_channels))

    threshold = percentile(energies, 0.1)

    elapsed_time = 0

    regions = []
    region_start = None
    #print energies
    for energy in energies:
        
        is_silence = energy <= threshold
        max_exceeded = region_start and elapsed_time - region_start >= max_region_size

        if (max_exceeded or is_silence) and region_start:
           # print energy
            if elapsed_time - region_start >= min_region_size:
                regions.append((region_start, elapsed_time))
                #print regions,"region"
                region_start = elapsed_time

        elif (not region_start) and (not is_silence):
            #print elapsed_time,"elasped_start"
            region_start = elapsed_time
            #print region_start,"start"
        elapsed_time += chunk_duration
    return regions
