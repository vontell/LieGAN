# me_irl Image Downloader
# Author: Jay Bulsara

# uses leonardicus's imgur downloader: https://github.com/leonardicus/imgurdl

import logging
from os import listdir
import mimetypes
import traceback

from archiveHelper import ArchiveHelper
from downloadHelper import DownloadHelper

def main():
	# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
	numberOfMonths = 18
	numberOfScoreRanges = 5

	archiveHelper = ArchiveHelper()

	for i in range(numberOfMonths): # months
		for j in range(3): # score buckets
			archiveHelper.setup(i,j)
			if not archiveHelper.skipFlag:
				writeFlag = False
				# read file line by line
				try:
					for line in archiveHelper.f:
						try:
							# reset writeFlag
							writeFlag = False

							# extract post data
							archiveHelper.setPost(line)

							# send post to downloadHelper
							downloadHelper = DownloadHelper(archiveHelper.post)

							# run download helper
							downloadHelper.run()

							# transfer post to proper directory
							archiveHelper.transfer(downloadHelper.post, downloadHelper.outputFlag)
							writeFlag = True

						except Exception as e:
							print('Error on post ' + archiveHelper.post['date'])
							traceback.print_exc()
							print('Transferring post back to archive.')
							archiveHelper.transfer(downloadHelper.post, 'archive')

				except KeyboardInterrupt:
					print('Program interrupted. Transferring remaining posts back to archive.')
					currentLine = line
					runFlag = False
					archiveHelper.f.seek(0)
					for line in archiveHelper.f:
						if runFlag:
							archiveHelper.setPost(line)
							archiveHelper.transfer(downloadHelper.post, 'archive')
						elif not line == currentLine:
							continue
						elif line == currentLine:
							runFlag = True
							if not writeFlag:
								if not archiveHelper.post:
									archiveHelper.setPost(line)
								archiveHelper.transfer(archiveHelper.post, 'archive')
					traceback.print_exc()
					exit()

				finally:
					archiveHelper.cleanup()



if __name__ == '__main__':
	main()
