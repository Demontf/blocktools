import struct
from sys import byteorder
from hashlib import sha256
import chardet

def uint1(stream):
	return ord(stream.read(1))

def uint2(stream):
	# unsign short
	return struct.unpack('H', stream.read(2))[0]

def uint4(stream):
	# unsign int
	return struct.unpack('I', stream.read(4))[0]

def uint8(stream):
	# unsign long long
	return struct.unpack('Q', stream.read(8))[0]

def hash32(stream):
	return stream.read(32)[::-1]

def time(stream):
	time = uint4(stream)
	return time

def varint(stream):
	size = uint1(stream)

	if size < 0xfd:
		return size
	if size == 0xfd:
		return uint2(stream)
	if size == 0xfe:
		return uint4(stream)
	if size == 0xff:
		return uint8(stream)
	return -1

def hashStr(bytebuffer):
	return ''.join(('%02x'%ord(a)) for a in bytebuffer)

def txhex(stream,length):
	return hashStr(stream.read(length))




def hex2hash(str):
	#print chardet.detect(str)
	str = str.decode("hex")
	hash = sha256(sha256(str).digest()).digest()
	#Internal-Byte-Order Hash
	iboh = hash.encode('hex_codec')
	#print iboh
	#RPC-Byte-Order Hash
	rboh = hash[::-1].encode('hex_codec')
	#print rboh
	return rboh

# if __name__ == '__main__':
# 	str = "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff0704ffff001d0102ffffffff0100f2052a01000000434104d46c4968bde02899d2aa0963367c7a6ce34eec332b32e42e5f3407e052d64ac625da6f0718e7b302140434bd725706957c092db53805b821a85b23a7ac61725bac00000000"
# 	hex2hash(str)