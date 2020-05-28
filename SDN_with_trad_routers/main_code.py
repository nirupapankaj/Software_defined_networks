from netmiko import ConnectHandler
import re
import pexpect
import time
import threading
import graph_code as pgraph


#Code to get leased ip address from R1
print('\n')
print('*** ssh into R1 and get IP address leased to the Mininet VM ***')
device_R1 = {
	'device_type':'cisco_ios',
	'username':'lab',
	'password':'lab123',
	'ip':'192.168.100.1'
		}
net_connect = ConnectHandler(**device_R1)
output = net_connect.send_command('sh ip dhcp binding')
output2 = re.findall('\d+\.\d+\.\d+\.\d+',output)
print('\n')
print("IP address leased to the mininet VM is %s" %output2[0])


#Code to ssh into mininet and initialize default mininet topology
print('\n')
print('*** ssh into mininet and initializing default mininet topology ***')
user = 'mininet'
ip = output2[0]
passw = 'mininet'
ssh = pexpect.spawn('ssh %s@%s' %(user,ip))
try:
	user_ssh = '%s@%s' %(user,ip)
	texts = user_ssh + '\'s' + ' ' + 'password:'
	i = ssh.expect([texts, 'continue connecting (yes/no)?'],timeout=30)
	if i == 0:
		ssh.sendline(passw)
	elif i == 1:
		ssh.sendline('yes')
		ssh.expect(texts)
		ssh.sendline(passw)
	ssh.expect('@.*\$')
	print(ssh.before.decode("utf-8") + ssh.after.decode("utf-8"))
	cmd = 'sudo mn --switch=ovsk,protocols=OpenFlow13'
	ssh.sendline(cmd)
	ssh.sendline(passw)
	#ssh.expect('.*\CLI:')
	ssh.expect('mininet>')
	print(ssh.before.decode("utf-8") + ssh.after.decode("utf-8"))

except pexpect.EOF:
	print("EOF")
except pexpect.TIMEOUT:
	print('TIMEOT')


#Code to configure OVS on Mininet to connect to the conntroller
print('\n')
print('*** Configuring OVS on Mininet to connect to the controller ***')
print('\n')
print('New ssh session to the mininet VM')
user = 'mininet'
ip = output2[0]
passw = 'mininet'
ssh_new = pexpect.spawn('ssh %s@%s' %(user,ip))
try:
	user_ssh_new = '%s@%s' %(user,ip)
	texts = user_ssh_new + '\'s' + ' ' + 'password:'
	i = ssh_new.expect([texts, 'continue connecting (yes/no)?'],timeout=30)
	if i == 0:
		ssh_new.sendline(passw)
	elif i == 1:
		ssh_new.sendline('yes')
		ssh_new.expect(texts)
		ssh_new.sendline(passw)
	ssh_new.expect('@.*\$')
	print(ssh_new.before.decode("utf-8") + ssh_new.after.decode("utf-8"))
	connect_to_the_controller = 'sudo ovs-vsctl set-controller s1 tcp:10.20.30.2:6653'
	ssh_new.sendline(connect_to_the_controller)
	ssh_new.sendline(passw)
	ssh_new.expect('@.*\$')
	print(ssh_new.before.decode("utf-8") + ssh_new.after.decode("utf-8"))
	get_controller = 'sudo ovs-vsctl get-controller s1'
	ssh_new.sendline(get_controller)
	ssh_new.expect('.*\:6653')
	print(ssh_new.after.decode("utf-8"))

except pexpect.EOF:
	print("EOF")
except pexpect.TIMEOUT:
	print('TIMEOT')


#Code to ssh into all routers and configure routing
print('\n')
print('*** SSH into all routers and configure OSPF to achieve full connectivity ***')
device_R1 = {
	'device_type':'cisco_ios',
	'username':'lab',
	'password':'lab123',
	'ip':'192.168.100.1'
		}
net_connect = ConnectHandler(**device_R1)
config_set = ['router ospf 1', 'network 192.168.100.0 0.0.0.255 area 0', 'network 192.168.200.0 0.0.0.255 area 0']
output = net_connect.send_config_set(config_set)
print(output)
net_connect.send_config_set(['exit'])

