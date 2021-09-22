"""
All of the following commands, except where noted, are to be entered into
the Terminal interface.
"""

## Step 5 - Import Prodigy and Run Initial Annotation ##

pip install spacy
pip install json
pip install prodigy -f /Users/michaeldonnay/prodigy

#Create following directories:

# data - drop in raw text files, Jesuit names list, and Residence names list
# sources - to save source files and patterns

# Run Prodigy ner.manual to annotate the text manually, looking for named entities

prodigy ner.manual [name_of_dataset] blank:en [source_file.json] --loader json
--label RESID,PERSON --patterns [patterns_file.json]

#For this project, the dataset with punct (which I ultimately ended up using) -> dig_jes_with_punct

## Step 6 - Train Temporary NER Model ##

prodigy train [name_of_model] --ner [dataset_from_step_5] --eval-split .3

# Will give you a set of results, the score of which should hopefully increase over time

## Step 7 - Use Temp Model to Continue Annotating ##

prodigy ner.correct [name_of_new_dataset] [path_for_ner_model_from_step_6] 
[path_for_source_file_from_step_5.json] --loader json --label RESID,PERSON
--exclude [dataset_from_step_5]


#Dataset name should be different, to keep separate from previous dataset in case
#we need to go back a step, we'll have an older dataset to use.

#For this project, the dataset with punct (which I ultimately ended up using) -> dig_jes_with_punct

## Step 8 - Train Full NER Model ##

prodigy train [name_new_model] --ner [dataset_one],[dataset_two] --eval-split .3

#Use datasets from Step 5 and Step 7 if using multiple datasets
