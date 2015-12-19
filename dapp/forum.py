# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import time

from contractvmd import config, dapp
from contractvmd.proto import Protocol
from contractvmd.chain.message import Message

logger = logging.getLogger(config.APP_NAME)

#List of the methods codes:
#METHOD_POST = code of the method createPost
#METHOD_COMMENT = code of the method commentPost
#METHOD_POLL = code of the method createPoll
#METHOD_VOTE = code of the method vote
#METHOD_EDITP = code of the method editPost
#METHOD_EDITC = code of the method editComment
#METHOD_DELPOST = code of the method deletePost
#METHOD_DELC = code of the method deleteComment
#METHOD_DELPOLL = code of the method deletePoll
class ForumProto:
	DAPP_CODE = [ 0x01, 0x04 ]
	METHOD_POST = 0x9
	METHOD_COMMENT = 0x10
	METHOD_POLL = 0x11
	METHOD_VOTE = 0x12
	METHOD_EDITP = 0x13
	METHOD_EDITC = 0x14
	METHOD_DELPOST = 0x15
	METHOD_DELC = 0x16
	METHOD_DELPOLL = 0x17
	METHOD_LIST1 = [METHOD_POST, METHOD_COMMENT, METHOD_POLL, METHOD_VOTE]
	METHOD_LIST2 = [METHOD_EDITP, METHOD_EDITC] 
	METHOD_LIST3 = [METHOD_DELPOST, METHOD_DELC, METHOD_DELPOLL]
	METHOD_LIST = METHOD_LIST1 + METHOD_LIST2 + METHOD_LIST3

class ForumMessage (Message):
	
	#Each createPost message must have the id of the user which creates 
	#the post (owner), a title of the post and a body (or message) of the post
	def createPost(owner, title, message):
		m = ForumMessage()
		m.Owner=owner
		m.Title=title
		m.Message=message
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_POST
		return m

	#Each commentPost message must have the id of the user which comments 
	#the post (owner), the id of the post to comment and a comment to the post
	def commentPost(owner, postid, comment):
		m = ForumMessage()
		m.Owner=owner
		m.PostID = postid
		m.Comment = comment
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_COMMENT
		return m

	#Each editPost message must have the id of the user which edits
	#the post (owner), the id of the post to edit, a new title of the post
	#and a new body (or message) of the post
	def editPost(owner, postid, title, message):
		m = ForumMessage
		m = ForumMessage()
		m.Owner=owner
		m.PostID=postid
		m.Title=title
		m.Message=message
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_EDITP
		return m
	
	#Each editComment message must have the id of the user which edits
	#the comment (owner), the id of the comment to edit and a new comment 
	#to the post
	def editComment(owner, commentid, comment):
		m = ForumMessage()
		m.Owner=owner
		m.CommentID = commentid
		m.Comment = comment
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_EDITC
		return m

	#Each deletePost message must have the id of the user which deletes
	#the post (owner) and the id of the post to delete
	def deletePost(owner, postid):
		m = ForumMessage()
		m.Owner=owner
		m.PostID = postid
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_DELPOST
		return m

	#Each deletePost message must have the id of the user which deletes
	#the post (owner) and the id of the post to delete
	def deleteComment(owner, commentid):
		m = ForumMessage()
		m.Owner=owner
		m.CommentID = commentid
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_DELC
		return m

	#Each createPoll message must have the id of the user which creates
	#the poll, the title of the poll, a list of choices for the poll
	#and a deadline.
	def createPoll(owner, title, choices, deadline):
		m = ForumMessage()
		m.Owner=owner
		m.Title=title
		m.Choices=choices
		m.Deadline=deadline
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_POLL
		return m
	
	#Each deletePoll message must have the id of the user which deletes 
	#the poll and the id of the poll to delete.
	def deletePoll(owner, pollid):
		m = ForumMessage()
		m.Owner=owner
		m.PollID = pollid
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_DELPOLL
		return m

	#Each vote message must have the id of the user which votes,
	#the id of the post to vote and a choice.
	def vote(owner, pollid, choice):
		m = ForumMessage()
		m.Owner = owner
		m.PollID = pollid
		m.Choice = choice
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_VOTE
		return m

	def toJSON (self):
		data = super (ForumMessage, self).toJSON ()

		if self.Method==ForumProto.METHOD_POST:
			data['owner']=self.Owner
			data['title']=self.Title
			data['message']=self.Message

		elif self.Method==ForumProto.METHOD_COMMENT:
			data['owner']=self.Owner
			data['postid']=self.PostID
			data['comment']=self.Comment

		elif self.Method==ForumProto.METHOD_EDITP:
			data['owner']=self.Owner
			data['postid']=self.PostID
			data['title']=self.Title
			data['message']=self.Message

		elif self.Method==ForumProto.METHOD_EDITC:
			data['owner']=self.Owner
			data['commentid']=self.CommentID
			data['comment']=self.Comment	
		
		elif self.Method==ForumProto.METHOD_DELPOST:
			data['owner']=self.Owner
			data['postid']=self.PostID

		elif self.Method==ForumProto.METHOD_DELC:
			data['owner']=self.Owner
			data['commentid']=self.CommentID

		elif self.Method==ForumProto.METHOD_POLL:
			data['owner']=self.Owner
			data['title']=self.Title
			data['choices']=self.Choices
			data['deadline']=self.Deadline
			
		elif self.Method==ForumProto.METHOD_DELPOLL:
			data['owner']=self.Owner
			data['pollid']=self.PollID

		elif self.Method==ForumProto.METHOD_VOTE:
			data['owner']=self.Owner
			data['pollid']=self.PollID
			data['choice']=self.Choice

		else:
			return None

		return data


