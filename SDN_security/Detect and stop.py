import subprocess
import re
from scapy.all import *
from scapy.contrib import openflow as of


def detect_attack(src_ip, src_port):
        pkt_ins = 0
	cmd = ['sudo', 'tcpdump','-i','enp0s8','src',src_ip,'-w','output.pcap','-c','300']
	time.sleep(5)
	load_contrib('openflow3')
        while True:
                output = (subprocess.check_output(cmd)).decode('utf-8')
                packets=rdpcap('output.pcap')
		for i in range(len(packets)):
                	if packets[i]['IP']:
                        	pkt=packets[i].show(dump=True)
                        	if re.findall('OFPT_PACKET_IN',pkt):
                                	pkt_ins += 1
		if pkt_ins > 100:
                        return True

def stop_attack(src_ip, src_port):
	print("Adding IPtables rules to stop the attack")
	cmd = ['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '-s', src_ip, '-d', '192.168.56.105', '--dport', '6653', '--sport', src_port, '-j', 'DROP']
	out = (subprocess.check_output(cmd)).decode('utf-8')
	cmd1 = ['sudo', 'iptables', '-L', '-v']
	out1 = (subprocess.check_output(cmd1)).decode('utf-8')
	print("The IPtable rules after adding the drop rule to prevent attack are:")
	print(out1)
	reg_rule = '.*192.168.56.105.*tcp\\sspt:' + src_port + '\\sdpt:6653.*'
	stop_rule = re.search(reg_rule, out1)
	if stop_rule:
		dropped_packets = stop_rule.group().split()[0]
		print("Number of dropped packets are: %s" %dropped_packets)
	if dropped_packets > 0:
		print('Stopped attack by blocking/dropping packets from the IP %s' %src_ip)

if __name__ == "__main__":
        src_ip = '192.168.56.107'
        src_port = '41510'
       	if detect_attack(src_ip, src_port):
                print('Controller under attack')
		stop_attack(src_ip, src_port)
