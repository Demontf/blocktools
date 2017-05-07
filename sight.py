#!/usr/bin/python
import sys
from blocktools import *
from block import Block, BlockHeader
import db

def parse(blockchain):
	print 'print Parsing Block Chain'
	continueParsing = True
	counter = 0
	blockchain.seek(0, 2)
	fSize = blockchain.tell() - 80 #Minus last Block header size for partial file
	blockchain.seek(0, 0)
	while continueParsing:	
		block = Block(blockchain)
		continueParsing = block.continueParsing
		#db.save2db(block)
		if continueParsing:
			block.toString()
		counter+=1

	print ''
	print 'Reached End of Field'
	print 'Parsed %s blocks', counter

def main():
	# if len(sys.argv) < 2:
     #        print 'Usage: sight.py filename'
	# else:
	# 	with open(sys.argv[1], 'rb') as blockchain:
	# 		parse(blockchain)

	with open("1M.dat", 'rb') as blockchain:
		parse(blockchain)


if __name__ == '__main__':
	main()