class ForumAPI (dapp.API):

	def __init__ (self, vm, dht, api):
		self.api = api
		self.vm = vm
		self.dht = dht

		rpcmethods = {}
		
		#I define a list of APIs
		rpcmethods["createPost"]={
			"call": self.method_createPost, 
			"help": {"args": ["owner","title","message"], "return": {}}
		}

		rpcmethods["commentPost"]={
			"call": self.method_commentPost, 
			"help": {"args": ["owner","postid","comment"], "return": {}}
		}

		rpcmethods["editPost"]={
			"call": self.method_editPost, 
			"help": {"args": ["owner","postid","title","message"], "return": {}}
		}

		rpcmethods["editComment"]={
			"call": self.method_editComment, 
			"help": {"args": ["owner","commentid","comment"], "return": {}}
		}

		rpcmethods["deletePost"]={
			"call": self.method_deletePost, 
			"help": {"args": ["owner","postid"], "return": {}}
		}

		rpcmethods["deleteComment"]={
			"call": self.method_deleteComment, 
			"help": {"args": ["owner","commentid"], "return": {}}
		}

		rpcmethods["createPoll"]={
			"call": self.method_createPoll, 
			"help": {"args": ["owner","title","choices", "deadline"], "return": {}}
		}

		rpcmethods["deletePoll"]={
			"call": self.method_deletePoll, 
			"help": {"args": ["owner","pollid"], "return": {}}
		}

		rpcmethods["vote"]={
			"call": self.method_vote, 
			"help": {"args": ["owner", "pollid", "choice"], "return": {}}
		}

		rpcmethods["listPosts"] = {
			"call": self.method_listPosts,
			"help": {"args": [], "return": {}}
		}

		rpcmethods["listPolls"] = {
			"call": self.method_listPolls,
			"help": {"args": [], "return": {}}
		}

		rpcmethods["getPostInfo"] = {
			"call": self.method_getPostInfo,
			"help": {"args": ["postid"], "return": {}}
		}
			
		rpcmethods["getPollInfo"] = {
			"call": self.method_getPollInfo,
			"help": {"args": ["pollid"], "return": {}}
		}

		rpcmethods["getUserInfo"] = {
			"call": self.method_getUserInfo,
			"help": {"args": ["userid"], "return": {}}
		}

		errors = {}

		super (ForumAPI, self).__init__(vm, dht, rpcmethods, errors)
	
	#This method constructs a createPost message and creates a transaction
	#with which it distributes the message to the other nodes.
	def method_createPost(self, owner, title, message):
		msg=ForumMessage.createPost(owner, title, message)
		return self.createTransactionResponse(msg)
	
	#This method constructs a commentPost message and creates a transaction
	#with which it distributes the message to the other nodes.
	def method_commentPost(self, owner, postid, comment):
		msg=ForumMessage.commentPost(owner, postid, comment)
		return self.createTransactionResponse(msg)
	
	#This method constructs an editPost message and creates a transaction
	#with which it distributes the message to the other nodes.
	def method_editPost(self, owner, postid, title, message):
		msg=ForumMessage.editPost(owner, postid, title, message)
		return self.createTransactionResponse(msg)

	#This method constructs an editComment message and creates a transaction
	#with which it distributes the message to the other nodes.
	def method_editComment(self, owner, commentid, comment):
		msg=ForumMessage.editComment(owner, commentid, comment)
		return self.createTransactionResponse(msg)

	#This method constructs a deletePost message and creates a transaction
	#with which it distributes the message to the other nodes.
	def method_deletePost(self, owner, postid):
		msg=ForumMessage.deletePost(owner, postid)
		return self.createTransactionResponse(msg)

	#This method constructs a deleteComment message and creates a transaction
	#with which it distributes the message to the other nodes.
	def method_deleteComment(self, owner, commentid):
		msg=ForumMessage.deleteComment(owner, commentid)
		return self.createTransactionResponse(msg)

	#This method constructs a createPoll message and creates a transaction
	#with which it distributes the message to the other nodes.
	def method_createPoll(self, owner, title, choices, deadline):
		msg=ForumMessage.createPoll(owner, title, choices, deadline)
		return self.createTransactionResponse(msg)

	#This method constructs a deletePoll message and creates a transaction
	#with which it distributes the message to the other nodes.
	def method_deletePoll(self, owner, pollid):
		msg=ForumMessage.deletePoll(owner, pollid)
		return self.createTransactionResponse(msg)

	#This method constructs a vote message and creates a transaction
	#with which it distributes the message to the other nodes.
	def method_vote(self, owner, pollid, choice):
		msg=ForumMessage.vote(owner, pollid, choice)
		return self.createTransactionResponse(msg)

	#This method calls the self.core.listPosts method to request the list
	#of all the posts in the database
	def method_listPosts (self):	
		return self.core.listPosts ()
	
	#This method calls the self.core.listPolls method to request the list
	#of all the polls in the database
	def method_listPolls (self):
		return self.core.listPolls ()

	#This method calls the self.core.getPostInfo to request the info
	#of the post referred by postid
	def method_getPostInfo (self, postid):	
		return self.core.getPostInfo (postid)

	#This method calls the self.core.getPollInfo to request the info
	#of the poll referred by pollid
	def method_getPollInfo (self, pollid):	
		return self.core.getPollInfo (pollid)

	#This method calls the self.core.getUserInfo to request the info
	#of the user referred by userid
	def method_getUserInfo (self, userid):
		return self.core.getUserInfo (userid)

