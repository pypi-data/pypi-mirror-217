from requests import post
from random import randint, choice
from .url import requests_url

ch_url = choice(requests_url.urls)

class rubinoBot:
	def __init__(self, auth):
		self.auth = auth
		
	def getProfileList(self):
		data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"limit":10,"sort":"FromMax"},"method":"getProfileList"}
		return post(url=ch_url,json=data).json()
		
	def getRecentFollowingPosts(self,profile_id=None):
		data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"profile_id":profile_id,"limit":20,"sort":"FromMax"},"method":"getRecentFollowingPosts"}
		return post(url=ch_url,json=data).json()
		
	def getProfilesStories(self, profile_id=None):
		data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"profile_id":profile_id},"method":"getProfilesStories"}
		return post(url=ch_url, json=data).json()
		
	def Follow(self, followee_id, profile_id=None):
		data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"followee_id":followee_id,"f_type":"Follow","profile_id":profile_id},"method":"requestFollow"}
		statuss = post(url=ch_url,json=data).json()
		if statuss['status'] == "OK":
			return statuss
		else:
			return f"{statuss}\n\nاگر این ارور را دریافت میکنید به این معنی است که یا قبلا فالو شده یا اشتباه درخواست میزنید."
			
	def UnFollow(self, followee_id, profile_id=None):
		data = data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"followee_id":followee_id,"f_type":"Unfollow","profile_id":profile_id},"method":"requestFollow"}
		return post(url=ch_url, json=data).json()
		
	def getProfileInfo(self, target_profile_id):
		data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data":{"target_profile_id":target_profile_id},"method": "getProfileInfo"}
		return post(url=ch_url,json=data).json()
		
	def getProfilePosts(self, target_profile_id):
		data = {"auth":self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"limit": 21,"sort": "FromMax","target_profile_id":target_profile_id},"method": "getProfilePosts"}
		return post(url=ch_url,json=data).json()
		
	def getPostByShareLink(self, link, profile_id=None):
		link_id = link.split("post/")[1]
		data = {"auth":self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"share_string":link_id,"profile_id":profile_id},"method": "getPostByShareLink"}
		return post(url=ch_url, json=data).json()
		
	def likePost(self, post_id, post_profile_id):
		data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"post_id":post_id,"post_profile_id":post_profile_id,"action_type":"Like"},"method":"likePostAction"}
		return post(url=ch_url, json=data).json()
		
	def UnlikePost(self, post_id, post_profile_id):
		data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"post_id":post_id,"post_profile_id": post_profile_id,"action_type":"Unlike"},"method":"likePostAction"}
		return post(url=ch_url, json=data).json()
		
	def getComments(self,post_id, post_profile_id, profile_id = None ):
		data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"profile_id": profile_id,"post_id": post_id,"post_profile_id": post_profile_id,"limit": 20,"sort": "FromMax","max_id": None},"method": "getComments"}
		return post(url=ch_url, json=data).json()
		
	def sendComment(self, text, post_id, post_profile_id, profile_id=None):
		data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"content": text,"post_id": post_id,"post_profile_id": post_profile_id,"rnd":f"{randint(100000,999999999)}" ,"profile_id":profile_id},"method": 'addComment'}
		return post(url=ch_url, json=data).json()
		
	def getExplorePosts(self, profile_id=None):
		data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"profile_id": profile_id,"limit": 21,"sort": "FromMax","max_id": None},"method": "getExplorePosts"}
		return post(url=ch_url, json=data).json()
		
	def getStoryIds(self, target_profile_id, profile_id=None):
		data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"profile_id": profile_id,"target_profile_id": target_profile_id},"method": "getStoryIds"}
		return post(url=ch_url, json=data).json()
		
	def getStory(self, story_profile_id, story_ids, profile_id=None):
		data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"profile_id": profile_id,"story_profile_id": story_profile_id,"story_ids": story_ids},"method": "getStory"}
		return post(url=ch_url,json=data).json()
		
	def savePost(self, post_id, post_profile_id, profile_id=None):
		data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"action_type":"Bookmark","post_id":post_id,"post_profile_id":post_profile_id,"profile_id":profile_id},"method": 'postBookmarkAction'}
		return post(url=ch_url, json=data).json()
		
	def addViewStory(self, story_profile_id, story_ids):
		data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"story_profile_id": story_profile_id,"story_ids": story_ids},"method": "addViewStory"}
		return post(url=ch_url, json=data).json()
		
	def createPage(self, name, username, bio=None):
		data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"bio": bio,"name": name,"username": username}, "method": "createPage"}
		return post(url=ch_url, json=data).json()
		
	def addPostViewCount(self, post_id, post_profile_id):
		data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"post_id":post_id,"post_profile_id":post_profile_id}, "method": "addPostViewCount"}
		return post(url=ch_url, json=data).json()
		
	def getMyProfileInfo(self, profile_id=None):
		data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"profile_id":profile_id}, "method": "getMyProfileInfo"}
		return post(url=ch_url, json=data).json()
		
	def getShareLink(self, post_id, post_profile_id, profile_id=None):
		data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"post_id":post_id,"post_profile_id":post_profile_id,"profile_id":profile_id}, "method": "getShareLink"}
		return post(url=ch_url, json=data).json()