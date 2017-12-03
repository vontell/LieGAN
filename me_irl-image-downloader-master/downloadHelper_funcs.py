from imgurdl import ImgurDL
import mimetypes
import logging
import os
import urllib3

def downloadHelper(url):
	mimetypes.init()

	filetypes = tuple(getExtensionsForType('image'))
	domains = 'imgur', 'gfycat', 'youtube', 'youtu.be', 'reddituploads', 'fbcdn'

	# no file extension and no known domain - rogue
	if not url.split('?')[0].endswith(filetypes) and not any(s in url for s in domains):
		imagePath = '-rogue'

	# either a proper domain or a file extension exist
	else:
		args = {'url': url}

		for s in domains:
			if s in url:
				args['domain'] = s
				break
		# logging.info('domain = ' + domain)

		if url.split('?')[0].endswith(filetypes):
			args['fileExt'] = '.' + url.split('?')[0].split('.')[-1]
			# logging.info('has file extension ' + fileExt)

		imagePath = download(**args)

	return imagePath


def getExtensionsForType(generalType):
	for ext in mimetypes.types_map:
		if mimetypes.types_map[ext].split('/')[0] == generalType:
			yield ext


def download(url, domain='', fileExt=''):
	logging.debug('{0}, {1}, {2}'.format(url, domain, fileExt))
	imagePath = ''

	if domain == 'imgur':
		if fileExt != '':
			# cut off file extension as it is not supported by imgurdl
			url = url.split(fileExt)[0]
		# imagePath = downloadImgur(url)
		imagePath = '-imgur'
	
	elif domain == 'youtube' or domain == 'youtu.be':
		imagePath = '-skip'

	elif domain == 'fbcdn':
		# need to get me_irl post url for the picture
		imagePath = '-fbcdn'
	
	elif domain == 'gfycat':
		# very rarely will gfycat links have an extension, but sometimes they do
		if fileExt != '':
			imagePath = '-gfycat'
		else:
			# download as fileExt
			imagePath = '-ext'
	
	elif domain == 'reddituploads':
		# need to find out image type when http request is made
		imagePath = '-reddituploads'
	
	else:
		# just download the image
		imagePath = '-ext'

	

	return imagePath
		

def downloadImgur(url):
	imgur = ImgurDL()

	# set output directory
	imgur.use_default_directory = False
	imgur.output_dir = 'images'

	# add url token
	token = imgur.parse_token(url)

	if imgur.is_album(url):
		imgur.token_list.add((token, 'album'))
	else:
		imgur.token_list.add((token, 'image'))


	imgur.extract_urls(imgur.token_list)
	imgur.save_images()

	odir, ofile = list(list(imgur.download_list)[0])[1:]

	imagePath = "{0}/{1}/{2}".format(os.path.dirname(os.path.realpath(__file__)), odir, ofile)

	return imagePath

def downloadFileExt(url):
	imagePath = ''

	return imagePath


