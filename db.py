#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
from blocktools import *

db = MySQLdb.connect("localhost", "root", "", "ana_tx")
cursor = db.cursor()
# 打开数据库连接
class Publickey:

    def __init__(self,public_key="",public_hash="",address=""):

        self.public_key = public_key
        self.public_hash = public_hash
        self.address = address

    def save(self):
        sql = "insert into pk(pk,pk_hash_160,address) value(%s,%s,%s)"
        m1 = (self.public_key, self.public_hash, self.address)
        cursor.execute(sql, m1)
        res = int(cursor.lastrowid)
        db.commit()
        return res

    def getIdByHash(self,shash):
        sql = " select * from pk where pk_hash_160 ='" + str(shash)+"'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result==None:
            return 0
        return result[0]

class Transaction:

    def __init__(self,transaction_hash="",vin=0,vout=0,times=0):
        self.transaction_hash = transaction_hash
        self.vin = vin
        self.vout = vout
        self.times = times

    def save(self):
        sql = "insert into tx(tx_hash,vin,vout,times) value(%s,%s,%s,%s)"
        m1 = (self.transaction_hash, self.vin, self.vout,self.times)
        cursor.execute(sql, m1)
        res=int(cursor.lastrowid)
        db.commit()
        return res

    def getIdByHash(self, txhash):
        sql = " select * from tx where tx_hash ='" + str(txhash)+"'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None:
            return 0
        return result[0]


class Edges:

    def __init__(self,transaction_id,pk_id,type,value,index=-1):

        self.transaction_id = transaction_id
        self.pk_id = pk_id
        self.type = type
        self.value = value
        self.index = index

    def save(self):

        sql = "insert into edges(tx_id,pk_id,type,value,idx) value(%s,%s,%s,%s,%s)"
        m1 = (self.transaction_id, self.pk_id, self.type,self.value,self.index)
        cursor.execute(sql, m1)
        res = int(cursor.lastrowid)
        db.commit()
        return res


    def getOutByTxid(self, txid,index):
        sql = " select * from edges where tx_id =" + txid +" and tpye = 2 and index=" +index
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None:
            return 0
        return result

def save2db(block):
    for tx in block.Txs:
        # 1 save transaction
        item_tx = Transaction(tx.txid,tx.inCount,tx.outCount,block.blockHeader.time)
        # the tx exist, have been saved, continue

        tx_id = item_tx.getIdByHash(str(tx.txid))
        if tx_id != 0:
            continue

        tx_id=item_tx.save()

        # save edges
        # 2 save output type=2 index mean order in outputs
        count = 0
        for vout in tx.outputs:
            pk = Publickey("",hashStr(vout.pubkey))
            pk_id = pk.getIdByHash(hashStr(vout.pubkey))
            if pk_id == 0:
                pk_id == pk.save()
            edge = Edges(tx_id,pk_id,2,vout.value,count)
            edge.save()
            count +=1

        # 3 save Input type = 1
        for vin in tx.inputs:
            if vin.txOutId == 4294967295: #coinbase  txOutid ffffffff
                edge = Edges(tx_id, 0, 1, -1)
                edge.save()
            # todo output save miners address
            else:
                # todo order read file , query the table edges index which links to input
                # 查询数据库获得对应的输出 得到金额
                print "^"*50
                print hashStr(vin.prevhash)
                pre_tx_id = item_tx.getIdByHash(hashStr(vin.prevhash))
                if pre_tx_id!=0:
                    edge_tmp = Edges(tx_id, 0, 1, -1)
                    out_edge = edge_tmp.getOutByTxid(pre_tx_id)
                    # 查找到对应的output
                    if not out_edge:
                        in_edge =  Edges(tx_id,out_edge.pk_id,1,out_edge.value)
                    else:
                        # 未找到
                        in_edge =  Edges(tx_id,-1,1,-1)
                    in_edge.save()

    return 0


if __name__ == '__main__':
    # pk = Publickey("","tttt")
    #
    # print pk.getIdByHash("3333")
    # item_tx = Transaction("sdfasiodjfo", 1, 1, 100922)
    # # the tx exist, have been saved, continue
    # s = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
    # tx_id = item_tx.getIdByHash(s)
    # print tx_id
    edge = Edges(1,1,2,11,0)
    print edge.save()
