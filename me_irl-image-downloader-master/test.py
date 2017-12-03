# me_irl Image Downloader testing
# Author: Jay Bulsara

import mimetypes
import logging

from archiveHelper import ArchiveHelper
from downloadHelper import DownloadHelper

def test():
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
	archiveHelper = ArchiveHelper()

	print('Setting up dump file for reading.')
	archiveHelper.setup(18,0)
	print('Done\n')

	try:
		print('Parsing dump file.')
		# read file line by line
		for line in archiveHelper.f:
			# extract post data
			archiveHelper.setPost(line)

			# send post to downloadHelper
			downloadHelper = DownloadHelper(archiveHelper.post)

			# run download helper
			downloadHelper.run()

			# transfer post to proper directory
			archiveHelper.transfer(downloadHelper.post, 'archive')

	finally:
		print('Done\n'); print('Cleaning up.')
		archiveHelper.cleanup()
		print('Finished.\n\n')


if __name__ == '__main__':
	test()
