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

while True:
	os.system ('clear')
	print ('List:')
	polls = srMan.listPolls ()
	keys = polls.keys()
	for key in keys:
		poll=polls[key]
		print ('Poll id:\t\t',key)
		print ('Title of the post:\t',poll['title'])
		print('Choices:')
		i=0	
		for c in poll['choices']:
			print ("%d)"% i, c)
			i=i+1
				
		print ('Deadline of the poll:\t',poll['deadline'])
		
		votes = poll['votes']
		if len (votes) > 0:
			print('Votes:')
			i=0	
			for c in votes.values():
				print ("%d)"% i, c)
				i=i+1		
	
		print('\n')

	time.sleep (5)

