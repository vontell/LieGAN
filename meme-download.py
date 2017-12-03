from os import listdir, walk
from os.path import isfile, join

path = './me_irl-image-downloader-master/downloaded'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]