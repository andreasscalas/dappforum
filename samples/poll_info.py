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
pollid = input('Insert the ID of the poll: ')
try:
	poll = srMan.getPollInfo(pollid)
	print ('The poll is ', poll['status'])
	print ('Title of the poll:\t',poll['title'])
	
	outcomes = poll['outcomes']
	print('Votes:')
	i=0	
	for vote in outcomes.keys():
		print (vote, outcomes[vote])
		i=i+1
		
	votes = poll['votes']
	if len (votes) > 0:
		print('Votes:')
		i=0	
		for c in votes.values():
			print ("%d)"% i, c)
			i=i+1

	print ('The poll will close on ',time.strftime("%d/%m/%Y - %H.%M",time.gmtime(poll['deadline'])))
	
except:
	print('Error')
	

