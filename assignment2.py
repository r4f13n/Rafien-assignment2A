#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: "Rafien Mohammed"
Semester: "Fall 2024"

The python code in this file is original work written by
"Rafien Mohammed". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: Rafien Mohammed Assignment 2 A 

'''

import argparse
import os, sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    # check the docs for an argparse option to store this as a boolean.
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use is not.")
    args = parser.parse_args()
    return args
# create argparse function
# -H human readable
# -r running only

def percent_to_graph(percent: float, length: int=20) -> str:
    "turns a percent 0.0 - 1.0 into a bar graph"
    num_hashes = int(percent * length)
    return "#" * num_hashes + " " * (length - num_hashes)
# percent to graph function

def get_sys_mem() -> int:
    "return total system memory (used or available) in kB"
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if line.startswith("MemTotal"):
                return int(line.split()[1]) # Extracts the value of MemTotal
    return 0

def get_avail_mem() -> int:
    "return total memory that is available"
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if line.startswith("MemAvailable"):
                return int(line.split()[1]) # Extracts the value of MemAvailable
    return 0

def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    pids = os.popen(f'pidof {app_name}').read().strip().split()
    return pids if pids else []

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    rss_mem = 0
    try:
        with open(f'/proc/{proc_id}/smaps', 'r') as f:
            for line in f:
                if 'Rss:' in line:
                    rss_mem += int(line.split()[1])
    except FileNotFoundError:
        pass
    return rss_mem


def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:
        total_mem = get_sys_mem()
        avail_mem = get_avail_mem()
        used_mem = total_mem - avail_mem
        used_percent = used_mem / total_mem
        graph = percent_to_graph(used_percent, args.length)
        if args.human_readable:
            total_mem = bytes_to_human_r(total_mem)
            used_mem = bytes_to_human_r(used_mem)
        print(f"Memory {graph} {int(used_percent * 100)}% {used_mem}/{total_mem}")
    else:
        pids = pids_of_prog(args.program)
        if not pids:
            print(f"{args.program} not found.")
            sys.exit()
        for pid in pids:
            rss = rss_mem_of_pid(pid)
            rss_percent = rss / get_sys_mem()
            graph = percent_to_graph(rss_percent, args.length)
            if args.human_readable:
                rss = bytes_to_human_r(rss)
            print(f"{pid:6} {graph} {rss}")
    # process args
    # if no parameter passed, 
    # open meminfo.
    # get used memory
    # get total memory
    # call percent to graph
    # print

    # if a parameter passed:
    # get pids from pidof
    # lookup each process id in /proc
    # read memory used
    # add to total used
    # percent to graph
    # take total our of total system memory? or total used memory? total used memory.
    # percent to graph.
