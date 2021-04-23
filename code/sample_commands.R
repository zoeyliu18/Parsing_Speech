python -m stanza.models.tagger --wordvec_file /workspace/stanza-eval/data/wordvec/word2vec/English/glove.840B.300d.txt --eval_file /workspace/stanza-eval/stanza/full/Brown_Eve_24_child.train --output_file /workspace/stanza-eval/stanza/full/Brown_Eve_24_child.pos --gold_file /workspace/stanza-eval/stanza/full/Brown_Eve_24_child.train --lang en --shorthand en_childes --mode predict $args

python -m stanza.models.parser --wordvec_file /workspace/stanza-eval/data/wordvec/word2vec/English/glove.840B.300d.txt --eval_file /workspace/stanza-eval/stanza/full/Brown_Eve_21_child.pos --output_file /workspace/stanza-eval/stanza/full/Brown_Eve_21_child.pred.parent --gold_file /workspace/stanza-eval/stanza/full/Brown_Eve_21_child.train --lang en --shorthand en_childes --mode predict $args

python -m stanza.models.finer --wordvec_file /workspace/stanza-eval/data/wordvec/word2vec/English/glove.840B.300d.txt --eval_file /workspace/stanza-eval/stanza/full/Brown_Eve_18_child.pos --output_file /workspace/stanza-eval/stanza/full/Brown_Eve_18_child.pred.ewt-parent-finetune --gold_file /workspace/stanza-eval/stanza/full/Brown_Eve_18_child.train --lang en --shorthand en_childes --mode predict $args

python -m stanza.models.parser --wordvec_file /workspace/stanza-eval/data/wordvec/word2vec/English/glove.840B.300d.txt --eval_file /workspace/stanza-eval/stanza/full/Brown_Eve_18_child.pos --output_file /workspace/stanza-eval/stanza/full/Brown_Eve_18_child.pred.parent --gold_file /workspace/stanza-eval/stanza/full/Brown_Eve_18_child.train --lang en --shorthand en_childes --mode predict $args

