import random
import util



def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]
    

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
			wl.append(random.choice(dist.keys()))
		else:
			wl.append(util.sample(dist[wl[i-1]]))
	#convert the word list into a string
	return ' '.join(word for word in wl)
		
		
    
print generateTextFromDistribution(learnDistribution(read_words("solzhenitsyn.txt")), 50)