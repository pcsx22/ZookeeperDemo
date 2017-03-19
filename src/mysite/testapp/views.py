from django.http import HttpResponse
from kazoo.client import KazooClient
import logging,socket,random

logging.basicConfig()
zk = KazooClient(hosts='172.17.0.2:2181')
zk.start()
db_servers=[]

@zk.ChildrenWatch("/zk-test/leader_election")
def watch_children(children):
	print "Change in the node....."
	global db_servers
	children.sort()
	db_servers = children

def index(request):
    data, stat = zk.get("/zk-test/hawa")
    l.append(1)
    print l
    return HttpResponse("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
    #return HttpResponse("<p>Hello, world. You're at the polls index.</p>")

def read(request,id):
	if db_servers is None or len(db_servers) == 0:
		return HttpResponse("All database servers are down. Please try again later")
	db_server = db_servers[random.randint(0, len(db_servers) - 1)]
	db_ip,stat = zk.get("/zk-test/leader_election/" + db_server)
	print "DB server selected: %s" % db_ip
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((db_ip,6000))
	sock.send("read " + str(id))
	data = sock.recv(128)
	return HttpResponse("You Requested: %s" % data)

def update(request,id,value):
	if db_servers is None or len(db_servers) == 0:
		return HttpResponse("All database servers are down. Please try again later")
	db_server = db_servers[0]
	db_ip,stat = zk.get("/zk-test/leader_election/" + db_server)
	print "DB server selected: %s" % db_ip
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((db_ip,6000))
	sock.send("write " + str(id) + " " + value)
	return HttpResponse("Your Value changed...")