class ForumCore (dapp.Core):

	def __init__ (self, chain, database):
		database.init('posts', {})
		database.init('polls', {})
		super (ForumCore, self).__init__ (chain, database)
	
	#This method creates a new post
	#This post has a univocal ID (postid)
	def createPost(self, postid, owner, title, message):
		#I check in the list of posts if the post already exists 
		#(this will prevent the case in which a message is received more then 1 time)
		posts = self.database.get ('posts')
		if not (postid in posts):
			posts[postid] = {'owner': owner, 'title': title, 'message': message, 'comments': {}}
			self.database.set('posts', posts) #This will override the list in the db with the new list

	#This method creates a new comment to the post referred by postid
	#This comment has a univocal ID (commentid)
	def commentPost(self, commentid, owner, postid, comment):
		#I check if the post that the user wants to comment exists		
		posts=self.database.get ('posts')
		if postid in posts:
			post=posts[postid]			
			comments=post['comments']		
			#I check in the list of comments if the comment already exists 
			#(this will prevent the case in which a message is received more then 1 time)
			if not(commentid in comments):
				comments[commentid]= {'owner':owner, 'comment':comment}		
				self.database.set('posts', posts) #This will override the list in the db with the new list
		else:
			logger.pluginfo('This post does not exist')

	#This method edits the post referred by postid
	def editPost(self, owner, postid, title, message):
		#I check if the post that the user wants to edit exists		
		posts=self.database.get ('posts')
		if postid in posts:
			#I check if the user that wants to edit the post is the 
			#owner of the post itself (only the real owner can edit it)
			post=posts[postid]			
			if post['owner']==owner:
				post['title']=title
				post['message']=message	
				self.database.set('posts', posts) #This will override the post in the db with the new post
			else:
				logger.pluginfo('You cannot edit this post')
		else:
			logger.pluginfo('This post does not exist')

	#This method edits the comment referred by commentid
	def editComment(self, owner, commentid, comment):
		#I browse the list of posts in the database to find the comment
		posts=self.database.get ('posts')
		found=0
		for post in posts.values(): 
			logger.pluginfo(post)
			comments = post['comments']
			if commentid in comments:
				#I check if the user that wants to edit the comment is the 
				#owner of the comment itself (only the real owner can edit it)
				found=1
				c = comments[commentid]
				logger.pluginfo(c)			
				if c['owner']==owner:
					c['comment']=comment
					self.database.set('posts', posts) #This will override the comment in the db with the new comment
				else:
					logger.pluginfo('You cannot edit this comment')
		#I check if the comment that the user wants to edit exists
		#(if it exists the variable found would be equal to 1)		
		if found==0:
			logger.pluginfo('This comment does not exist')

	#This method deletes the post referred by postid
	def deletePost(self, owner, postid):
		#I check if the post that the user wants to delete exists
		posts=self.database.get('posts')
		if postid in posts:
			#I check if the user that wants to delete the post is the 
			#owner of the post itself (only the real owner can delete it)
			post = posts[postid]
			if owner==post['owner']:
				del posts[postid]
				self.database.set('posts', posts) #This will delete the post from the db
			else:
				logger.pluginfo('You cannot delete this post')
		else:
			logger.pluginfo('This post does not exists')			

	#This method deletes the commentreferred by commentid
	def deleteComment(self, owner, commentid):
		#I browse the list of posts in the database to find the comment
		posts=self.database.get('posts')
		found=0		
		for post in posts.values():
			comments=post['comments']
			if commentid in comments:
				#I check if the user that wants to delete the comment is the 
				#owner of the comment itself (only the real owner can delete it)
				comment=comments[commentid]
				found=1
				if owner==comment['owner']:
					del comments[commentid]
					self.database.set('posts', posts) #This will delete the comment from the db
				else:
					logger.pluginfo('You cannot delete this comment')
		#I check if the comment that the user wants to delete exists
		#(if it exists the variable found would be equal to 1)			
		if found==0:
			logger.pluginfo('This comment does not exists')			

	#This method creates a new poll
	def createPoll(self, pollid, owner, title, choices, deadline):
		#I check in the list of polls if the poll already exists 
		#(this will prevent the case in which a message is received more then 1 time)
		polls=self.database.get ('polls')
		if not (pollid in polls):	
			polls[pollid] = {'owner': owner, 'title': title, 'choices': choices, 'deadline': deadline, 'votes': {}}
			self.database.set('polls', polls) #This will override the list in the db with the new list
	
	#This method deletes the poll referred by pollid
	def deletePoll(self, owner, pollid):
		#I check if the poll that the user wants to delete exists
		polls=self.database.get('polls')
		if pollid in polls:
			#I check if the user that wants to delete the poll is the 
			#owner of the poll itself (only the real owner can delete it)
			poll = polls[pollid]
			if owner==poll['owner']:
				del polls[pollid]
				self.database.set('polls', polls) #This will delete the poll from the db
			else:
				logger.pluginfo('You cannot delete this poll')
		else:
			logger.pluginfo('This poll does not exists')	

	#This method inserts a new vote in the poll referred by pollid
	def vote(self, voteid, owner, pollid, choice):
		
		polls=self.database.get ('polls')
		if pollid in polls:
			poll=polls[pollid]
			if poll['deadline'] > int(time.time()):
				votes=poll['votes']
				#I check in the list of votes if the vote already exists 
				#(this will prevent the case in which a message is received more then 1 time)
				if not(voteid in votes):
					found=0
					#I check if the user that wants to vote has already voted
					for vote in votes.values():
						if owner in vote['owner']:
							found=1
					if found==0:					
						votes[voteid] = {'owner': owner, 'choice': choice}
						self.database.set('polls', polls) #This will override the list of votes in the db with the new list of votes
					else:
						logger.pluginfo("The user had already voted")								
			else:
				logger.pluginfo("Tried to vote a closed poll")
		else:
			logger.pluginfo("The poll does not exist")


	#This method returns the list of all the posts in the database
	def listPosts (self):
		return self.database.get ('posts')

	#This method returns the list of all the polls in the database
	def listPolls (self):	
		return self.database.get ('polls')
	
	#This method returns the information about the post
	#referred by postid
	def getPostInfo(self, postid):
		posts = self.database.get('posts')
		return posts[postid]

	#This method returns the information about the poll
	#referred by pollid
	#This information is composed by:
	#A flag which shows if the poll is open or closed
	#The title of the poll
	#The choices of the poll
	#The outcomes of each choice
	#The list of votes
	#The deadline
	def getPollInfo(self, pollid):
		return_dict = {}
		polls = self.database.get('polls')
		poll = polls[pollid]
		#I define if the poll is open or closed 
		if poll['deadline'] > int(time.time()):		
			return_dict['status'] = 'open'
		else:
			return_dict['status'] = 'closed'
		return_dict['title'] = poll['title']
		choices = poll['choices']
		res={}		
		for choice in choices:
			res[choice]=0

		votes = poll['votes']	
		#If there are votes in the poll i check what is
		#the choice of each vote and I increment the outcome
		#of he corresponding choice
		if(len(votes) > 0):
			for vote in votes.values():
				res[vote]=res[vote]+1
		return_dict['outcomes']=res
		return_dict['votes']=votes
		return_dict['deadline']=poll['deadline']
		
		return return_dict

	#This method returns the information about the user
	#referred by userid. This information is composed by:
	#The posts owned by the user
	#The comments inserted by the user
	#The polls owned by the user
	def getUserInfo(self, userid):
		posts=self.database.get('posts')
		polls=self.database.get('polls')
		
		user_posts={}
		user_comments={}
		user_polls={}
		user_votes={}
		
		#For each post I check if it is owned by the user
		#and if there are comments to the post written by the
		#user.
		for post_key in posts.keys():
			post=posts[post_key]
			if post['owner']==userid:
				user_posts[post_key]=post
			comments=post['comments']
			for comment_key in comments.keys():
				comment=comments[comment_key]
				if comment['owner']==userid:
					user_comments[comment_key]=comment
		
		#For each poll I check if it is owned by the user
		for poll_key in polls.keys():
			poll=polls[poll_key]
			if poll['owner']==userid:
				user_polls[poll_key]=poll	

		return_dict={'posts':user_posts, 'comments': user_comments, 'polls':user_polls}	
		return return_dict
			

