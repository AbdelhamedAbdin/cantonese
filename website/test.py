import re

verb_options = ['Verb', 'Noun']

# Case 1
sentence1 = ['SFP', 'Verb', '', 'Noun'] # Correct
# Case 2
sentence2 = ['Noun', 'SFP', '', 'Verb'] # rejected
# Case 3
sentence3 = ['Noun', 'SFP', '', 'Pu']   # rejected

i = 0
verb_inc = 0
collect_sentence = []
sentence_key = sentence1
verb_allowed = False

for s in sentence_key:
	obj = s
	if s in verb_options:
		i += 1
		# check if all verb are existing
		if i == len(verb_options):
			verb_allowed = True

if verb_allowed:
	if obj == verb_options[verb_inc]:
		collect_sentence.append(obj)
		verb_inc += 1

if len(collect_sentence) != len(verb_options):
	collect_sentence = []
	print("sentence doesn't have the verb sequence")
else:
	print(collect_sentence)
