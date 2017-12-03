def count(dateIndex, scoreRangeIndex):
	# archive configuration
	archiveFolder = 'archive'
	scoreRanges = ['0-50.txt', '51-500.txt', '501-1000.txt', '1001-5000.txt', '5001-inf.txt']
	dates = listdir(archiveFolder)

	# construct filepath
	filepath = archiveFolder + '/' + dates[dateIndex] + '/' + scoreRanges[scoreRangeIndex]
	# logging.info(filepath)
	
	count = 0
	with codecs.open(filepath, 'r', 'utf-8') as f:
		for line in f:
			count += 1

	return count

def countalbum(dateIndex, scoreRangeIndex):
	# archive configuration
	archiveFolder = 'archive'
	scoreRanges = ['0-50.txt', '51-500.txt', '501-1000.txt', '1001-5000.txt', '5001-inf.txt']
	dates = listdir(archiveFolder)

	# construct filepath
	filepath = archiveFolder + '/' + dates[dateIndex] + '/' + scoreRanges[scoreRangeIndex]
	# logging.info(filepath)
	
	count = 0
	with codecs.open(filepath, 'r', 'utf-8') as f:
		for line in f:
			if '/a/' in line.split(',')[1]:
				count += 1

	return count

def countall(numberOfMonths, numberOfScoreRanges):
	postCount = []
	for i in range(numberOfMonths):
		row = [i]
		for j in range(numberOfScoreRanges):
			row.append(countalbum(i,j))
		postCount.append(row)
	return postCount