# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from libcontractvm import Wallet, ConsensusManager, DappManager

class ForumManager (DappManager.DappManager):
	def __init__ (self, consensusManager, wallet = None):
		super (ForumManager, self).__init__(consensusManager, wallet)

	def createPost(self, title, message):
		#I add the address of the wallet as the ID of the user
		owner=self.wallet.getAddress();
		cid=self.produceTransaction('forum.createPost', [owner, title, message])
		return cid

	def commentPost(self, postid, comment):
		#I add the address of the wallet as the ID of the user
		owner=self.wallet.getAddress();
		cid=self.produceTransaction('forum.commentPost', [owner, postid, comment])
		return cid

	def editPost(self, postid, title, message):
		#I add the address of the wallet as the ID of the user
		owner=self.wallet.getAddress();
		cid=self.produceTransaction('forum.editPost', [owner, postid, title, message])
		return cid

	def editComment(self, commentid, comment):
		#I add the address of the wallet as the ID of the user
		owner=self.wallet.getAddress();
		cid=self.produceTransaction('forum.editComment', [owner, commentid, comment])
		return cid

	def deletePost(self, postid):
		#I add the address of the wallet as the ID of the user
		owner=self.wallet.getAddress();
		cid=self.produceTransaction('forum.deletePost', [owner, postid])
		return cid

	def deleteComment(self, commentid):
		#I add the address of the wallet as the ID of the user
		owner=self.wallet.getAddress();
		cid=self.produceTransaction('forum.deleteComment', [owner, commentid])
		return cid

	def createPoll (self, title, choices, deadline):
		#I add the address of the wallet as the ID of the user
		owner=self.wallet.getAddress();
		cid=self.produceTransaction('forum.createPoll', [owner, title, choices, deadline])
		return cid

	def deletePoll(self, pollid):
		#I add the address of the wallet as the ID of the user
		owner=self.wallet.getAddress();
		cid=self.produceTransaction('forum.deletePoll', [owner, pollid])
		return cid

	def vote(self, pollid, choice):
		#I add the address of the wallet as the ID of the user
		owner=self.wallet.getAddress();
		cid=self.produceTransaction("forum.vote", [owner, pollid, choice])
		return cid	

	def listPosts (self):
		return self.consensusManager.jsonConsensusCall ('forum.listPosts', [])['result']

	def listPolls (self):
		return self.consensusManager.jsonConsensusCall ('forum.listPolls', [])['result']

	def getPostInfo(self, postid):
		return self.consensusManager.jsonConsensusCall ('forum.getPostInfo', [postid])['result']

	def getPollInfo(self, pollid):
		return self.consensusManager.jsonConsensusCall ('forum.getPollInfo', [pollid])['result']

	def getUserInfo(self, userid):
		return self.consensusManager.jsonConsensusCall ('forum.getUserInfo', [userid])['result']