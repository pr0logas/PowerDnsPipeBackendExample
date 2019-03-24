#!/usr/bin/python -u
##: Author: Tomas Andriekus
##: 2019-03-24
##: pdns backend collects data from JSON API and flushes to daemon

from sys import stdin, stdout, stderr
import requests

# Parse real time data
url = "https://task.forcandidate.com"
r = requests.get(url)
json = r.json()

sorted_data = sorted(json, key=lambda x: x['util'], reverse=False) # Sorted data by util

# Start pdns
data = stdin.readline()
stdout.write("OK\tCC DNS Backend\n")
stdout.flush()

stderr.write("$$$ Main loop started...\n")

while True:
    line = stdin.readline().strip()

    kind, qname, qclass, qtype, id, ip, mask = line.split('\t')

    if kind == 'Q':
        stderr.write('$$$ Got request ' + qname + "\n")  
        stderr.write(line)
        if qtype != 'SOA':
            r1 = "DATA\t"+sorted_data[0]['server']+"\t"+qclass+"\t" + "A" + "\t3600\t"+id+"\t"+sorted_data[0]['ip']+"\n"
            r2 = "DATA\t"+sorted_data[1]['server']+"\t"+qclass+"\t" + "A" + "\t3600\t"+id+"\t"+sorted_data[1]['ip']+"\n"
            r3 = "DATA\t"+sorted_data[2]['server']+"\t"+qclass+"\t" + "A" + "\t3600\t"+id+"\t"+sorted_data[2]['ip']+"\n"
            stderr.write(r1 + r2 + r3)
            stdout.write(r1 + r2 + r3)
        else:
            stderr.write("$$$ Sending SOA\n")
            r = "DATA\tforcandidate.com\tIN\tSOA\t86400\t1\tvpntask7.taskforcandidate.com server.vpntask7.forcandidate.com 2008080300 1800 3600 604800 3600\n"
            stdout.write(r)
            stderr.write(r)

        stdout.write("END\n")
        stderr.write("END\n")
        stdout.flush()
