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

try:
	#Detection of wallet_A, if it doesn't exist it will be created
	wallet_A = WalletExplorer.WalletExplorer (wallet_file='A.wallet')
	#Creation of the ForumManager for the wallet A
	srManA = ForumManager.ForumManager (consMan, wallet=wallet_A)	
	
	#Detection of wallet_B, if it doesn't exist it will be created
	wallet_B = WalletExplorer.WalletExplorer (wallet_file='B.wallet')
	#Creation of the ForumManager for the wallet B
	srManB = ForumManager.ForumManager (consMan, wallet=wallet_B)
	#Just to check if the system is working
	srManA.listPosts()
except:
	#In the case contracvmd is not running or the dapp is not installed the program will exit
	print('Contractvm is not running or the dapp is not installed properly')
	os._exit(1)

try:
	#***********Creation of post and comment by wallet A************
	try:
		#Creation of the first post of user A
		postid = srManA.createPost('Hello post', 'Post di test')
	except:
		print('Error 1')

	#The program will wait until the post is saved in the db, showing the list of posts in
	#the db
	os.system ('clear')
	posts = srManA.listPosts()
	print('Posts: ', list(posts.keys()))
	while True:
		posts = srManA.listPosts()
		if postid in posts:		
			print('Posts: ', list(posts.keys()))
			break
		time.sleep(30)

	#Meaningful print that informs that the post has been created
	print('Post->', postid)

	try:
		#Creation of the first comment to the post referred by postid for the user A
		commid = srManA.commentPost(postid, 'This is a comment')
	except:
		print('Error 2')
	
	#The program will wait until the comment is saved in the db, showing the details
	#of the post that will be commentedos.system ('clear')
	post = srManA.getPostInfo(postid)
	print('Post ', postid)
	print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
	while True:
		post = srManA.getPostInfo(postid)
		if commid in post['comments']:
			print('Post ', postid)
			print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
			break
		time.sleep(30)

	#Meaningful print that informs that the comment has been saved
	print('COMMENT->', commid)

	#***********Creation of post and comment by wallet B************
	try:
		#Creation of the first post of user B
		postid2 = srManB.createPost('Hello post 2', 'Post di test 2')
	except:
		print('Error 3')

	try:
		#Creation of the first comment to the post referred by postid for 
		#the user B
		commid2 = srManB.commentPost(postid, 'This is a comment of B')
	except:
		print('Error 4')

	#The program will wait until the comment is saved in the db, showing the details
	#of the post that will be commented
	post = srManB.getPostInfo(postid)
	print('Post ', postid)
	print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
	while True:
		post = srManB.getPostInfo(postid)
		if commid2 in post['comments']:
			print('Post ', postid)
			print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
			break
		time.sleep(30)

	#Meaningful print that informs that the comment has been saved
	print('COMMENT->', commid2)

	#The program will wait until the post is saved in the db
	while True:
		posts = srManA.listPosts()
		if postid2 in posts:
			break
		time.sleep(30)

	#Meaningful print that informs that the post has been saved
	print('POST->', postid2)

	#**************************End of Basic part***************************

	#***************Creation of poll and votes by wallet A*****************
	try:
		#Creation of the first poll of user A
		pollid = srManA.createPoll('Title', ['answer1', 'answer2', 'answer3', 'answer4'], '31/12/2017 - 23.59')
	
	except:
		print('Error 5')

	#The program will wait until the poll is saved in the db, showing the list of polls in
	#the db
	polls = srManA.listPolls()
	print('Polls: ', list(polls.keys()))
	while True:
		polls = srManA.listPolls()
		if pollid in polls:
			print('Polls: ', list(polls.keys()))
			break
		time.sleep(30)

	#Meaningful print that informs that the poll has been saved
	print('POLL->', pollid)

	try:
		#First vote for the user to the poll referred by pollid
		voteid1 = srManA.vote(pollid, 'answer1')
	except:
		print('Error 6')

	#################################VERY IMPORTANT##################################
	#I've modified the sequence, anticipating the infinite loop inserted for waiting#
	#the insertion of the vote referred by voteid1, to prevent the case in which the#
	#vote referred by voteid2 is received before that referred by voteid1. If i had #
	#preserved the original sequence, the order in which the two transactions are   #
	#received would be nondeterministic (I can't say which of the transations would #
	#fail.									 	# 
	#################################################################################

	#The program will wait until the vote is saved in the db, showing the details
	#of the poll that will be voted
	poll = srManA.getPollInfo(pollid)
	print('Poll ', pollid)
	print(poll['status'], ' ', poll['title'], ' ', poll['outcomes'], ' ', list(poll['votes'].values()), ' ', poll['deadline'])
	while True:
		poll = srManA.getPollInfo(pollid)
		if voteid1 in poll['votes']:
			print('Poll ', pollid)
			print(poll['status'], ' ', poll['title'], ' ', poll['outcomes'], ' ', list(poll['votes'].values()), ' ', poll['deadline'])
			break
		time.sleep(30)

	#Meaningful print that informs that the vote has been saved
	print('VOTE->', voteid1)

	try:
		#Creation of the second vote for the user A to the poll referred by pollid (it shouldn't work,
		#the user has already voted
		voteid2 = srManA.vote(pollid, 'answer2')
	except:
		print('Error 7')


	#***************Creation of poll and votes by wallet B*****************
	try:
		#Creation of the first vote for the user B to the poll refered by pollid
		voteid3 = srManB.vote(pollid, 'answer2')
	except:
		print('Error 8')

	#The program will wait until the vote is saved in the db, showing the details
	#of the poll that will be voted
	poll = srManB.getPollInfo(pollid)
	print('Poll ', pollid)
	print(poll['status'], ' ', poll['title'], ' ', poll['outcomes'], ' ', list(poll['votes'].values()), ' ', poll['deadline'])
	while True:
		poll = srManB.getPollInfo(pollid)
		if voteid3 in poll['votes']:
			print('Poll ', pollid)
			print(poll['status'], ' ', poll['title'], ' ', poll['outcomes'], ' ', list(poll['votes'].values()), ' ', poll['deadline'])
			break
		time.sleep(30)

	#Meaningful print that informs that the vote has been saved
	print('VOTE->', voteid3)

	try:
		#Creation of the first poll for the user B
		pollid2 = srManB.createPoll('Title', ['answer1', 'answer2', 'answer3', 'answer4'], '31/12/2017 - 23.59')
	
	except:
		print('Error 9')

	#The program will wait until the poll is saved in the db, showing the list of polls in
	#the db
	polls = srManB.listPolls()
	print('Polls: ', list(polls.keys()))
	while True:
		polls = srManB.listPolls()
		if pollid2 in polls:			
			print('Polls: ', list(polls.keys()))
			break
		time.sleep(30)

	#Meaningful print that informs that the poll has been saved
	print('POLL->', pollid2)

	#*************************End of Advanced part*************************

	#Print of the information of the user A
	user_info=srManA.getUserInfo(wallet_A.getAddress())
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

	try:
		#Editing of the comment referred by commentid (it shouldn't work,
		#the comment is not owned by B)
		srManB.editComment(commid, 'New comment 1 message')
	except:
		print('Error 10')

	try:
		#Editing of the comment referred by commentid by user A
		srManA.editComment(commid, 'New comment 2 message')
	except:
		print('Error 11')

	#The program will wait until the new comment is saved in the db, showing the details
	#of the post of the comment that will be edited
	post = srManB.getPostInfo(postid)
	print('Post ', postid)
	print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
	while True:
		post = srManB.getPostInfo(postid)
		comments=post['comments']
		comment=comments[commid]
		if comment['comment']=='New comment 2 message':
			print('Post ', postid)
			print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
			break
		time.sleep(30)

	#Meaningful print that informs that the new comment has been saved
	print('Edit COMMENT->', commid)

	try:
		#Editing of the post referred by postid (it shouldn't work,
		#the post is not owned by B)
		srManB.editPost(postid, 'New hello post', 'New message!')
	except:
		print('Error 12')

	try:
		#Editing of the post referred by postid by user A
		srManA.editPost(postid, 'New hello post A', 'New message!')
	except:
		print('Error 13')

	#The program will wait until the new post is saved in the db, showing the list of posts in
	#the db
	posts = srManA.listPosts()
	print('Posts: ', list(posts.keys()))
	while True:
		posts = srManA.listPosts()
		post=posts[postid]
		if post['title']=='New hello post A':
			print('Posts: ', list(posts.keys()))
			break
		time.sleep(30)

	#Meaningful print that informs that the new post has been saved
	print('Edit POST->', postid)

	try:
		#Deletion of the first comment inserted by user A
		srManA.deleteComment(commid)
	except:
		print('Error 14')

	try:
		commid3 = srManB.commentPost(postid, 'This is a new comment')
	except:
		print('Error 15')

	#The program will wait until the comment is saved in the db, showing the details
	#of the post that will be commented
	post = srManB.getPostInfo(postid)
	print('Post ', postid)
	print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
	while True:
		post = srManB.getPostInfo(postid)
		if commid3 in post['comments']:
			print('Post ', postid)
			print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
			break
		time.sleep(30)

	#Meaningful print that informs that the comment has been saved
	print('COMMENT->', commid3)

	try:
		#Deletion, by the user A, of the comment just inserted by the user B
		#(it shouldn't work, the comment isn't owned by A)
		srManA.deleteComment(commid3)
	except:
		print('Error 16')

	try:
		#Deletion, by the user A, of the comment just inserted by the user B
		#(it shouldn't work, the comment isn't owned by A)
		srManB.deleteComment(commid3)
	except:
		print('Error 17')	

	#The program will wait until the comment is deleted from the db, showing the details
	#of the post of the comment that will be deleted
	post = srManB.getPostInfo(postid)
	print('Post ', postid)
	print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
	while True:
		post = srManB.getPostInfo(postid)
		if not(commid3 in post['comments']):
			print('Post ', postid)
			print(post['title'], ' ', post['message'], ' ', list(post['comments'].values()))
			break
		time.sleep(30)

	#Meaningful print that informs that the comment has been saved
	print('Delete COMMENT->', commid3)

	try:
		#Deletion, by the user B, of the first post created by the user A
		#(it shouldn't work, the post isn't owned by B)
		srManB.deletePost(postid)
	except:
		print('Error 18')

	try:
		#Deletion of the first post inserted by user A
		srManA.deletePost(postid)
	except:
		print('Error 19')

	#The program will wait until the post will be deleted, showing
	#the list of posts in the db
	posts = srManA.listPosts()
	print('Posts: ', list(posts.keys()))
	while True:
		posts = srManA.listPosts()
		if not(postid in posts):
			print('Posts: ', list(posts.keys()))
			break
		time.sleep(30)

	#Meaningful print that informs about the deletion of the post
	print('Delete POST->', postid)

	try:
		#Deletion of the first poll created by user B
		srManB.deletePoll(pollid2)
	except:
		print('Error 20')

	#The program will wait unil the poll will be deleted from the db,
	#showing the list of polls in the db
	polls = srManB.listPolls()
	print('Polls: ', list(polls.keys()))
	while True:
		polls = srManB.listPolls()
		if not(pollid2 in polls):
			print('Polls: ', list(polls.keys()))
			break
		time.sleep(30)

	#Meaningful print about the deletion of the poll
	print('Delete POLL->', pollid2)

	#Print of the information of the user B
	user_info=srManB.getUserInfo(wallet_B.getAddress())
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

	#Print of the information of the user A
	user_info=srManA.getUserInfo(wallet_A.getAddress())
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

	os._exit(0)
	
except:
	#In the case that one or both the wallets are "empty" the program will exit
	#There is even the case that, for some reason, contractvmd has been stopped,
	#(in that case the program will exit)
	print('You have to recharge wallets or, if you have stopped the contracvmd, you have to restart it')
	os._exit(1)