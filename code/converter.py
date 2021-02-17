##### Rule-based converter from CHILDES dependency to Universal Dependency-style dependency ######s

import os, io, argparse


### reading in sentences in CoNLL format ###

def conll_read_sentence(file_handle):
	sent = []
	for line in file_handle:
		line = line.strip('\n')
		
		if line.startswith('#') is False:
			toks = line.split("\t")
			
			if len(toks) != 10 and sent not in [[], ['']]:
				return sent 
			if len(toks) == 10 and '-' not in toks[0] and '.' not in toks[0]:
				sent.append(toks)	

	return None

def dependents(index, sentence):

	d = []

	for tok in sentence:
		if tok[6] == index:
			d.append(tok)

	return d

def convert(sentence):

	saying = ' '.join(w[1] for w in sentence)

	for tok in sentence:

		### root ###

		if tok[7] in ['ROOT', 'INCROOT':
			tok[7] = 'root'
	
		### subject ###

		if tok[7] == 'SUBJ':
			tok[7] = 'nsubj'

		### clausal subject ###

		if tok[7] == 'CSUBJ':
			tok[7] = 'csubj'

		### direct object ###

		if tok[7] == 'OBJ':
			tok[7] = 'obj'

		### indirect object ###

		if tok[7] == 'OBJ2':
			tok[7] = 'iobj'

	### COMP ###
	### TO DO ###

		### PRED ###

		if tok[7] == 'PRED':
			h = sentence[int(tok[6]) - 1]

			if h[3] == 'cop':
				subj = ''
				d_list = dependents(h[0], sentence)
				for d in d_list:
					if d[7] in ['SUBJ', 'nsubj']:
						subj = d

				if subj != '':
					if subj[1].startswith('wh') or subj[1] in ['how', 'How']: ### what is that
						sentence[int(subj[0]) - 1][6] = h[6]
						sentence[int(subj[0]) - 1][7] = h[7]
						sentence[int(h[0]) - 1][6] = sentence[int(subj[0]) - 1][1]
						sentence[int(h[0]) - 1][7] = 'cop'
						tok[6] = sentence[int(subj[0]) - 1][1]
						tok[7] = 'nsubj'

						for d in d_list:
							sentence[int(d[0]) - 1][6] = tok[0]
				
					else:
						 # that is good
						tok[6] = h[6]
						tok[7] = h[7]

						sentence[int(h[0]) - 1][6] = tok[0]
						sentence[int(h[0]) - 1][7] = 'cop'
			
						for d in d_list:
							sentence[int(d[0]) - 1][6] = tok[0]
				else:
					print(saying + ' COPULA NO SUBJECT')

			else:
				tok[7] = 'xcomp'  # become good

		if tok[3] == v:
			d_list = dependents(tok[0], sentence)
			for d in d_list:
				if d[3] == 'conj' and d[7] == 'LINK':
					if d[1] != 'and':
						sentence[int(d[0]) - 1][7] = 'mark'
					else:
						sentence[int(d[0]) - 1][7] = 'cc'
				else:
					print(saying + ' CHECK LINK')


		### adpositional object ###
		### sit on the stool / apple on the table ###

		if tok[7] == 'POBJ':
			h = sentence[int(tok[6]) - 1]
			tok[6] = h[6]
			sentence[int(h[0]) - 1][6] = tok[0]
		
			if h[7] == 'JCT':
				tok[7] = 'obl'
			if h[7] == 'NJCT':
				tok[7] = 'nmod'
		
			sentence[int(h[0]) - 1][7] = 'case'

			d_list = dependents(h[0], sentence)
			for d in d_list:
				sentence[int(d[0]) - 1][6] = tok[0]

		### serial verb ###
		### go find it ###

		if tok[7] == 'SRL':
			h = sentence[int(tok[6]) - 1]

			tok[6] = h[6]
			tok[7] = h[7]

			sentence[int(h[0]) - 1][6] = tok[0]
			sentence[int(h[0]) - 1][7] = 'compound:svc'


		### xadjunct ###
		### TO DO ###

		if tok[7] == 'MOD':
			if tok[3] == 'n' and "'s" not in tok[1]:
				tok[7] = 'nmod'
			if tok[3] == 'adj' and "'s" not in tok[1]:
				tok[7] = 'amod'

		### appositive ###

		if tok[7] == 'APP':
			tok[7] = 'appos'

		### Clausal modifier ###
		### TO DO ###

		### Xmodifier ###
		### TO DO ###

		### determiner ###

		if tok[7] == 'DET':
			if tok[3] == 'pro':
				tok[7] = 'nmod:poss'
			else:
				tok[7] = 'det'

		### quantifier ###
		### TO DO ###

		### postquantifier ###
		### TO DO ###

		### auxiliary ###

		if tok[7] == 'AUX':
			tok[7] = 'aux'

		### negation ###

		if tok[7] == 'NEG':
			h = sentence[int(tok[6]) - 1]

			if h[7] == 'AUX' or h[3] == 'cop':
				try:
					h_h = sentence[int(h[6]) - 1]
					if h_h[3] == 'v':
						tok[7] = 'advmod'
				except:
					tok = tok

		### infinitive ###

		if tok[7] == 'INF':
			tok[7] = 'mark'


		### COM BEG END ###

		if tok[7] in ['COM', 'BEG', 'END']:
			tok[7] = 'discourse'

		### VOC ###

		if tok[7] == 'VOC':
			tok[7] = 'vocative'

		### NAME ###
		### TO DO ###

		### DATE ###

		if tok[7] == 'DATE':
			tok[7] = 'nummod'

		### enumeration ###

		if tok[7] == 'ENUM':
			tok[7] = 'conj'

		### (multiple) conjunction with coordination ###

		if tok[7] == 'COORD':
			h = sentence[int(tok[6]) - 1]

			if h[3] == 'conj':
				if h[6] == '0':
					tok[6] = '0'
					tok[7] = 'root'
					sentence[int(h[0]) - 1][6] = tok[0]
					sentence[int(h[0]) - 1][7] = 'cc'
				else:
					if h[7] == 'CONJ':
						h_h = sentence[int(h[6]) - 1]

						tok[6] = h[6]
						tok[7] = 'conj'

						sentence[int(h) - 1][6] = tok[0]
						sentence[int(h) - 1][7] = 'cc'


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'path to .conllu files')
	parser.add_argument('--output', type = str, help = 'output converted .conllu files')

	args = parser.parse_args()

	path = args.input
	os.chdir(path)

	for file in os.listdir(path):		
		if file.endswith('.conllu'):
			Expelliarmus(file, path, args.output)
				




