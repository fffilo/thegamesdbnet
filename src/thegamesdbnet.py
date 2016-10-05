# -*- coding: utf-8 -*-

import requests, xmltodict, json


title = "TheGamesDB"
description = "An open, online database for video game fans"
base_url = "http://thegamesdb.net/"
api_url = base_url + "api/"
xml_attribs = True
json_indent = 4


class TheGamesDBNetException(Exception):
	pass


def _request(method, params={}):
	'''
	Send request to http://thegamesdb.net/api/{method}
	with parameters.

	Response (xml data) is converted to dict.

	Exeption is raised if not 200 status code is returned,
	or if Error node exists in xml document.
	'''
	url = api_url + method
	for key, value in params.items():
		if value == None:
			del params[key]

	try:
		request = requests.get(url, params)
		response = request.text
	except Exception, e:
		raise TheGamesDBNetException(e)

	if not request.status_code == 200:
		raise TheGamesDBNetException("Request to `%s` returns status code %s" % (url, str(request.status_code)))

	result = xmltodict.parse(response, xml_attribs=xml_attribs)

	if "Error" in result and result["Error"]:
		raise TheGamesDBNetException(result["Error"])

	return json.loads(json.dumps(result))

def get_games_list(name, platform=None, genre=None):
	'''
	The GetGamesList API search returns a listing of games matched up with loose search terms.

	Parameters:
		name (required)
		platform (optional): filters results by platform
		genre (optional): filters results by genre

	URL:
		http://wiki.thegamesdb.net/index.php/GetGamesList

	Example request:
		http://thegamesdb.net/api/GetGamesList.php?name=x-men
	'''
	return _request("GetGamesList.php", {"name": name, "platform": platform, "genre": genre})

def get_game(name=None, exactname=None, id=None, platform=None):
	'''
	The GetGameApi title search returns game data in an XML document or if an id is given it just returns the data for that specific game.
	An id overrides a name search.
	You must provide either the id, name, or exactname parameter. Any of these may be combined with the optional platform parameter.

	Parameters:
		name (string): Performs a search for a game by title - Alpha characters only, case insensitive, partial phrases accepted, no partial words.
		exactname (string): Performs a search for a game by exact title - Case insensitive, exact title matches only.
		id (int): ID representing a specific game.
		platform (string) (optional): Platform to filter results by, Alpha-Numeric characters only.

	URL:
		http://wiki.thegamesdb.net/index.php/GetGame

	Example request (a request for game info relating to the game with id number "2"):
		http://thegamesdb.net/api/GetGame.php?id=2
	'''
	return _request("GetGame.php", {"name": name, "exactname": exactname, "id": id, "platform": platform})

def get_art(id):
	'''
	This API feature returns a list of available artwork types and locations specific to the requested game id in the database. It also lists the resolution of any images available. Scrapers can be set to use a minimum or maximum resolution for specific images.

	Parameters:
		id (integer) (required): The numeric ID of the game in our database that you like to fetch artwork details for.

	URL:
		http://wiki.thegamesdb.net/index.php/GetArt

	Example request (a query to return all art for the game with an ID number of "2"):
		http://thegamesdb.net/api/GetArt.php?id=2
	'''
	return _request("GetArt.php", {"id": id})

def get_platforms_list():
	'''
	The GetGamesList API search returns a listing of a listing of all platforms available on the site, sorted by alphabetical order of name.

	Parameters:
		none

	URL:
		http://wiki.thegamesdb.net/index.php/GetPlatformsList

	Example request:
		http://thegamesdb.net/api/GetPlatformsList.php
	'''
	return _request("GetPlatformsList.php")

def get_platform(id):
	'''
	This API feature returns a set of metadata and artwork data for a specified Platform ID.

	Parameters:
		id (integer) (required): The numeric ID of the platform in our database that you like to fetch metadata and artwork data for.

	URL:
		http://wiki.thegamesdb.net/index.php/GetPlatform

	Example request (a query to return a set of metadata and artwork data for a Platform with an ID number of "15"):
		http://thegamesdb.net/api/GetPlatform.php?id=15
	'''
	return _request("GetPlatform.php", {"id": id})

def get_platform_games(platform=None):
	'''
	The GetPlatformGames API method returns a listing of all games (like GetGamesList) available on the site for the given platform.

	Parameters:
		platform (optional): the integer id of the required platform, as retrived from GetPlatformsList)

	URL:
		http://wiki.thegamesdb.net/index.php/GetPlatformGames

	Example request:
		http://thegamesdb.net/api/GetPlatformGames.php?platform=1
	'''
	return _request("GetPlatformGames.php", {"platform": platform})

def platform_games(platform):
	'''
	The PlatformGames API call lists all games under a certain platform.

	Parameters:
		platform (string) (required): the platform alias to list games for

	URL:
		http://wiki.thegamesdb.net/index.php/PlatformGames

	Example request:
		http://thegamesdb.net/api/PlatformGames.php?platform=microsoft+xbox+360
	'''
	return _request("PlatformGames.php", {"platform": platform})

def updates(time):
	'''
	The Updates API call returns all the games updated since the time in seconds.

	Parameters:
		time (int): time in seconds.

	URL:
		http://wiki.thegamesdb.net/index.php/Updates

	Example request (query for games that have been updated in the last 2,000 seconds):
		http://thegamesdb.net/api/Updates.php?time=2000
	'''
	return _request("Updates.php", {"time": time})

def user_rating(accountid, itemid, rating=None):
	'''
	The UserRating API call allows you get and set a user rating on a game.
	To get a users rating for a particular game supply only the 'accountid' and 'itemid' parameters.
	To set a users rating supply the 'accountid', 'itemid' and 'rating' parameters with a 'rating' parameter value of between 1 - 10 inclusive.
	To unrate/delete a users rating supply a 0 using the 'rating' parameter.

	Parameters:
		accountid (int) (required): users unique account api id.
		itemid (int) (required): unique game id
		rating (int 0-10) (optional): user rating.

	URL:
		http://wiki.thegamesdb.net/index.php/UserRating

	Example request:
		http://thegamesdb.net/api/User_Rating.php?accountid=58536D31278176DA&itemid=2
	'''
	return _request("User_Rating.php", {"accountid": accountid, "itemid": itemid, "rating": rating})

def user_favorites(accountid, type=None, gameid=None):
	'''
	The UserFavorites API call allows you get, set and remove a user game favorite.
	Always returns a list of the current favorite game id's.

	Parameters:
		accountid (int): users unique account api id.
		type (string add|remove) (optional): sets the action (add or remove) for the request.
		gameid (int) (optional): required if type is 'set'. The game id to preform the type on.

	URL:
		http://wiki.thegamesdb.net/index.php/UserFavorites

	Example request:
		http://thegamesdb.net/api/User_Favorites.php?accountid=58536D31278176DA&type=add&gameid=2
	'''
	return _request("User_Favorites.php", {"accountid": accountid, "type": type, "gameid": gameid})


if __name__ == "__main__":
	# to do: cli
	print json.dumps(get_game(id=2040), indent=json_indent)
