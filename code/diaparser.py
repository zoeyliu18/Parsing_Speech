import io, os, string, argparse
from diaparser.parsers import Parser
import pandas as pd

puncts = list(string.punctuation)

AUX = ['can', 'could', 'ca', 'dare', 'do', 'did', 'does', 'have', 'had', 'has', 'may', 'might', 'must', 'need', 'ought', 'shall', 'should', 'will', 'would']
COP = ['be', 'is', 'was', 'am', 'are', 'were']
SUBJ = ['you', 'she', 'he', 'they', 'it', 'we', 'i']

unintelligible = ["xxx", "xx", "yyy", "yy", "www", "ww", "zzz", "zz"]

### Loading models

en_parser = Parser.load('en_ewt-electra')
#parser = Parser.load('en_ptb-electra')

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

def has_punct(w):

	p_l = []

	w = list(w)
	for p in puncts:
		if p in w:
			p_l.append(p)

	return p_l

def parse(file, output):

	print(file)

	w_punct = []

	df = pd.read_csv(output + file, encoding = 'utf-8')
	gloss = df['gloss'].tolist()
	stem = df['stem'].tolist()
	u_type = df['type'].tolist()
	num_morphemes = df['num_morphemes'].tolist()
	num_tokens = df['num_tokens'].tolist()
	corpus_name = df['corpus_name'].tolist()
	pos = df['part_of_speech'].tolist()
	speaker_code = df['speaker_code'].tolist()
	speaker_name = df['speaker_name'].tolist()
	speaker_role = df['speaker_role'].tolist()
	target_child_name = df['target_child_name'].tolist()
	target_child_age = df['target_child_age'].tolist()
	target_child_sex = df['target_child_sex'].tolist()
	collection_name = df['collection_name'].tolist()

	speaker_feature = []
	child_feature = []

	for i in range(len(speaker_name)):
		feature = u_type[i] + ' ' + str(num_morphemes[i]) + ' ' + str(num_tokens[i]) + ' ' + collection_name[i] 
		speaker_feature.append(str(speaker_name[i]) + ' ' + str(speaker_code[i]) + ' ' + str(speaker_role[i]))
		child_feature.append(str(target_child_name[i]) + ' ' + str(target_child_age[i]) + ' ' + str(target_child_sex[i]) + ' ' + str(corpus_name[i]) + ' ' + feature)

	new_gloss_list = []
	new_stem_list = []
	new_pos_list = []

	check = 0

	for i in range(len(gloss)):
		new_gloss = []
		new_stem = []
		new_pos = []
		if type(stem[i]) is not float and type(gloss[i]) is not float:
			check += 1
			toks = gloss[i].split()
			tok_stem = stem[i].split()
			tok_pos = pos[i].split()
			for z in range(len(toks)):
				w = toks[z]
				w_stem = '_'
				w_pos = '_'
				try:
					w_stem = tok_stem[z]
					w_pos = tok_pos[z]
				except:
					w_stem = '_'
					w_pos = '_'
		
				### e.g. don't ###
		
				if w.endswith("n't"):
					new_gloss.append(w[ : -3])
					new_gloss.append("n't")
					new_stem.append(w_stem)
					new_stem.append('not')
					new_pos.append(w_pos)
					new_pos.append('neg')
			
				### e.g. I'm ###
		
				elif w.endswith("'m"):
					new_gloss.append(w[ : -2])
					new_gloss.append("'m")
					new_stem.append(w_stem)
					new_stem.append('be')
					new_pos.append(w_pos)
					new_pos.append('cop')

				### e.g. She's / Mommy's book; copula vs. possessive###
		
				elif w.endswith("'s"):
					new_gloss.append(w[ : -2])
					new_gloss.append("'s")
					new_stem.append(w_stem)
					if w_pos == 'adj':
						new_stem.append("'s")
						new_pos.append('n')
						new_pos.append('poss')
					else:
						new_stem.append('be')
						if w[ : -2].lower() in SUBJ:
							new_pos.append('pro')
							new_pos.append('cop')
						else:
							new_pos.append('n')
							new_pos.append('cop')


				### e.g. There're ###
		
				elif w.endswith("'re"):
					new_gloss.append(w[ : -3])
					new_gloss.append("'re")
					new_stem.append(w_stem)
					new_stem.append('be')
					new_pos.append(w_pos)
					new_pos.append('cop')

				### combined adverbs or conjunctives ###

				elif len(has_punct(w)) != 0 and "'" not in w and "+" not in w:
					if '_' not in w:
						w_punct.append(w)

					for p in has_punct(w):
						w = w.replace(p, ' ')
				
					w = w.split()

					new_gloss.append(w[0])
					new_stem.append(w_stem)
					new_pos.append(w_pos)
					for c in w[1 : ]:
						new_gloss.append(c)
						new_stem.append(c)
						new_pos.append('combined')
						
				elif w in ['wanna', 'wana']:
					new_gloss.append(w[ : -2])
					new_gloss.append('na')
					new_stem.append('want')
					new_stem.append('to')
					new_pos.append('v')
					new_pos.append('inf')

				elif w in ['hafta']:
					new_gloss.append(w[ : -2])
					new_gloss.append('ta')
					new_stem.append('have')
					new_stem.append('to')
					new_pos.append('v')
					new_pos.append('inf')

				elif w in ['lemme']:
					new_gloss.append(w[ : -2])
					new_gloss.append('me')
					new_stem.append('let')
					new_stem.append('I')
					new_pos.append('v')
					new_pos.append('pro')

				elif w in ['shoulda', 'coulda', 'woulda', 'musta']:
					new_gloss.append(w[ : -1])
					new_gloss.append('a')
					new_stem.append(w[ : -1])
					new_stem.append('have')
					new_pos.append('aux')
					new_pos.append('aux')

				else:
					if w not in unintelligible:
						new_gloss.append(w)
						new_stem.append(w_stem)
						new_pos.append(w_pos)
					else:
						new_gloss.append('xxx')
						new_stem.append('xxx')
						new_pos.append('xxx')


		else:
			new_gloss.append('xxx')
			new_stem.append('xxx')
			new_pos.append('xxx')

		new_gloss_list.append(new_gloss)
		new_stem_list.append(new_stem)
		new_pos_list.append(new_pos)

	print(len(new_gloss_list))
	print(len(gloss))

	assert len(new_gloss_list) == len(gloss)
	assert len(new_gloss_list) == len(new_stem_list)
	assert len(new_gloss_list) == len(new_pos_list)

	print(set(w_punct))

	####### Parsing ######

	file_name = file[ : -4]

	outfile = io.open(output + file_name + '.conllu', 'w', encoding = 'utf-8')

	parse_check = 0

	for i in range(len(gloss)):
		if new_gloss_list[i] != ['xxx']:
