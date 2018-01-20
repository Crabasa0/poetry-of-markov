#pom2 uses second-order markov chains
import random
import util
import time



def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]

    
def readWordsAndPunctuation(wordsFile):
	punctuation = ['!', '.', '?', '"', '(', ')', ';', ':', ',']
	with open(wordsFile, 'r') as f:
		wl = []
		for line in f:
			plist = []
			for word in line.split():
				if word[-1:] in punctuation:
					plist.append(word[:-1])
					plist.append(word[-1:])
				else:
					plist.append(word)
			wl += plist
		return wl

		
#TODO: Learn a first-order and second-order distribution
def learnDistribution2(wordList):
	dist = dict()
	for i in range (0, len(wordList)-2):
		w1 = wordList[i]
		w2 = wordList[i+1]
		w3 = wordList[i+2]
		if (w1,w2) not in dist:
			dist[(w1,w2)] = util.Counter()
		dist[(w1,w2)][w3] += 1
	for wp, c in dist.iteritems():
		#print "BEFORE NORMALIZING: ", c
		c = util.normalize(c)
		dist[wp] = c
		#print "AFTER NORMALIZING: ", c
	#print dist
	return dist

#yeah I think for now we're just gonna run 2 methods. Shouldnt be that much slower	
def learnDistribution1(wordList):
	dist = dict()
	for i in range (0, len(wordList)-1):
		w1 = wordList[i]
		w2 = wordList[i+1]
		if w1 not in dist:
			dist[w1] = util.Counter()
		dist[w1][w2] += 1
	for w, c in dist.iteritems():
		#print "BEFORE NORMALIZING: ", c
		c = util.normalize(c)
		dist[w] = c
		#print "AFTER NORMALIZING: ", c
	#print dist
	return dist
		
#TODO: change to use 2nd order mc		
def generateTextFromDistribution(dist1, dist2, length):
	wl = []
	for i in range(0, length):
		if i == 0:
			#wl.append(random.choice(dist.keys()))
			wl.append(util.sample(dist1["."]))
		elif i == 1:
			wl.append(util.sample(dist2[(".",wl[0])]))
		else:
			wl.append(util.sample(dist2[(wl[i-2], wl[i-1])]))#sample from dist for previous tuple
	#convert the word list into a string
	return ' '.join(word for word in wl)
		
#same as above, but won't stop until it reaches a stopping point
def gTFD_smartTermination(dist1, dist2, length):
	wl = []
	i = 0
	last = "."
	lastpair = (None, last)
	stops = [".", "!", "?"]
	while (i < length or last not in stops):
		if i < 1:
			next = util.sample(dist1[last])
		else:
			try:
				next = util.sample(dist2[lastpair])
			except KeyError: #this is a corner case when the lastpair is the last pair in the entire source. backs off to 1st order
				next = util.sample(dist1[last])
		lastpair = (last, next)
		#print "", i, " ", last not in stops
		last = next
		wl.append(next)
		i += 1
	return stitch(wl)

def stitch(wordList):
	nsp = [":", ";", ".", ",", "!", "?", ")"]
	#list of punctuation with no preceding space
	wl = []
	i = 0
	while i < len(wordList)-1:
		w1 = wordList[i]
		w2 = wordList[i+1]
		if w2 in nsp:
			w1 = ''.join([w1, w2])
			i += 1
		wl.append(w1)
		i += 1
	return ' '.join(word for word in wl)

"""	
st = time.time()	
words = readWordsAndPunctuation("shakespeare.txt")
dist1 = learnDistribution1(words)
dist2 = learnDistribution2(words)
print gTFD_smartTermination(dist1, dist2, 50)
print "elapsed time: ", time.time() - st
"""


