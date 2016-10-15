#!/usr/bin/env python3

import argparse
import os
import re
import sys

ver = '1.0'

def main():

    # First check user has root privileges
    if os.geteuid() != 0:
        exit('Need to have root privileges to run this script!')

    # Construct an arg parser
    parser = argparse.ArgumentParser(description = 'This is a utility script \
             for parsing pacman mirrorlists and enabling all mirrors within \
             a given section (e.g \'Worldwide, United States\')')

    # Configure the parser
    parser.add_argument('-v', '--version', action = 'version',
                        version = ver)

    parser.add_argument('-f', '--filter', dest = 'filter',
                        help = 'Filter for which sections in the mirrorlist \
                        to uncomment.  To select multiple sections, separate \
                        with a comma.  e.g \'France,United Kingdom,Germany\' \
                        (default = Worldwide)', default = 'Worldwide')

    parser.add_argument('-i', '--input', dest = 'in_file', required = False,
                        help = 'Location of input file to parse, e.g \
                        /etc/pacman.d/mirrorlist.pacnew (default)',
                        default = '/etc/pacman.d/mirrorlist.pacnew')
    
    parser.add_argument('-o', '--output', dest = 'out_file', required = False,
                        help = 'Location of output file to write, e.g \
                        /etc/pacman.d/mirrorlist (default)',
                        default = '/etc/pacman.d/mirrorlist')

    # Grab the arguments
    args = parser.parse_args()

    # Compose the filter list
    filter_list = args.filter.split(',')
    for idx, section in enumerate(filter_list):
        filter_list[idx] = '## ' + section.strip()
    
    # Open files
    try:
        in_file = open(args.in_file, 'r')
    except FileNotFoundError:
        print('Couldn\'t open input file %s!' % args.in_file)
        exit()
    try:
        out_file = open(args.out_file, 'w')
    except FileNotFoundError:
        print('Couldn\'t open output file %s!' % args.out_file)
        exit()
    
    # Loop over each line looking for the filter entries
    enable_mirror = False
    for line in in_file:
        out_line = line

        # Look for section headers and check against the filter
        if re.search('##', line):
            enable_mirror = False
            for filter in filter_list:
                if re.search(filter, line):
                    enable_mirror = True
                    print('Mirror enabled')

        # Strip comments if we are enabled and update out line
        elif enable_mirror:
            out_line = line.strip('#')

        # Write out the result
        out_file.write(out_line)
        
    in_file.close()
    out_file.close()
    

if __name__ == '__main__':
    main()
