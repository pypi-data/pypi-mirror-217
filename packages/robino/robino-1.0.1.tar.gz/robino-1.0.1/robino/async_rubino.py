from random import randint, choice
from .url import requests_url
import aiohttp

ch_url = choice(requests_url.urls)

class async_rubinoBot:
		def __init__(self, auth):
			self.auth = auth
			
		async def getMyProfileInfo(self, profile_id=None):
			async with aiohttp.ClientSession() as client:
				data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"profile_id":profile_id}, "method": "getMyProfileInfo"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def getProfileList(self):
			async with aiohttp.ClientSession() as client:
				data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"limit":10,"sort":"FromMax"},"method":"getProfileList"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def getRecentFollowingPosts(self,profile_id=None):
			async with aiohttp.ClientSession() as client:
				data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"profile_id":profile_id,"limit":20,"sort":"FromMax"},"method":"getRecentFollowingPosts"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def getProfilesStories(self, profile_id=None):
			async with aiohttp.ClientSession() as client:
				data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"profile_id":profile_id},"method":"getProfilesStories"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def Follow(self, followee_id, profile_id=None):
			async with aiohttp.ClientSession() as clinet:
				data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"followee_id":followee_id,"f_type":"Follow","profile_id":profile_id},"method":"requestFollow"}
				async with clinet.post(url=ch_url, json=data) as response:
					statuss = await response.json()
					if statuss['status'] == "OK":
						return statuss
					else:
						return f"{statuss}\n\nاگر این ارور را دریافت میکنید به این معنی است که یا قبلا فالو شده یا اشتباه درخواست میزنید."
						
		async def UnFollow(self, followee_id, profile_id=None):
			async with aiohttp.ClientSession() as client:
				data = data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"followee_id":followee_id,"f_type":"Unfollow","profile_id":profile_id},"method":"requestFollow"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def getProfileInfo(self, target_profile_id):
			async with aiohttp.ClientSession() as client:
				data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data":{"target_profile_id":target_profile_id},"method": "getProfileInfo"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def getProfilePosts(self, target_profile_id):
			async with aiohttp.ClientSession() as client:
				data = {"auth":self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"limit": 21,"sort": "FromMax","target_profile_id":target_profile_id},"method": "getProfilePosts"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def getPostByShareLink(self, link, profile_id=None):
			async with aiohttp.ClientSession() as client:
				link_id = link.split("post/")[1]
				data = {"auth":self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"share_string":link_id,"profile_id":profile_id},"method": "getPostByShareLink"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def likePost(self, post_id, post_profile_id):
			async with aiohttp.ClientSession() as client:
				data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"post_id":post_id,"post_profile_id":post_profile_id,"action_type":"Like"},"method":"likePostAction"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def UnlikePost(self, post_id, post_profile_id):
			async with aiohttp.ClientSession() as client:
				data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.0.2","package":"m.rubika.ir","platform":"PWA"},"data":{"post_id":post_id,"post_profile_id": post_profile_id,"action_type":"Unlike"},"method":"likePostAction"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def getComments(self,post_id, post_profile_id, profile_id = None ):
			async with aiohttp.ClientSession() as client:
				data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"profile_id": profile_id,"post_id": post_id,"post_profile_id": post_profile_id,"limit": 20,"sort": "FromMax","max_id": None},"method": "getComments"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def sendComment(self, text, post_id, post_profile_id, profile_id=None):
			async with aiohttp.ClientSession() as client:
				data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"content": text,"post_id": post_id,"post_profile_id": post_profile_id,"rnd":f"{randint(100000,999999999)}" ,"profile_id":profile_id},"method": 'addComment'}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def getExplorePosts(self, profile_id=None):
			async with aiohttp.ClientSession() as client:
				data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"profile_id": profile_id,"limit": 21,"sort": "FromMax","max_id": None},"method": "getExplorePosts"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def getStoryIds(self, target_profile_id, profile_id=None):
			async with aiohttp.ClientSession() as client:
				data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"profile_id": profile_id,"target_profile_id": target_profile_id},"method": "getStoryIds"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def getStory(self, story_profile_id, story_ids, profile_id=None):
			async with aiohttp.ClientSession() as client:
				data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"profile_id": profile_id,"story_profile_id": story_profile_id,"story_ids": story_ids},"method": "getStory"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def savePost(self, post_id, post_profile_id, profile_id=None):
			async with aiohttp.ClientSession() as client:
				data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"action_type":"Bookmark","post_id":post_id,"post_profile_id":post_profile_id,"profile_id":profile_id},"method": 'postBookmarkAction'}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def addViewStory(self, story_profile_id, story_ids):
			async with aiohttp.ClientSession() as client:
				data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"story_profile_id": story_profile_id,"story_ids": story_ids},"method": "addViewStory"}
				async with client.post(url=ch_url, json=data) as respons:
					return await respons.json()
					
		async def createPage(self, name, username, bio=None):
			async with aiohttp.ClientSession() as client:
				data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"bio": bio,"name": name,"username": username}, "method": "createPage"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def addPostViewCount(self, post_id, post_profile_id):
			async with aiohttp.ClientSession() as client:
				data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"post_id":post_id,"post_profile_id":post_profile_id}, "method": "addPostViewCount"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()
					
		async def getShareLink(self, post_id, post_profile_id, profile_id=None):
			async with aiohttp.ClientSession() as client:
				data = {"auth": self.auth,"api_version": "0","client": {"app_name": "Main","app_version": "2.0.2","package": "m.rubika.ir","platform": "PWA"},"data": {"post_id":post_id,"post_profile_id":post_profile_id,"profile_id":profile_id}, "method": "getShareLink"}
				async with client.post(url=ch_url, json=data) as response:
					return await response.json()