#			if len(gloss[i].split()) != len(stem[i].split()):
#				print(gloss[i])
			
			parse_check += 1

			u = gloss[i]
			
			outfile.write('# text = ' + ' ' + u + '\n')
			
			try:
				parse_tree = en_parser.predict(new_gloss_list[i], text = 'en').sentences[0]
				attributes = parse_tree.__dict__['values']
				attributes[2] = tuple(new_stem_list[i])
				attributes[3] = tuple(new_pos_list[i])
				attributes[-2] = tuple([speaker_feature[i]] * len(attributes[0]))
				attributes[-1] = tuple([child_feature[i]] * len(attributes[0]))

				for i in range(len(attributes[0])):
					feature = []
					for z in attributes:
						feature.append(str(z[i]))
					outfile.write('\t'.join(w for w in feature) + '\n')

				outfile.write('\n')

			except:
				print(gloss[i], new_gloss_list[i])
				print(type(gloss[i]))

	print(check)
	print(parse_check)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = '.csv file extracted from childes-db')
	parser.add_argument('--output', type = str, help = 'output .conllu file')

	args = parser.parse_args()

	path = args.input
	os.chdir(path)

	for file in os.listdir(path):
		if file.endswith('.csv'):
			parse(file, args.output)


'''

with io.open('Parsing_Speech/Data/Eve/eve_annotated/full/Brown_Eve_18_parent.train', encoding = 'utf-8') as f:
	sent = conll_read_sentence(f)
	while sent is not None:
		sents.append([tok[1] for tok in sent])
		sent = conll_read_sentence(f)

pred = []

for s in sents:
	pred.append(parser.predict(s,text='en'))


with io.open('Parsing_Speech/Data/Eve/eve_annotated/full/parent_test.conllu', 'w', encoding = 'utf-8') as f:
	for s in pred:
		s = s.sentences[0]
	#	annotations = s.__dict__['annotations']
	#	f.write(annotations[-1] + '\n')
	#	f.write(annotations[-2] + '\n')
		attributes = s.__dict__['values']
		f.write('# text = ' + ' '.join(w for w in attributes[1]) + '\n')
		for i in range(len(attributes[0])):
			feature = []
			for z in attributes:
				if 'busy' in z:
					print(attributes)
				feature.append(str(z[i]))
			f.write('\t'.join(w for w in feature) + '\n')
		f.write('\n')

'''