class forum (dapp.Dapp):
	def __init__ (self, chain, db, dht, apimaster):
		self.core = ForumCore (chain, db)
		apiprov = ForumAPI (self.core, dht, apimaster)		
		super (forum, self).__init__(ForumProto.DAPP_CODE, ForumProto.METHOD_LIST, chain, db, dht, apiprov)
		

	def handleMessage (self, m):
		if m.Method==ForumProto.METHOD_POST:	
			logger.pluginfo('Found new message %s: creation of new post %s', m.Hash, m.Data['title'])
			#I add the hash of the transaction, which will be used as a univocal ID for the post, 
			#to the method parameters 
			self.core.createPost(m.Hash, m.Data['owner'], m.Data['title'], m.Data['message'])

		elif m.Method==ForumProto.METHOD_COMMENT:
			logger.pluginfo('Found new message %s: comment to %s', m.Hash, m.Data['postid'])
			#I add the hash of the transaction, which will be used as a univocal ID for the comment, 
			#to the method parameters 
			self.core.commentPost(m.Hash, m.Data['owner'], m.Data['postid'], m.Data['comment'])

		elif m.Method==ForumProto.METHOD_EDITP:
			logger.pluginfo('Found new message %s: edit post %s', m.Hash, m.Data['postid'])
			self.core.editPost(m.Data['owner'], m.Data['postid'], m.Data['title'], m.Data['message'])

		elif m.Method==ForumProto.METHOD_EDITC:
			logger.pluginfo('Found new message %s: edit comment %s', m.Hash, m.Data['commentid'])
			self.core.editComment(m.Data['owner'], m.Data['commentid'], m.Data['comment'])

		elif m.Method==ForumProto.METHOD_DELPOST:
			logger.pluginfo('Found new message %s: delete post %s', m.Hash, m.Data['postid'])
			self.core.deletePost(m.Data['owner'], m.Data['postid'])

		elif m.Method==ForumProto.METHOD_DELC:
			logger.pluginfo('Found new message %s: delete comment %s', m.Hash, m.Data['commentid'])
			self.core.deleteComment(m.Data['owner'], m.Data['commentid'])

		elif m.Method==ForumProto.METHOD_POLL:	
			logger.pluginfo('Found new message %s: creation of new poll %s', m.Hash, m.Data['title'])
			#I add the hash of the transaction, which will be used as a univocal ID for the poll, 
			#to the method parameters 
			self.core.createPoll(m.Hash, m.Data['owner'], m.Data['title'], m.Data['choices'], m.Data['deadline'])

		elif m.Method==ForumProto.METHOD_DELPOLL:
			logger.pluginfo('Found new message %s: delete poll %s', m.Hash, m.Data['pollid'])
			self.core.deletePoll(m.Data['owner'], m.Data['pollid'])

		elif m.Method==ForumProto.METHOD_VOTE:
			logger.pluginfo('Found new message %s: vote to %s', m.Hash, m.Data['pollid'])
			self.core.vote(m.Hash, m.Data['owner'], m.Data['pollid'], m.Data['choice'])