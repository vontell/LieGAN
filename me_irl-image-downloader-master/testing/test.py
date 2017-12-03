import mimetypes

def getExtensionsForType(generalType):
	for ext in mimetypes.types_map:
		if mimetypes.types_map[ext].split('/')[0] == generalType:
			yield ext
		yield '.gifv'

mimetypes.init()
filetypes = tuple(getExtensionsForType('image'))

url = 'https://40.media.tumblr.com/9b488440d40f8aee15bcf865b888a292/tumblr_o06u8mq3FV1v27d59o1_540.png'

if url.split('?')[0].endswith(filetypes):
	fileExt = '.' + url.split('?')[0].split('.')[-1]

print(fileExt)
