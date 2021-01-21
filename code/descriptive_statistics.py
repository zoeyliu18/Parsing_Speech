import io, os, argparse
import pandas as pd


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


def Expelliarmus(input):

	descriptive = {}

	for file in os.listdir(path):		
		if file.endswith('.conllu'):

			with io.open(file, encoding = 'utf-8') as f:

				target_child_u = []
				parent_u = []

				sent = conll_read_sentence(f)

				while sent is not None:
					speaker_info = sent[0][-2].split()
					speaker_role = speaker_info[-1]

					child_info = sent[0][-1]

					age = child_info.split()[1]

					if age not in ['nan', 'Multiple']:

						if speaker_role in ['Target_Child']:
							target_child_u.append(child_info + ' ' + speaker_role)

						if speaker_role in ['Mother', 'Father']:
							parent_u.append(child_info + ' ' + 'Parent')

					sent = conll_read_sentence(f)

				if len(target_child_u) >= 1:
					if target_child_u[0] not in descriptive:
						descriptive[target_child_u[0]] = len(target_child_u)
					else:
						descriptive[target_child_u[0]] += len(target_child_u)

				if len(parent_u) >= 1:
					if parent_u[0] not in descriptive:
						descriptive[parent_u[0]] = len(parent_u)
					else:
						descriptive[parent_u[0]] += len(parent_u)

	return descriptive


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'path to all .conllu files')
	parser.add_argument('--output', type = str, help = 'output .csv file')

	args = parser.parse_args()

	path = args.input
	os.chdir(path)

	descriptive_info = Expelliarmus(args.input)

	global_temp = {}

	corpus_temp = []
	child_temp = []
	age_temp = []
	gender_temp = []
	development_temp = []
	speaker_temp = []
	utterance_temp = []

	corpus_info = []
	child_info = []
	age_info = []
	gender_info = []
	development_info = []
	speaker_info = []
	utterance_info = []

	for k, v in descriptive_info.items():
	
		info = k.split()
	
		corpus = info[-2]
		child = info[0]
		age = info[1]
		gender = info[2]
		development = info[3]
		speaker = info[-1]

		corpus_temp.append(corpus)
		child_temp.append(child)
		age_temp.append(age)
		gender_temp.append(gender)
		development_temp.append(development)
		speaker_temp.append(speaker)
		utterance_temp.append(v)

		if corpus not in global_temp:
			global_temp[corpus] = [child]
		else:
			if child not in global_temp[corpus]:
				global_temp[corpus].append(child)

	for x in sorted(zip(corpus_temp, child_temp, age_temp, gender_temp, development_temp, speaker_temp, utterance_temp)):
		corpus_info.append(x[0])
		child_info.append(x[1])
		age_info.append(x[2])
		gender_info.append(x[3])
		development_info.append(x[4])
		speaker_info.append(x[5])
		utterance_info.append(x[6])

	global_info = []

	for c in corpus_info:
		global_info.append(len(global_temp[c]))


	data = {'Corpus': corpus_info, 'Child': child_info, 'Speaker': speaker_info, 'Age': age_info, 'Gender': gender_info, 
	'Development': development_info, 'Num_of_Utterance': utterance_info, 'Num_of_Children': global_info}

	data = pd.DataFrame(data)

	data.to_csv(args.output, index=False, encoding = 'utf-8')


