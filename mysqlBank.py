#-*- coding: utf-8 -*-
import pymysql
import sys

class TransferMoney(object):
	def __init__(self,conn):
		self.conn=conn
	def check_acct_available(self,acctid):
		cur = self.conn.cursor()
		try:
			
			sql = "SELECT * FROM account WHERE acctid=%s"%acctid
			cur.execute(sql)
			print("check_acct_available:"+sql)
			rs = cur.fetchall()
			if len(rs) != 1:
				raise Exception("acctid %s not exist"%acctid)
		finally:
			cur.close()
	def has_enough_money(self,acctid,money):
		cur = self.conn.cursor()
		try:
			
			sql = "SELECT * FROM account WHERE acctid=%s and money>%s"%(acctid,money)
			cur.execute(sql)
			print("has_enough_money:"+sql)
			rs = cur.fetchall()
			if len(rs) != 1:
				raise Exception("acctid %s has no enough money"%acctid)
		finally:
			cur.close()
	def reduce_money(self,acctid,money):
		cur = self.conn.cursor()
		try:
			
			sql = "UPDATE account set money=money-%s WHERE acctid=%s"%(money,acctid)
			cur.execute(sql)
			print("reduce_money:"+sql)
			if cur.rowcount != 1:
				raise Exception("acctid %s fail to reduce money"%acctid)
		finally:
			cur.close()
	def add_money(self,acctid,money):
		cur = self.conn.cursor()
		try:
			
			sql = "UPDATE account set money=money+%s WHERE acctid=%s"%(money,acctid)
			cur.execute(sql)
			print("add_money:"+sql)
			if cur.rowcount != 1:
				raise Exception("acctid %s fail to add money"%acctid)
		finally:
			cur.close()


	def transfer(self,source_acctid,target_acctid,money):
		try:
			self.check_acct_available(source_acctid)
			self.check_acct_available(target_acctid)
			self.has_enough_money(source_acctid,money)
			self.reduce_money(source_acctid,money)
			self.add_money(target_acctid,money)
			self.conn.commit()
		except Exception as e:
			self.conn.rollback()
			raise e



if __name__ == "__main__":

	source_acctid = sys.argv[1]
	target_acctid = sys.argv[2]
	money = sys.argv[3]

	conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='password',db='bank')
	tr_money = TransferMoney(conn)

	try:
		tr_money.transfer(source_acctid,target_acctid,money)
	except Exception as e:
		print("fault"+str(e))
	finally:
		conn.close()

