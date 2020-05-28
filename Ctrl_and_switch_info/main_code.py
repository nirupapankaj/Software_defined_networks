import time
from scapy.all import *
import subprocess
import re
import json

#Running tcpdump over the terminal
output = subprocess.Popen(['sudo','tcpdump','-i','enp0s8','port','6653','-w','lab3.pcap','-c','200'], stdout=subprocess.PIPE)
time.sleep(10)

load_contrib('openflow3')
lis_ip = []
lis_status = []
lis_port = []

#Code to verify and display the connection between the sontroller and the switch
packet = rdpcap('lab3.pcap')
for i in range(len(packet)):
	if packet[i]['IP'].src == '192.168.56.105':
		p = packet[i].show(dump=True)
		if re.findall('OFPT_HELLO',p):
			lis_ip.append(packet[i]['IP'].dst)
			lis_status.append('connected')
			lis_port.append(packet[i]['TCP'].dport)

if len(lis_ip) > 0:
	for i in range(len(lis_ip)):
		print("connection is successful for the switch with ip %s and port %s") %(lis_ip[i],lis_port[i])

else:
	print('No connections established between any of the switches and the controller')

print(' ------------------------------------------------------------------------- ')

#Code to print out the dpid of the switches
ovs1 = {}
dpid = {}
load_contrib('openflow3')
packet = rdpcap('lab3.pcap')
print('Printing out switches info in json format')
for i in range(len(packet)):
	#if packet[i]['IP'].src == '192.168.56.106':
	p1 = packet[i].show(dump=True)
	if re.findall('OFPT_FEATURES_REPLY',p1):
		data_id = packet[i]['OFPTFeaturesReply'].datapath_id
		src_port = packet[i]['TCP'].sport
		ind = lis_port.index(src_port)
		ovs1['ip_address'] = lis_ip[ind]
		ovs1['status'] = lis_status[ind]
		dpid[data_id] = ovs1
print(dpid)
with open('connected.txt', 'w') as json_dpid:
	json.dump(dpid, json_dpid)
