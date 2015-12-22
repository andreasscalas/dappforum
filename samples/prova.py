#!/usr/bin/python3
# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import os
import sys
import time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")
#Detection of wallet_A, if it doesn't exist it will be created
wallet_A = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
#Creation of the ForumManager for the wallet A
srManA = ForumManager.ForumManager (consMan, wallet=wallet_A)
user_info=srManA.getUserInfo(wallet_A.getAddress())
print('Comments owned by user test: ')
comments=user_info['comments']
for key in comments.keys():
	comment=comments[key]
	print('ID: ', key)
	print('Comment: ', comment['comment'])