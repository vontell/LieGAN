# The month is determined by the index of that month's folder in
# archive/. They are listed in ascending order when returned by
# listDir.

import os
import codecs # to handle Unicode characters

class ArchiveHelper():
	def __init__(self):
		# file indentifiers
		self.dateIndex = 0
		self.scoreRangeIndex = 0

		# folder names
		self.archive = 'archive'

		self.scoreRanges = ['5001-inf.txt', '1001-5000.txt', '501-1000.txt', '51-500.txt','0-50.txt']
		self.dates = os.listdir(self.archive)

		# filenames
		self.filename = ''
		self.tempFilename = ''

		# file for reading
		self.f = ''

		# read/write counters
		self.readCount = 0
		self.writeCount = 0

		# initialze post info container
		self.post = {}

		# flag to skip current file and move on
		self.skipFlag = False

	def setup(self, dateIndex, scoreRangeIndex):
		# sets up the data filename based on indentifiers and creates a temp file and opens it to read

		# construct filename based on date and score range
		self.filename = os.path.join(self.dates[dateIndex], self.scoreRanges[scoreRangeIndex])

		# reset skipFlag
		self.skipFlag = False

		try:
			# construct temp filename in archive
			self.tempFilename = self.filenameIn(self.archive) + '.tmp'

			# create temp file for reading
			os.rename(self.filenameIn(self.archive), self.tempFilename)
			print('Renamed ' + self.filenameIn(self.archive) + ' to ' + self.tempFilename)

			# open temp file for reading
			self.f = codecs.open(self.tempFilename, 'r', 'utf-8')

		except FileNotFoundError:
			print('Dump file {} doesn\'t exist. Moving to next file.'.format(self.filenameIn(self.archive)))
			self.skipFlag = True

	def filenameIn(self, folder):
		# returns a path to the data file inside the specified folder
		return os.path.join(folder, self.filename)

	def setPost(self, line, postfields = ['date', 'imageurl', 'score', 'title', 'user', 'posturl']):
		i = 0

		# remove newlines and carriage returns
		line = line.replace('\n', '')
		line = line.replace('\r', '')

		for field in str.split(line, ','):
			self.post[postfields[i]] = field
			i += 1

		# increment read counter
		self.readCount += 1

	def transfer(self, post, folder):
		# transfer a post to the specified folder

		# update post values to reflect changes made during processing
		self.post = post

		# define output path
		outputPath = self.filenameIn(folder)

		# make directories and file as necessary
		try:
			# open output file to append
			f = codecs.open(outputPath, 'a', 'utf-8')
		except FileNotFoundError:
			outputDir = ''
			for dir in outputPath.split('\\')[:-1]:
				outputDir = os.path.join(outputDir, dir)
			os.makedirs(outputDir)
			f = codecs.open(outputPath, 'a', 'utf-8')

		# make sure no comma is written before first value
		firstKey = True

		# write post data to file
		for key, value in self.post.items():
			if firstKey:
				firstKey = False
			else:
				f.write(',')

			f.write(value)

		f.write('\n')

		# increment write counter
		self.writeCount += 1

		f.close()

	def cleanup(self):
		self.f.close()
		# print('{} {}'.format(self.readCount, self.writeCount))

		# if no writes occur, rename temp file back to original
		if self.writeCount == 0:
			os.rename(self.tempFilename, self.filenameIn(self.archive))
			print('Renamed {0} to {1}'.format(self.tempFilename, self.filenameIn(self.archive)))

		# if writes occur and no lines are lost, delete temp file
		elif self.readCount == self.writeCount:
			os.remove(self.tempFilename)
			print('Removed {0}'.format(self.tempFilename))

		else:
			print('Error: some lines were lost when processing ' + self.filename)
