import pom
import pom2
import cPickle
import sys
import time #to see if unpickling is faster than learning

#interface which *should* make it easier to manage running various operations

def run (src, order, length):
	#attempt to load 1st order distribution from pickle, otherwise learn and create pickle
	#print "running with arguments ", src, " ", order, " ", length
	print "attempting to load d1 from pickle..."
	try:
		d1p = open((src+"1.pkl"))
		d1 = cPickle.load(d1p)
	except IOError:
		print "Fail! Learning d1."
		d1 = pom2.learnDistribution1(pom2.readWordsAndPunctuation(src+".txt"))
		d1p = open(src+"1.pkl", "w+")
		cPickle.dump(d1, d1p)
	d1p.close()
	print "d1 loaded."
	#same as above for 2nd order, if applicable
	if order == 2:
		print "attempting to load d2 from pickle..."
		try:
			d2p = open((src+"2.pkl"))
			d2 = cPickle.load(d2p)
			d2p.close()
		except IOError:
			print "Fail! Learning d2."
			d2 = pom2.learnDistribution2(pom2.readWordsAndPunctuation(src+".txt"))
			d2p = open((src+"2.pkl"), "w+")
			cPickle.dump(d2, d2p)
		d2p.close()
		print "d2 loaded"
	#generate text.
	text = "ERROR"
	print "generating text"
	if order == 1:
		text = pom.gTFD_smartTermination(d1, length)
	elif order == 2:
		text = pom2.gTFD_smartTermination(d1, d2, length)
	
	print text
	return text

args = sys.argv
#run(args[0] = "shakespeare", args[1] = 2, args[2] = 50)
startTime = time.time()
run(args[1], int(args[2]), int(args[3]))
print "time elapsed: ", time.time() - startTime



