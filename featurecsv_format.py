#!/usr/bin/python

import os
import sys
import csv

if __name__=="__main__":
    filename = sys.argv[1]
    out_filename = filename.rsplit('.',1)[-2] +"_out.csv"
    print filename, out_filename
    with open(filename, "r") as input_file, open (out_filename, "w+") as output_file:
        input_reader = csv.reader(input_file, quoting=csv.QUOTE_NONE)
        output_writer = csv.writer(output_file, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        for line in input_reader:
            if len(line) == 25:
                new_line = []
                for s in line:
                    if s != '"?"':
                        new_line.append(s)
                    else:
                        ss = s.replace('"', '')
                        new_line.append(ss)
                output_writer.writerow(new_line)
            else:
                pass
    output_file.close()
    input_file.close()
