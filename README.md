# digital_jesuits_project

<h3>The Digital Jesuits Project</h3>
A repository for code, data, and documentation for the Digital Jesuit Project (DJP). The DJP is a collaboration between Michael Donnay,
UCL Dept. of Information Studies, and Christopher Donnay, OSU Dept. of Mathematics.
<br>
<br>
This project would not be possible without contributions, advice, or resources from:<br>
Adam F. Harrison <br>
I’yanla Brown<br>
John W. O'Malley, SJ<br>
David Collins, SJ<br>
Thomas Gaunt, SJ<br>
John Ladd<br>
Jessica Otis<br>
Daniel Shore<br>
Tommaso Astarita<br>
Nicoletta Pireddu<br>
WJB Mattingly & Python for Digital Humanities<br>
Explosion AI<br>
READ Coop<br>
<br>
This repository includes:<br>
1. All of the raw text files of the Maryland-New York Province Catalogues from 1880-1890 and 1915-1925.<br>
2. The Python files to process those text files.<br>
3. Terminal commands to run the natural language processing (NLP) annotation and training process.<br>
4. The Python files to analyze the NLP-processed catalogues.<br>
5. Copies of all saved files from the above processes.<br>
<br>
This ReadMe file contains:<br>
1. Research question.<br>
2. Timeline of project development.<br>
3. Explanation of steps for data pre-processing and processing.<br>
4. Results<br>


<h1>Research Question</h1>
Did the Jesuits in the Maryland-New York Province become less mobile in the period between 1880 and 1925?

<h1>Timeline</h1>

- April 2020: Initital project development and ideation

- April - May 2020: Version 0.1 - Manual data entry

- May 2020: Version 0.2 - Built in OCR with manual correction (Georgetown Interns)

- May 2020 - May 2021: Life-induced pause and Python skill development

- May-August 2021: Develop Transkribus model for HTR, process catalogues into text files

- August-September 2021: Version 0.3 - Write and test Python code for processing catalogues

- September 2021: Produce initital results


<h1>Explanation of Steps</h1>

