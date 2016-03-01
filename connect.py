import socket
import socks
import ssl
import time
import sys

from multiprocessing import Process
from thread import start_new_thread as Thread

class Con:
	
	def __init__( self , host , port , s , master , channel, nick ):
		self.errors = []
		self.functions = { "join" : self.join, "part" : self.part, "msg" : self.send_chan , "pewpewpew": self.spam}
		self.trigger = '!'
		self.host = host
		self.port = port
		self.master = master
		self.channel = channel
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
		socket.socket = socks.socksocket
		self.socket = socket.socket()
		self.s = s
		self.connect( nick )

	def connect( self , nick ):
		
		for i in xrange(3):

			try:
				self.socket.connect( ( self.host, self.port ) )
				if self.s == 1: 
					self.socket = ssl.wrap_socket( self.socket )
				#	print "using ssl"
				self.ident( nick )
				break
			except socket.error, e:

				self.log( e )
				continue
	def ident( self , nick ):
		user = "{} ".format(nick) * 4

		self.snick( nick )
		self.send( "USER {} ".format(user)  )


		data = self.recv()
		while data is not None:

			cmd = data.split(" ")
			if '433' in data:
				self.log( "[!] Nick already in use" )
				nick += '_'
				self.snick( nick )
			elif '004' in data:
				self.join( self.channel )
				self.log( "[+] Identified" )
				#print "Identified"
				break
			if 'PING' in data:
				self.pong( cmd[1] )
			#print data
			data = self.recv()
		self.main()
	def main( self ):
		spam = 0
		who = ''
		data = self.recv()
		while data is not None:
			cmd = data.split(' ')
			if 'PING' in data:
				self.pong( cmd[1] )
			try:
				command = cmd[3].strip( ':{}'.format(self.trigger) )
				self.functions[command](data.split(cmd[3])[1:][0].split()) #when you're too lazy to regex
			except Exception, e: pass#print e.message
			data = self.recv()
	def log( self , error ):
		
		self.errors.append( error )
	def send( self , data ):

		self.socket.send( "%s\r\n" % data )
	def recv( self ):
		
		return self.socket.recv( 4096 )
	def snick( self, nick ):

		self.send( "NICK {}".format( nick ) )
	def send_chan( self , chan , data ):
		
		#print ( "PRIVMSG {} : {}\r\n".format( chan[0], data ) )
		self.send( "PRIVMSG {} : {}\r\n".format( chan[0], data ) )

	def join( self, chan):

		if type(chan) != type('stringssssss'):
			for i in chan:
				self.send( "JOIN {}".format( i ) )
		else:
			self.send( "JOIN {}".format( chan ) )
	def part( self, chan , msg):

		self.send( "PART {} {}".format( chan, msg) )
	def pong( self, pong ):

		self.send("PONG {}".format( pong ) )
	def spam( self, who ):
		print "Spamming %s"  % who[0]
		for i in range(10):
			self.send_chan( who , "A" *10)
		return

			


