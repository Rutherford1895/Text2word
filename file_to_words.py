#This module can split up an English passage into sentences and store the dictionary into a file
import sys
import string
import cPickle as pickle
import re

def unicodetoascii(text):

		TEXT = (text.
						replace('\xef\xbb\xbf', " ").
						replace('\xe3\x80\x80', " ").
						replace('\xe2\x80\x94',"-").
						replace('\xe2\x85\xa2',"III").
						replace('\xe2\x80\xa8',"\n").
						replace('\xe2\x80\x99',"'").
						replace('  '," ").
						replace('   '," ").
						replace('     '," ").
						replace('!',".")

								 )
		return TEXT

currentpassage = 'None'

# read file in
def Cat(filename1):
	print '\n','============================== Starting Cat =====','\n'
	f1 = open(filename1, 'r')
	global currentpassage 
	currentpassage = filename1[-10:-4]
	f2 = open(("out_"+currentpassage+".txt"), 'w+')
	text_raw = f1.read()
	text = unicodetoascii(text_raw)

	#show entire file
	print '\n','------------------------------ Original text ----','\n'
	#print text
	#print '------------'
	#split into sentences
	sentences = text.split('.')
	print text_raw.split('.')
	print "\n","------------------------------ Sentence list ----"
	print sentences
	#print '------------'

	for i in range(len(sentences)):
		letters = list(sentences[i])
		#add '.'to each sentence
		letters.append('.')
		#delete spaces before sentences
		for j in range(len(letters)):
			if (letters[j] == ' ') or (letters[j]=='\n') or (letters[j]=='\xe3') or (letters[j]=='\x80'):
				j+=1
			else:
				break
		del letters[0:j]		
		sentences[i]=''.join(letters)

	sentences.pop() #delete the last '.'
	numbered_sentences={}
	for k in range(len(sentences)):
		numbered_sentences[str(k)]=sentences[k]

	#print in lines, in terms of dict
	print '\n','------------------------------ Split text -------','\n'
	for l in range(len(numbered_sentences)):
		print l, ':', numbered_sentences.get(str(l))
		print
		f2.write(str(l)+' : '+numbered_sentences.get(str(l))+'\n')

	#save dict
	f3 = open("dict_of_sentences.txt",'w+')
	pickle.dump(numbered_sentences,f3)
	
	#close files
	f1.close() 
	f2.close()
	f3.close()

#Load passage dictionary into passage_dict
def Count(filename2):

	fn = open("words_full.txt",'r+') # inter - loop use, cannot truncate here

	fq = open("words_frequency.txt",'r+')
	try:
		words_full = pickle.load(fn)
	except EOFError:
		print 'There is currently no words in the dictionary'
		words_full = {}
	try:
		words_frequency = pickle.load(fq)
	except EOFError:
		print 'There is no frequency by now'
		words_frequency = {}

	passage_dict = pickle.load(open("dict_of_sentences.txt",'r'))
	word_number=len(words_full) # read how many words in the dictionary
	print 'Now dictionary length:', word_number
	for i in range(len(passage_dict)):
		print('')
		line = passage_dict.get(str(i))
		print(line)
		print

		#words = line.split(' ')
		words = re.split('\W+',line)
		words.pop()
		print(words)
		
		for j in range(len(words)):
			print '====>', words[j]
			notword = 0 # indicator for checking if this string contains number
			if (re.search('\d',words[j]) != None):
				print words[j], 'contains digital number, pass'
				notword = 1
			if ((words_full.get(words[j].lower()) == None) and (notword == 0)): # a new word appears
				#conjugation or plural?
				conjugation_or_plural = 0
				if (words[j][-1:] == 's') and (words[j][:-1] in words_full): #'s'
					conjugation_or_plural = 1
				if (words[j][-2:] == 'es') and (words[j][:-2] in words_full): #'es'
					conjugation_or_plural = 1	
				if (words[j][-3:] == 'ing') and ((words[j][:-3] in words_full) or (words[j][:-3]+'e' in words_full)):#v+ing or v-e+ing
					conjugation_or_plural = 1
				if (words[j][-2:] == 'ed') and ((words[j][:-2] in words_full) or (words[j][:-2]+'e' in words_full)):#v+ed or v-e+ed
					conjugation_or_plural = 1
				if conjugation_or_plural == 0:
					words_full[words[j].lower()] = str(word_number) # add new line into dict, no capital letter
					print words[j], ':',  word_number
					word_number+=1
					print 'New word "', words[j],  '" added, now dict size: ', word_number
					words_frequency[words[j].lower()] = 1
				else:
					print 'Conjugation of', words[j], 'found, pass.'
			else:
				if (words_full.get(words[j].lower()) != None): #this word already exists
			 		value = words_frequency[words[j].lower()] #frequency of this world +1
					value += 1
					words_frequency[words[j].lower()] = value
					#print '''"''', words[j],'''" 's''', 'frequency increased to ', words_frequency[words[j].lower()]
	print
	print('=====Counting New words completed=====')
	print
	print 'Now dictionary length:', word_number, '\n'
	print 'Writing in log'
	fl = open("words_count.txt",'a')
	fl.write(filename2[-10:-4]+'	'+str(word_number)+'\n')
	fl.close()
	print '...done'

	fn.close()
	print 'Writing dictionary'
	fn = open("words_full.txt",'w+') 
	pickle.dump(words_full,fn)
	fn.close()

	fq.close()
	print 'Updating frequency'
	sorted(words_frequency.iteritems(), key=lambda d:d[1], reverse = True)
	fq = open("words_frequency.txt",'w+')
	pickle.dump(words_frequency,fq)
	fq.close()
	print '...done'

def main():
	f1 = open("words_count.txt",'w+')
	f1.truncate()
	f1.close()
	f1 = open("words_full.txt",'w+')
	f1.truncate()
	f1.close()
	f1 = open("words_frequency.txt",'w+')
	f1.truncate()
	f1.close()

	books = ['5','6','7','8']
	for book in books:
		for test in ['1','2','3','4']:
			for passage in ['1','2','3']:
				path = './C'+book+'/C'+book+'T'+test+'P'+passage+'.txt'
				Cat(path)
				Count(path)


if __name__ == '__main__':
	main()
