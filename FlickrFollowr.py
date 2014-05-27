import sqlite3
import urllib2
import json

conn = sqlite3.connect('flickrbase.db')
c = conn.cursor()

flickr_json_api = 'http://api.flickr.com/services/rest/?format=json&%s'
api_key = "8a9fab943f79d23a3135b31d73bfdd6c"
api_secret = "d48d7bd4543562ff"


def get_contacts(nsid, storage):
	
	#--- Calls up a contact list, checks the database for old entries, and stores new ones ---#
	#--- Public call. No auth required---# 

	req_method = "flickr.contacts.getPublicList"	
	req_url = "https://api.flickr.com/services/rest/?method=" + req_method + "&api_key=" + api_key + "&user_id=" + nsid + "&format=json&nojsoncallback=1"	
		
	# read json response
	jstr = urllib2.urlopen(req_url).read()
	#convert json response to dictionary
	dict = json.loads(jstr) 
	list = dict["contacts"]["contact"]
	for num in list:
		nsid  = num["nsid"]
		username = num["username"]
		
		c.execute('SELECT * FROM '+storage+' WHERE Nsid like ? AND UserName=?', (nsid ,username,))
		if not c.fetchone():
			print "nope. not here yet" 
			#store Username and NSID
			c.execute('INSERT INTO '+storage+' (Nsid, Username) VALUES (?,?)', 
			(nsid, username))
			conn.commit()
		else: 
			print "already in existence"

# -------------------------------------------------------
# ---- PEOPLE I ALREADY FOLLOW --------------------------
# -------------------------------------------------------


def get_my_contacts():
	my_nsid = "91257603@N08"
	storage = "MyContacts" 
	get_contacts(my_nsid, storage)

# -------------------------------------------------------
# ---- INFLUENCERS AND THE PEOPLE THEY FOLLOW------------
# -------------------------------------------------------

def get_their_contacts():
	nsid_list = ["51035555243@N01"]
	storage = "TheirContacts"
	their_nsid =  nsid_list[0]
	for x in nsid_list:
		get_contacts(x, storage)

get_my_contacts()
get_their_contacts()
	
conn.close()
