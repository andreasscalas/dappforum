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
userid = input('Insert the ID of the user: ')
try:
	user_info = srMan.getUserInfo(userid)
	print('Posts owned by the user: ')
	posts=user_info['posts']
	for post in posts.values():
		print('Title: ', post['title'])
	print("\n")
	print('Comments owned by the user: ')
	comments=user_info['comments']
	for comment in comments.values():
		print('Comment: ', comment['comment'])
	print("\n")
	print('Polls owned by the user: ')
	polls=user_info['polls']
	for poll in polls.values():
		print('Poll: ', poll['title'])
except:
	print('Error')
	