'''

		### clausal prepositional object ###
		### I'm confused about what you are asking ###

		if tok[7] == 'CPOBJ':
			tok[7] = 'advcl'

			h = sentence[int(tok[6]) - 1]
			tok[6] = h[6]
			h[6] = tok[0]
			h[7] = 'mark'

			d_list = dependents(tok[0], sentence)
			subj = 0
			obj = 0
			for d in d_list:
				if d[7] == 'nsubj':
					subj += 1
				if d[7] == 'obj':
					obj += 1
			for d in d_list:
				if d[7] == 'LINK':
					if subj != 0 and obj == 0:
						d[7] = 'obj'
					if subj == 0:
						d[7] = 'nsubj'
					if subj != 0 and obj != 0:
						d[7] = 'obl'

		### clausal object ###
		### I remember what you said ###

		if tok[7] == 'COBJ':
			tok[7] = 'acl:relcl'

			d_list = dependents(toks[0], sentence)
			for d in d_list:
				if d[7] == 'LINK':
					d[6] = tok[6]
					d[7] = 'obj'
					tok[6] = d[0]

		### adjunct ###
		### TO DO ###

		### clausal conjunct ###

		if tok[7] == 'CJCT':
			d_list = dependents(tok[0], sentence)
			for d in d_list:
				if d[7] == 'LINK':
					tok[7] = 'advcl'
					d[3] = 'SCONJ'


		### postmodifier ###
		### TO DO ###

		### POSS ###
		### TO DO ###


'''







