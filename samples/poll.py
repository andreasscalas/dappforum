#!/usr/bin/python3
# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
from datetime import date
import time
import calendar

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
srMan = ForumManager.ForumManager (consMan, wallet=wallet)

while True:
	title = input ('Insert the title of the poll: ')
	choices = []
	n = input('How many choices do you want to make available? ')
	for i in range(0,int(n)):
		choices.append(input ('Insert the new choice of the poll: '))
	tmp = input('Insert the deadline in the format 01/01/1970 - 10.01: ')
	deadline_human = time.strptime(tmp, "%d/%m/%Y - %H.%M")
	deadline_human
	deadline=calendar.timegm(deadline_human)
	try:
		print ('Broadcasted:', srMan.createPoll (title, choices, deadline))
	except:
		print ('Error.')