#ssh into R2 from R1
net_connect.write_channel('ssh -l lab 192.168.200.2\n')
time.sleep(1)
out = net_connect.read_channel()
print(out)
if 'ssword' in out:
	net_connect.write_channel('lab123\n')
	time.sleep(1)
out = net_connect.read_channel()
print(out)
net_connect.write_channel('conf t\n')
time.sleep(1)
print(net_connect.read_channel())
config_set1 = ['router ospf 1', 'network 172.16.100.0 0.0.0.255 area 0', 'network 192.168.200.0 0.0.0.255 area 0']
output1 = net_connect.send_config_set(config_set1)
print(output1)
net_connect.write_channel('exit\n')
time.sleep(1)
print(net_connect.read_channel())

#ssh into R3 from R1
net_connect.write_channel('ssh -l lab 172.16.100.1\n')
time.sleep(1)
out = net_connect.read_channel()
print(out)
if 'ssword' in out:
	net_connect.write_channel('lab123\n')
	time.sleep(1)
out = net_connect.read_channel()
print(out)
net_connect.write_channel('conf t\n')
time.sleep(1)
print(net_connect.read_channel())
config_set2 = ['router ospf 1', 'network 172.16.100.0 0.0.0.255 area 0', 'network 10.20.30.0 0.0.0.255 area 0']
output2 = net_connect.send_config_set(config_set2)
print(output2)

#Code to verify successful connection between the switch and the controller
print('New ssh session to the mininet VM')
print('*** ssh into mininet and verify conncetivity between OVS and controller ***')
user = 'mininet'
ip = output2[0]
#ip = '192.168.100.3'
passw = 'mininet'
ssh_new = pexpect.spawn('ssh %s@%s' %(user,ip))
try:
	user_ssh_new = '%s@%s' %(user,ip)
	texts = user_ssh_new + '\'s' + ' ' + 'password:'
	i = ssh_new.expect([texts, 'continue connecting (yes/no)?'],timeout=30)
	if i == 0:
		ssh_new.sendline(passw)
	elif i == 1:
		ssh_new.sendline('yes')
		ssh_new.expect(texts)
		ssh_new.sendline(passw)
	ssh_new.expect('@.*\$')
	print(ssh_new.before.decode("utf-8") + ssh_new.after.decode("utf-8"))
	show_controller = 'sudo ovs-vsctl show'
	ssh_new.sendline(show_controller)
	ssh_new.sendline(passw)
	ssh_new.expect('.*\-eth2"')
	output_new = ssh_new.after.decode("utf-8")
	print(output_new)
	output2 = re.findall('is_connected: true',output_new)
	print('\n')
	if output2[0]:
		print('Successful connection between the OVS and the controller')
	
except pexpect.EOF:
	print("EOF")
except pexpect.TIMEOUT:
	print('TIMEOT')

#Code to get the number of packet_in messages and tp plot a graph for the same
print('\n')
print('*** Get number of packet_in messages and plot graph on the webpage for the same ***')
def tshark_mininet():
	global val
	device_mininet = {
        'device_type':'linux',
        'username':'mininet',
        'password':'mininet',
        'ip':'192.168.100.3'
                }
	net_connect = ConnectHandler(**device_mininet)
	net_connect.send_command_timing('sudo -i')
	net_connect.send_command_timing('mininet')
	while True:
		net_connect.send_command_timing('sudo dumpcap -i eth1 -d tcp.port==6653,openflow -a duration:10 -w est.pcap')
		#time.sleep(10)
		net_connect.send_command_timing("sudo tshark -r est.pcap -Y 'openflow_v4.type == 10' > test.pcap")
		output = net_connect.send_command_timing('wc -l test.pcap')
		#print(output)
		final_output = re.findall('\d+',output)
		val = final_output[0]
		pgraph.X_axis.append(pgraph.X_axis[-1]+5)
		pgraph.Y_axis.append(int(val))
		
t1 = threading.Thread(target=tshark_mininet)
t1.start()
#pgraph is the python webpage file build using dash
pgraph.app.run_server(debug=False)
