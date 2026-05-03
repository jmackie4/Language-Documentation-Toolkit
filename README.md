# Language Documentation Toolkit

Langauge Documentation Toolkit (LDTK) is a python package for speeding up data annotation for language documentation projects and other projects interested in creating linguistic resources from unannotated corpora of parallel texts!

As of right now, LDTK creates the following resources from a loaded corpus:
1. Glossed Version of the Corpus
2. Tokenized Version of the Corpus
3. Initial Glosses of Each Word in the Corpus

In addition to creating the resources stated above, users can also use LDTK to search for specific information throughout the corpus. Searchable information includes word concordances, gloss statistics for words, words that match a specific sub-word pattern.

Finally, LDTK offers potential split points for given words to help with word stemming and morphological segmentation tasks!
## **How To Get Started Using LDTK**
In order to use LDTK, you'll need to make sure you meet all the following requirements:
1. A corpus of parallel texts that is a folder on your desktop. Seriously, the folder needs to be on your desktop!
2. Each file in the folder must be a plaintext (.txt) file. In addition, the lines in all files need to follow the following format:
   

    Source Language Line
    Target Language Line
2. As of May 3rd, the target language must be English due to LDTK making use of the spacy library's english language model. This will be changed at a later date to include other languages supported by spacy.
3. All of the dependencies in the requirements.txt file must be installed too!

## **What Do I Need to Get Started???**

In order to use TCP, you'll need to make sure the corpus of parallel texts meets the following requirements:
1. One of the languages must be English! If you're seeing this requirement, then that means I haven't modified TCP to be usable with any language pair!
2. The corpus of parallel texts you want to use with TCP must be a directory (folder) with two sub-directories in it. In addition, the two sub-directories must meet some requirements:
4. The sub-directories must contain the same number of plaintext files, and the plaintext files must have the same names between the two sub-directories
5. The files within a sub-directory must all be written in the same language
6. A regular expression pattern to give TCP that'll tokenize the source languages

Also make sure that you have all the necessary dependencies installed, you can find those in the requirements.txt file! 


## **Getting Started Using LDTK:**
1. First just run the main script using the following in the terminal
```
python3 -m 'your/specific/path/Language-Documentation-Toolkit'
```
2. You'll then see this prompt, insert the name of the folder that serves as your corpus! Don't worry it's not case sensitive!
```angular2html
Please enter the name of the folder that holds your corpus:
```
And with that you'll be in the LDTK main menu! It might take a minute to load everything up, especially if you have a larger corpus so please be patient!
```angular2html
0: get glosses
1: get concordances
2: use stemmer
3: export resources
Please enter what you want to do by typing the name of the option:
```
**Now if you want to exit out of LDTK, just make sure you're on the main menu and type exit!!!**

For every option besides export resources, you'll be sent to that specific app's menu. You can exit each individual apps meny by typing exit, and you'll be sent back to the main menu!
Each of these options allows you to provide a list of queries you want to search.

**Each query for a one of LDTK's apps must be separated by a comma, that's important, don't forget it!**

## **Exported Resources from LDTK!!**
LDTK is able to actually make resources for you! Just note that LDTK will create a folder on your desktop titled 'LDTK Created Resources' that will store everything it creates.
For now, LDTK creates one excel sheet that holds the tokenized version of your copus, the glossed version of your corpus, the vocabulary list and the gloss statistics of each vocabulary word!
I'm working on making sure that the created resources are much easier to edit and change, so please be patient. And sorry for it being in an excel sheet for now.


## **Future Updates and Features To Be Added**
Please note that LDTK is a one-person project. I'm unfortunately a busy person, so I can't add things in as quickly and continuously as I'd like to.
With that being said, I want to make sure that LDTK makes the language data annotation and resource creation process as painless and simple as possible.

I'm working to accomplish that goal by adding more relevant features, ensuring the resources LDTK creates are in-line with common genre expectations and making it as accessible and easy to use as possible.
That takes time though, so please be patient as I keep improving LDTK. 

Ok now that that's out the way, here's what's coming in the near future:
1. Allowing for word documents (.doc) and (.docx) files to be included in the corpus
2. Formatting the glossed version of the corpus in the standard Glossed Text format
3. Allowing users to edit the LDTK created resources to iteratively improve LDTK's created resources so it grows as the users complete more work
4. Letting users retrieve specific texts
5. A more robust search system that handles misspelled words
6. An improved word stemmer that proposes options for how each word could be segmented and stemmed
7. Based on number 6, an initial list of morphemes in the source language
6. A similar word finder
7. A POS Tagger
8. An improved word compendium that serves as a mini-dictionary. However, this will be created once the POS tagger and full stemmer are implemented.

## **Contact Information and Helping Out with LDTK!!**
**my email: jmackie4@asu.edu**

If you have any questions, or problems using LDTK, please reach out to me (Justin) at jmackie4@asu.edu!
Seriously, if you have any questions or problems at all, please never hesitate to reach out. I'm always happy to help solve any issues or questions.

In addition feel free to reach out if you have any suggestions on improvements to LDTK. If you have features you want added, or a specific experience you want improved, I really do want to hear your idea(s)!

Also if you'd like to help out with developing LDTK, feel free to reach out for now. I'll make a guide on contributing to the project at a later date, so for now just email me.

Oh yea, btw LDTK is actually just the better version of the Takelma Corpus Project (TCP) project I made awhile ago. So i'm sunsetting that project and won't be updating that anymore.