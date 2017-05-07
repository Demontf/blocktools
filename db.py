#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

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
        sql = " select * from pk where pk_hash_160 =" + str(shash)
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
        sql = " select * from tx where tx_hash =" + str(txhash)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None:
            return 0
        return result[0]


class Edges:

    def __init__(self,transaction_id,pk_hash,type,vaule,index=-1):

        self.transaction_id = transaction_id
        self.pk_hash = pk_hash
        self.type = type
        self.vaule = vaule
        self.index = index

    def save(self):

        sql = "insert into edges(tx_id,pk_id,type,vaule,index) value(%s,%s,%s,%s,%s)"
        m1 = (self.transaction_id, self.pk_hash, self.type,self.vaule,self.index)
        cursor.execute(sql, m1)
        res = int(cursor.lastrowid)
        db.commit()
        return res

def save2db(block):
    for tx in block.Txs:
        # 1 save transaction
        # todo write function to calc tx_hash
        tx_hash = ""
        item_tx = Transaction(tx_hash,tx.inCount,tx.outCount,block.blockHeader.time)
        # the tx exist, have been saved, continue
        tx_id = Transaction.getIdByHash(tx_hash)
        if tx_id != 0:
            continue

        tx_id=item_tx.save()

        # save edges
        # 2 save output type=2
        count = 0;
        for vout in tx.outputs:
            pk = Publickey("",vout.pubkey)
            pk_id = pk.getIdByHash(vout.pubkey)
            if pk_id == 0:
                pk_id == pk.save()
            edge = Edges(tx_id,pk_id,2,vout.value,count)
            edge.save()
            count +=1

        # 3 save Input type = 1
        for vin in tx.inputs:
            if vin.txOutId == 'ffffffff': #coinbase
                edge = Edges(tx_id, 0, 1, -1)
                edge.save()
            # todo order read file , query the table edges index which links to input
    return 0


if __name__ == '__main__':
    pk = Publickey("","tttt")
    print pk.getIdByHash("3333")

db.close()