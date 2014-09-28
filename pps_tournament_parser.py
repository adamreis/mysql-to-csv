#!/usr/bin/python

import sys
import os
import csv

def parse_sql_columns(sql_file):
    columns = []
    
    scraping = False
    for line in sql_file:
        if scraping:
            if 'ENGINE=' in line:
                break
            columns.append(line.split()[0][1:-1])

        if 'CREATE TABLE' in line:
            scraping = True

    return columns

def parse_sql_entries(sql_file):
    entries = []

    for line in sql_file:
        if 'INSERT INTO' in line:
            start = line.find('(') + 1
            end = line.find(';') - 1
            for entry in line[start:end].strip().split('),('):
                entries.append(entry.split(','))
            break

    return entries

def write_csv(columns, rows, name):
    with open(name, 'wb') as csv_file:
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        wr.writerow(columns)
        for row in rows:
            wr.writerow(row)

def usage():
    print """
    usage:

        ./tournament_parser.py <path/to/tournament/sql/file.sql> <output_name.csv>
    """

if __name__ == '__main__':
    if len(sys.argv) != 3 or os.path.splitext(sys.argv[1])[1] != '.sql':
        usage()
        sys.exit(2)

    with open(sys.argv[1]) as sql_file:
        columns = parse_sql_columns(sql_file)
        entries = parse_sql_entries(sql_file)
        write_csv(columns, entries, sys.argv[2])