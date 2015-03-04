import re
import os
import sys
import urllib as urllib
from client import Client

import flickrapi
api_key="1d6c93276d02fe2bb38032f2b9037f7e" 
api_secret="bfb7b736968b4447"

flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='read')

def flickr_base_url():
	return "http://www.flickr.com/photos/"

def flickr_url(orig_url):
	photo= orig_url[36:]
	return flickr_base_url()+photo

def get_flickr_image_urls():
	#flickr api code in here to return only url_o for all images in BBC flickr group tagged orion
	o = flickr.photos.search(text="orion", group_ID ="1574153@N21", extras="url_o",format='parsed-json')
	return o['photos']['photo']

if __name__ == '__main__':
	# import optparse
	# parser = optparse.OptionParser()
	# parser.add_option('--server', dest='server', default='http://supernova.astrometry.net/api/', help='Set server base URL (eg, http://nova.astrometry.net/api/)')
	# parser.add_option('--apikey', '-k', dest='apikey', help='API key for Astrometry.net web service; if not given will check AN_API_KEY environment variable')
	# opt, args = parser.parse_args()
	# if opt.apikey is None:
	# 	opt.apikey = os.environ.get('AN_API_KEY', None)
	# if opt.apikey is None:
	# 	parser.print_help()
	# 	print
	# 	print 'YOu must either specify --apikey or set AN_API_KEY'
	# 	sys.exit(-1)

	useclient=True
	if useclient:
		client= Client(apiurl='http://nova.astrometry.net/api/')
		client.login('fqdbiklowdboehmf')

	urls = get_flickr_image_urls()
	for n in range(3):
		urli = flickr_url(str(urls[n]['url_o']))
		print 'THIS IS THE URL ITS USING', urli
		if urli is None:
			continue
		if useclient:
			client.url_upload(urli)
			print 'uploaded something...'
			print client.submission_images(1)
		else:
			cmd = "python ../client.py --server %s --apikey %s --urlupload \"%s\"" % (opt.server, opt.apikey, iurl)
			print cmd
			os.system(cmd)
