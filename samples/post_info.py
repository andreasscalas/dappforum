#!/usr/bin/python3
# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time
import os

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
srMan = ForumManager.ForumManager (consMan, wallet=wallet)

os.system ('clear')
postid = input('Insert the ID of the post: ')
try:
	post = srMan.getPostInfo(postid)
	print ('Title of the post:\t',post['title'])
	print ('Message of the post:\t',post['message'])
	i=0	
	comments = post['comments']
	if(len(comments)>0):
		print("Comments:")
		for c in comments.values():
			print ("%d)"% i, c)
			i=i+1
except:
	print('Error')
	

