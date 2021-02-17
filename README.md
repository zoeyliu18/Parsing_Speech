# Parsing_Speech
Dependency Annotation and Parsing for Spontaneous Speech

1. **Convert original CHILDES xml file to .conllu file**
   1. ```python3 code/ori_xml2conll.py --input PATH_TO_CORPUS --output PATH_TO_OUTPUT --section SECTION (e.g. English-NA or English-UK)```
2. **Semi-automatic conversion from CHILDES annotation to UD annotation**
   1. ```python3 code/converter.py --input INPUT_PATH --output OUTPUT_PATH```
