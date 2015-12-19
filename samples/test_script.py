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

wallet_A = WalletExplorer.WalletExplorer (wallet_file='A.wallet')
srManA = ForumManager.ForumManager (consMan, wallet=wallet_A)

wallet_B = WalletExplorer.WalletExplorer (wallet_file='B.wallet')
srManB = ForumManager.ForumManager (consMan, wallet=wallet_B)

#***********Creation of post and comment by wallet A************
try:
	postid = srManA.createPost('Hello post', 'Post di test')
except:
	print('Error 1')

while True:
	os.system ('clear')
	posts = srManA.listPosts()
	print('Posts: ', list(posts.keys()))
	if postid in posts:
		break
	time.sleep(5)

print('POST->', postid)

try:
	commid = srManA.commentPost(postid, 'This is a comment')
except:
	print('Error 2')

while True:
	os.system ('clear')
	post = srManA.getPostInfo(postid)
	print('Post ', postid)
	print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
	if commid in post['comments']:
		break
	time.sleep(5)

print('COMMENT->', commid)

#***********Creation of post and comment by wallet B************
try:
	postid2 = srManB.createPost('Hello post 2', 'Post di test 2')
except:
	print('Error 3')

try:
	commid2 = srManB.commentPost(postid, 'This is a comment of B')
except:
	print('Error 4')

while True:
	os.system ('clear')
	post = srManB.getPostInfo(postid)
	print('Post ', postid)
	print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
	if commid2 in post['comments']:
		break
	time.sleep(5)

print('COMMENT->', commid2)

while True:
	posts = srManA.listPosts()
	if postid2 in posts:
		break
	time.sleep(5)

print('POST->', postid2)

#**************************End of Basic part***************************

#***************Creation of poll and votes by wallet A*****************
try:
	pollid = srManA.createPoll('Title', ['answer1', 'answer2', 'answer3', 'answer4'], '31/12/2017')
	
except:
	print('Error 5')

while True:
	os.system ('clear')
	polls = srManA.listPolls()
	print('Posts: ', list(polls.keys()))
	if pollid in polls:
		break
	time.sleep(5)

print('POLL->', pollid)

try:
	voteid1 = srManA.vote(pollid, 'answer1')
except:
	print('Error 6')

try:
	voteid2 = srManA.vote(pollid, 'answer2')
except:
	print('Error 7')

while True:
	os.system ('clear')
	poll = srManA.getPollInfo(pollid)
	print('Poll ', pollid)
	print(poll['title'], ' ', poll['choices'], ' ', list(poll['votes'].values()), ' ', poll['deadline'])
	if voteid1 in poll['votes']:
		break
	time.sleep(5)

print('VOTE->', voteid1)

#***************Creation of poll and votes by wallet B*****************
try:
	voteid3 = srManB.vote(pollid, 'answer2')
except:
	print('Error 8')

while True:
	os.system ('clear')
	poll = srManB.getPollInfo(pollid)
	print('Poll ', pollid)
	print(poll['title'], ' ', poll['choices'], ' ', list(poll['votes'].values()), ' ', poll['deadline'])
	if voteid3 in poll['votes']:
		break
	time.sleep(5)

print('VOTE->', voteid3)

try:
	pollid2 = srManB.createPoll('Title', ['answer1', 'answer2', 'answer3', 'answer4'], '31/12/2017')
	
except:
	print('Error 9')

while True:
	os.system ('clear')
	polls = srManB.listPolls()
	print('Posts: ', list(polls.keys()))
	if pollid2 in polls:
		break
	time.sleep(5)

print('POLL->', pollid2)

#*************************End of Advanced part*************************

print(srManA.getUserInfo(wallet_A.getAddress()))

try:
	srManB.editComment(commid, 'New comment 1 message')
except:
	print('Error 10')

try:
	srManA.editComment(commid, 'New comment 2 message')
except:
	print('Error 11')

try:
	srManB.editPost(postid, 'New hello post', 'New message!')
except:
	print('Error 12')

try:
	srManA.editPost(postid, 'New hello post A', 'New message!')
except:
	print('Error 13')

while True:
	os.system ('clear')
	posts = srManA.listPosts()
	print('Posts: ', list(posts.keys()))
	post=posts[postid]
	if post['title']=='New hello post A':
		break
	time.sleep(5)

print('Edit POST->', postid)

try:
	srManA.deleteComment(commid)
except:
	print('Error 14')

try:
	commid3 = srManB.commentPost(postid, 'This is a new comment')
except:
	print('Error 15')

while True:
	os.system ('clear')
	post = srManB.getPostInfo(postid)
	print('Post ', postid)
	print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
	if commid3 in post['comments']:
		break
	time.sleep(5)

print('COMMENT->', commid)

try:
	srManA.deleteComment(commid3)
except:
	print('Error 16')

try:
	srManB.deletePost(postid)
except:
	print('Error 17')

try:
	srManA.deletePost(postid)
except:
	print('Error 18')

while True:
	os.system ('clear')
	posts = srManA.listPosts()
	print('Posts: ', list(posts.keys()))
	if not(postid in posts):
		break
	time.sleep(5)

print('Delete POST->', postid)

try:
	srManB.deletePoll(pollid2)
except:
	print('Error 19')

while True:
	os.system ('clear')
	polls = srManB.listPolls()
	print('Posts: ', list(polls.keys()))
	if pollid2 in polls:
		break
	time.sleep(5)

print('Delete POLL->', pollid2)

print(srManA.getUserInfo(wallet_B.getAddress()))

print(srManA.getUserInfo(wallet_A.getAddress()))