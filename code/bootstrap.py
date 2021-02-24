import io, os, argparse, statistics, random


def conll_read_sentence(file_handle):
	sent = []
	for line in file_handle:
		line = line.strip('\n')
		if line.startswith('#') is False:
			toks = line.split("\t")
	#		print(toks)
	#		print(len(toks))
			if len(toks) != 10 and sent not in [[], ['']]:
				return sent 
			if len(toks) == 10 and '-' not in toks[0] and '.' not in toks[0]:
				sent.append(toks)	
#	print(sent)
	return None


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--gold', type = str, help = 'gold .conllu file')
	parser.add_argument('--pred', type = str, help = 'predicted .conllu file')
#	parser.add_argument('--output', type = str, help = 'output CoNLL-formatted file for CHILDES parsed by stanza')
	parser.add_argument('--n', type = str, help = 'number of sampling')
	parser.add_argument('--c', type = str, help = 'number of utterances in each sample')

	args = parser.parse_args()

#	path = args.input
#	os.chdir(path)

#	for file in os.listdir(path):			

	gold = []
	a = 0
	with io.open(args.gold, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)
		while sent is not None:
			gold.append(sent)
			a += len(sent)
			sent = conll_read_sentence(f)
	print(len(gold))
	print(a)
	pred = []
	with io.open(args.pred, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)
		while sent is not None:
			pred.append(sent)
			sent = conll_read_sentence(f)
	print(len(pred))
	all_ids = list(range(int(args.c)))

	POS = []
	UAS = []
	LAS = []

	for i in range(int(args.n)):
		sample_ids = random.choices(all_ids, k = int(args.c))
		gold_sample = []
		pred_sample = []
		for ids in sample_ids:
			gold_sample.append(gold[ids])
			pred_sample.append(pred[ids])
	
		uas = 0
		las = 0
		pos = 0
		total = 0
	
		for z in range(len(gold_sample)):
			gold_sent = gold_sample[z]
			pred_sent = pred_sample[z]

			total += len(gold_sample[z])

			for k in range(len(gold_sent)):

				if gold_sent[k][3] == pred_sent[k][3]:
					pos += 1

				if gold_sent[k][6] == pred_sent[k][6]:
					uas += 1
					if gold_sent[k][7] == pred_sent[k][7]:
						las += 1

		POS.append(round(pos * 100 / total, 2))
		UAS.append(round(uas * 100 / total, 2))
		LAS.append(round(las * 100 / total, 2))

	POS.sort()
	UAS.sort()
	LAS.sort()

	print("POS mean: " + str(round(statistics.mean(POS), 2)))
	print("POS lower: " + str(POS[250]))
	print("POS upper: " + str(POS[9750]))

	print("UAS mean: " + str(round(statistics.mean(UAS), 2)))
	print("UAS lower: " + str(UAS[250]))
	print("UAS upper: " + str(UAS[9750]))

	print("")

	print("LAS mean: " + str(round(statistics.mean(LAS), 2)))
	print("LAS lower: " + str(LAS[250]))
	print("LAS upper: " + str(LAS[9750]))

		

'''
	filename = args.file.split('.')[0]
	os.system('vim ' + args.input + filename + '.bootstrap')

	all_sent = []
	with io.open(args.input + args.file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)
		while sent is not None:
			all_sent.append(sent)
			sent = conll_read_sentence(f)

	for i in range(int(args.n)):

		with io.open(args.input + str(i) + '.pos', 'w', encoding = 'utf-8') as f:
			sample = random.choices(all_sent, k = int(args.c))
			for sent in sample:
				for tok in sent:
					f.write('\t'.join(w for w in tok) + '\n')
				f.write('\n')

#			os.system('python -m stanza.models.tagger --wordvec_file /workspace/stanza-childes/data/wordvec/word2vec/English/glove.840B.300d.txt --eval_file ' + args.input + file + ' --output_file ' + args.output + filename + '.pos' + ' --gold_file ' + args.input + file + ' --lang en --shorthand en_test --mode predict $args')
		os.system('python -m stanza.models.parser --wordvec_file /workspace/stanza-childes/data/wordvec/word2vec/English/glove.840B.300d.txt --eval_file ' + args.input + str(i) + '.pos' + ' --output_file ' + str(i) + '.pred' + ' --gold_file ' + args.input + filename + '.train' + ' --lang en --shorthand en_test --mode predict $args >> ' + args.input + filename + '.bootstrap')


	with io.open(args.input + filename + '.boostrap', encoding = 'utf-8') as f:
		UAS = []
		LAS = []

		for line in f:
			if line.startswith('UAS: '):
				uas = line.strip().split()[1]
				UAS.append(uas)
			if line.startswith('LAS: '):
				las = line.strip().split()[1]
				LAS.append(las)

		UAS.sort()
		LAS.sort()

		print("UAS mean: " + str(statistics.mean(UAS)))
		print("UAS lower: " + str(UAS[250]))
		print("UAS upper: " + str(UAS[9750]))

		print("")

		print("LAS mean: " + str(statistics.mean(LAS)))
		print("LAS lower: " + str(LAS[250]))
		print("LAS upper: " + str(LAS[9750]))

'''
