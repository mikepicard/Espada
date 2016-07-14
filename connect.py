import socket
import socks
import ssl
import time
import sys

from multiprocessing import Process
from thread import start_new_thread as Thread

class Con:
	
	def __init__( self , host , port , s , master , channel, nick ):
		self.functions 	= { "join" : self.join, "part" : self.part, "msg" : self.send_chan , "pewpewpew": self.spam, "stahp": self.stahp}
		self.trigger 	= '!'
		self.host 		= host
		self.port 		= port
		self.master 	= master
		self.channel 	= channel
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
		socket.socket 	= socks.socksocket
		self.socket 	= socket.socket()
		self.s 			= s
		self.spam 		= 0
		self.who		= None
		self.connect( nick )

	def connect( self , nick ):
		
		for i in xrange(3):

			try:
				self.socket.connect( ( self.host, self.port ) )
				if self.s == 1: 
					self.socket = ssl.wrap_socket( self.socket )
				self.ident( nick )
				break
			except socket.error, e:
				continue
	def ident( self , nick ):
		user = "{} ".format(nick) * 4

		self.snick( nick )
		self.send( "USER {} ".format(user)  )


		data = self.recv()
		while data is not None:

			cmd = data.split(" ")
			if '433' in data:
				nick += '_'
				self.snick( nick )
			elif '004' in data:
				self.join( self.channel )
				break
			if 'PING' in data:
				self.pong( cmd[1] )

			data = self.recv()
		self.main()
	def main( self ):
		data = self.recv()
		while data is not None:
			cmd = data.split(' ')
			if 'PING' in data:

				self.pong( cmd[1] )
			try:

				command = cmd[3].strip( ':{}'.format(self.trigger) )
				self.functions[command](data.split(cmd[3])[1:][0].split()) #when you're too lazy to regex
				continue

			except Exception, e:
				pass
			if self.spam is 1 and self.who is not None:
				time.sleep( 5 )
				self.spam( self.who )
			data = self.recv()

	def send( self , data ):

		self.socket.send( "%s\r\n" % data )
	def recv( self ):
		
		return self.socket.recv( 4096 )
	def snick( self, nick ):

		self.send( "NICK {}".format( nick ) )
	def send_chan( self , chan , data ):
	
		self.send( "PRIVMSG {} : {}\r\n".format( chan[0], data ) )
	def join( self, chan):

		if type(chan) is not str:
			for i in chan:
				self.send( "JOIN {}".format( i ) )
		else:
			self.send( "JOIN {}".format( chan ) )
	def part( self, chan , msg):

		self.send( "PART {} {}".format( chan, msg) )
	def pong( self, pong ):

		self.send("PONG {}".format( pong ) )
	def stahp( self ):
		self.who = None
		self.spam = 0 
        
        def spam( self, who ):
                if self.spam is 0: self.spam    = 1
                if self.who is None: self.who   = who
                
                fg = [
                    "31", "32", "33", "34", "35", 
                    "36", "37", "90", "91", "92", 
                    "93", "94", "95", "96", "97"
                ]

                bg = [
                    "40m", "41m", "42m", "43m", "44m",
                    "45m", "46m", "47m", "100m", "101m",
                    "102m", "103m", "104m", "105m", "106m"
                ]

                text = "\033[{};{}{}\033[0m".format( choice( fg ), choice( bg ), "GOTTA CATCH THEM ALL " * 10 )

                for i in xrange(10):
                        self.send_chan( who , text )
                time.sleep( 3 )
                return


			


