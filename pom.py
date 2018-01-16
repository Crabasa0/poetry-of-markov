import random
import util



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

def learnDistribution(wordList):
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
		
		
def generateTextFromDistribution(dist, length):
	wl = []
	for i in range(0, length):
		if i == 0:
			#wl.append(random.choice(dist.keys()))
			wl.append(util.sample(dist["."]))
		else:
			wl.append(util.sample(dist[wl[i-1]]))
	#convert the word list into a string
	return ' '.join(word for word in wl)
		
#same as above, but won't stop until it reaches a stopping point
def gTFD_smartTermination(dist, length):
	wl = []
	i = 0
	last = "."
	stops = [".", "!", "?"]
	while (i < length or last not in stops):
		next = util.sample(dist[last])
		last = next
		wl.append(next)
		i += 1
	return stitch(wl)

def stitch(wordList):
	nsp = [":", ";", ".", ",", "!", "?"]
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
    
    
#print generateTextFromDistribution(learnDistribution(read_words("solzhenitsyn.txt")), 50)

print gTFD_smartTermination(learnDistribution(readWordsAndPunctuation("shakespeare.txt")), 50)