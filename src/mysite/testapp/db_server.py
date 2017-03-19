import logging,socket,json,fcntl,struct,sys,time,thread
from kazoo.client import KazooClient

logging.basicConfig()

zk=KazooClient(hosts="172.17.0.2:2181")
zk.start()
leader = None
db_data = ["Apple","Google","Microsoft","Quora","Uber"]

def elect_leader():
	nodes = zk.get_children(path="/zk-test/leader_election")
	nodes.sort()
	if len(nodes) > 0:
		return nodes[0]
	return None



def serve_request(args):
	print "DB thread started...."
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.bind((get_ip(),6000))
	sock.listen(10)
	while True:
		con,addr = sock.accept()
		request = con.recv(1024)
		print "Request Received: %s " % request
		request = request.split(" ")
		if request[0] == "read":
			con.send(db_data[int(request[1])] + " from " + get_ip())
		elif request[0] == "write":
			db_data[int(request[1])] = request[2]
			nodes = zk.get_children(path="/zk-test/leader_election")
			args = [nodes,request[1],request[2]]
			thread.start_new_thread(synchronise,(args,))


		#con.close()
def synchronise(args):
	print "Synchronise Thread Started..."
	ip = get_ip()
	if args is not None:
		print "Sending other instances update message..."
		for node in args[0]:
			sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			data,stat = zk.get(path="/zk-test/leader_election/" + node)
			print "sending to %s " % data
			if ip != data:
				sock.sendto(str(args[1] + " " + args[2]),(data,7000))
	else:
		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		sock.bind((ip,7000))
		while True:
			print "Wating for synchronise request..."
			data,addr = sock.recvfrom(128)
			data = data.split(" ")
			global db_data
			db_data[int(data[0])] = data[1]


def get_ip():
	return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
	
thread.start_new_thread(synchronise,(None,))
zk_node_value = str(get_ip())
zk_node_name=zk.create("/zk-test/leader_election/db",sequence=True,ephemeral=True,makepath=True,value=zk_node_value)
print "Node Value %s" % zk_node_name

leader = elect_leader()

print "Leader: %s " % leader
data,stat = zk.get(path="/zk-test/leader_election/"+leader)
print "Leader Data: %s " % data

@zk.ChildrenWatch("/zk-test/leader_election/")
def watch_children(children):
	children.sort()
	global leader
	leader = children[0]
	print "New Leader: %s " % leader
	data,stat = zk.get(path="/zk-test/leader_election/"+leader)
	print "New Leader Data: %s " % data

thread.start_new_thread(serve_request,(None,))

while True:
	print "Type Command: "
	cmd = raw_input()
	if cmd == "exit":
		zk.stop()
		sys.exit(0)