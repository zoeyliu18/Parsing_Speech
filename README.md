# Parsing_Speech
Dependency Annotation and Parsing for Spontaneous Speech

1. **Convert original CHILDES xml file to .conllu file**
   1. ```python3 code/ori_xml2conll.py --input Path_To_Corpus --output Path_To_Output --section Section (e.g. English-NA or English-UK)```
   2. ```eve.py``` tailored specifically for the Eve corpus from the Brown corpus
2. **Semi-automatic conversion from CHILDES annotation to UD annotation**
   1. ```python3 code/converter.py --input Input_Path --output Output_Path```
   2. in ```data/Eve/eve_annotated```
3. **Manual annotation**
   1. in ```data/Eve/eve_annotated```
4. **Significance testing of parsing results**
   1. ```python3 code/bootrap.py --gold Gold_Annotation_File --pred Predicted_File --n Number_Of_Iterations (e.g. 10000) --c Sample_Size (e.g. number of utterances in the file)```
5. **Descriptive statistics of child information from CHILDES**
   1. ```python3 code/descriptive_statistics.py --input Input_Path --output .csv_file```
   2. English: in ```results/en_descriptive.csv```
   3. Chinese: in ```results/zh_descriptive.csv```
6. **Models will be available via Zenodo (Thank you for your patience!)**