<b>Step 1 - Clean Text</b>
- Import text files generated by Transkribus HTR program, remove most punctuation (retaining commas and periods, clean up some basic formatting issues, and save cleaned version as JSON files.
- `BEFORE` importing text files, go ahead and add year to first line of each one.
- In order to create enough text without any entities (which is important for the NER training process), I also generated some random Lorem Ipsum text and passed it through the same process as the catalogue text.

<b>Step 1.5 - Combine Catalogues</b>
- Prodigy requires a single source file of all of the text you'd like to annotate in order to train your model, so this step takes all of the clean text files generated in Step 1 and combines them into a single JSON file, which is the preferred format for Prodigy.
- For Prodigy training, it's useful to save them alternating 1880s and 1910s so that you can train the initial model on both decades.

<b>Step 2 - Import Jesuit Names</b>
- In order to train a named entity recognition pipeline in the spaCy NLP package, you need to annotate a chunk of text to serve as the training and validation sets for the model training process. You can annotate all of these examples by hand, but that can take a really long time. In order to sped the process up, you can use the Entity Ruler to create some initial rules for annotating the text. In our case, that means creating an initial list of Jesuit names.
- this step imports a CSV file of Jesuit names gathered from an earlier version of this project and manually from several catalogues. Once imported, the program cleans the names and saves them to a new JSON in the two formats they appear in the catalogues: FIRST MIDDLE LAST and LAST, FIRST MIDDLE.

<b>Step 3 - Import Residence Names</b>
- Just like with the Jesuit names, it's helps to speed the annotation process if we can start off with some residence patterns for spaCy to use.
- This program takes a text file of residence names manually assembled from some of the catalogues, imports it as a list, and then saves that list in spaCy's preferred format as a JSON file.

<b>Step 4 - Combine Patterns</b>
- Once you have created the separate Jesuit names and Residence patterns lists, they get combined so that Prodigy can load a single patterns list for the first round of annotation. This program loads both patterns lists, concatenates them, and saves them as a new list.

<b>Step 5 - Import Prodigy and Run Initial Annotation</b>
- All of the Prodigy commands happen in the terminal (Steps 5 - 8)
- Import the prodigy package and run the manual annotation with patterns process.

<b>Step 6 - Train Temporary Model</b>
- This allows you to see if the annotating you've been doing puts you on the right path.

<b>Step 7 - Use Temp Model to Continue Annotating</b>
- Once you have trained a temporary model, you can use that model to continue annotating the text. In this way, you are correcting the first guesses of the model rather than having to do it from scratch again.
- If you want to, you can do this step with an additional dataset to keep them separate. The advantage of this is that if something goes wrong during the training process, it won't have messed up the dataset you annotated manually. (I didn't do that for this process because I was working on such a small timeline that I didn't think I would have to come back and fix things for this experiment)

<b>Step 8 - Train Full NER Model</b>

- Once you are happy with the amount of annotations, you can train a full ner model to use to analyze the text.
- I ran Steps 6 and 7 a few times to see how my model was progressing and then added additional training material (like more 1910s and some specific residence types) in order to improve its performance.

<b>Step 9 - Run NER Model Test</b>
- Once you have a final NER model that you're happy with, run it on the text from an individual catalogue and pull out the named entities. You can check this list against the PDF of that catalogue to see how well it did.
- I did this step a few times and then redid Steps 6-8 based on the results (ie. it totally missed a particular residence).

<b>Step 10 - Extract Residence Names</b>
- Once you're happy with your NER model, it's time to start analyzing the catalogues. The first step is to generate and standardize a list of the residences. This is important both because the residence names change over time in the document and because the model sometimes pulls out slightly different versions of the name.
- This program runs the model over each individual catalogue, pulling out the residence entities for each one and saving them to a master list. Then it prints that master list, which I copied into a blank Excel document. I then worked through that document by hand, identify which named entities matched which residences and assigning them a standard name. I also assigned each an ID #, although I didn't end up using that.
    - For the residences that were outside the continental US, I removed them since they were out of scope for this project.
    - For the named entities I couldn't identify, I went through each catalogue individually and tried to match the residence and the named entity.

<b>Step 10.5 - Extract Entities from Catalogues</b>
- Once I made the standardized list of residences, we can use that list to help extract entities from the catalogues in a more orderly way. This step will create the dictionary of Jesuits & where they are stationed in each year that will serve as the foundation for our analysis (once we do some stuff to it).
- This program uses the NER model we created in Step 9 to extract both PERSONs and RESIDs (Jesuits and residences) from each catalogue. It then adds those Jesuits to a dictionary which stores them as the keys. The value for each key is another dictionary which has the full span of years for 1880s and 1915-1925. As we go through each catalogue, it adds the appropriate residence info for each year for each Jesuit. The result is a dictionary organized by person that provides information for where people are stationed.

<b>Step 11 - Export to CSV</b>
- This step is NOT necessary for the final workflow because I ended up using dictionaries, rather than pandas DataFrames, to analyze the data. I've kept this step here just so I can have the process saved.

<b>Step 12 - Build the "By Residence" Dictionary</b>
- Following discussions with Chris, we realized it would be easier to ask the questions we wanted to of the data if we had a dictionary organized by residences rather than by Jesuits. This step translates the existing "by Jesuits" dictionary into a "by residences" one.
- It starts by loading the existing by Jesuit dictionary, then creates a by_resid_dict. It then iterates through the by Jesuits dictionary and adds the Jesuit in the appropriate location and year to each residence. The result is a dictionary where the keys are residences and the values are another dictionary, in which the keys are years and the values lists of Jesuits present in those years.

<b>Step 13a - Analysis: Median Duration</b>
- Now we come to the analysis portion. Chris and I decided on two metrics to measure possible changes in Jesuit transfer patterns. This program looks at the first: median duration, which is a measure of the median amount of time Jesuits spent at a particular residence over the course of the decade. (eg. the median duration for Fordham in the 1880s might be 3.5 years).
- This program loads the by residence dictionary and then checks each academic residence (ignoring Woodstock and residences outside of the continental US). For each residence, it makes a list of all the Jesuits present during that decade. It then checks if each individual Jesuit is present in the first and second year. If they are present, it adds 1 to the counter. As long as the Jesuit continues to be present for pairs of years, it adds 1 to the counter. Once it has worked through the first decade, it adds those durations to a list for the 1880s. Then it takes the median of all of those durations and saves that for each residence. It then does the same for the 1915-1925 decade.

<b>Step 13b - Analysis: Percent of New Jesuits</b>
- This program looks at the second of the two metrics: the percent of new Jesuits at a residence each year (ie. the percent of new Jesuits at Fordham in 1884 might be 35%). While the median duration is a good measure of the time an individual Jesuit might spend at a residence before moving, this indicator shows what percent of the residence as a whole is made up of new Jesuits. This helps give a sense of the experience on a community-wide level.
- This program works similarly to the one in Step 13a. It goes through the by residence dictionary. In this case it compares the list of Jesuits for each year at each residence with the list from the preceding year → finding which Jesuits are only present in the origin year. It then divides that number by the total number of Jesuits at the residence in the origin year to give what percent of Jesuits at that residence are new that year. [Bottom level result] It then finds the average percent of new Jesuits across all of the academic residences for the entire province for each decade and compares the difference.
    - **NOTE**: I did not use results from the Python program for final analysis. Rather, I pulled them into Excel, removed schools that just appear in 1915-1925 and removed St. Joe's in Philadelphia (b/c it's % new in 1880s is off because it isn't present throughout the entire decade).

## Step 14 - Check Statistical Significance

- Once I had the results (listed below), I wanted to ensure they were statistically significant. I pulled the results for both indicators into Excel and used a t-test to check their p-value. Using a one-tail test, I found that the median duration indicator did have a p-value less than the alpha of 0.05 (0.029), but the percent of new Jesuits did not (0.059 not less than 0.05).
    - The percent of new Jesuits is close enough to significant than I think it's worth further exploration.
    - Both of these indicators would benefit from cleaning up the results of the initial Jesuit dictionary,  which I plan to do before publication.
    - The Excel file with the calculations is saved in the results depository.

<h2>Results:</h2>
<b>Average Percent of New Jesuits at Residences</b>

    - 1880s: 35.17%

    - 1915-1925: 31.42%

    - Change: -3.76%

    - P-Value: 0.059 (not significant)

<b>Median Duration of Jesuits at Residences</b>

    - 1880s: 3.01 years

    - 1915-1925: 3.34 years

    - Change: 0.33 years

    - P-Value: 0.029 (significant)
