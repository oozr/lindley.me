Title: CEFR.AI - Building my First Web App
Date: 2023-08-05
Author: George Lindley

They say that working on projects is far more beneficial for developing your skills as a computer scientist then following along tutorials/doing courses. That's certainly been the case for me as I completed my final project for the CS50 Introduciton to Computer Science course from Harvard Unviersity. 

### The Goal of CEFR.AI
I work at Pearson, which created the Global Scale of English - the GSE. The GSE is a 10-90 framework that is ahead of it's time. More on that in another post. I've always felt that the scale can be more useful to people if it were properly interpreted for specific goals. Enter the goal - a text analyser that gauges how 'hard to read' is a reading passage, by giving a score on the GSE as well as vocabulary that should be pre-taught to the student. 

### Pre-Research
Almost all text analysers on the internet for English use the 'Flesch-Kinclaid' algorithm for rating readability difficulty. You can review the [Wikipedia article](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests) for the full details. In a nutshell, the algorithm takes into account the number of words in a sentence and the number of syllables in a word in order to output an estimated difficulty of the text. Intuitivity, the greater the complexity of the sentences and higher the syllable count per word translates into a higher score. These scores can then be translated into a Common European Framework of Reference band (A1 to C2) that is the typical framework used by language learning teachers.

While at first I was amazed at its simplicity and ability to generate useful results, I was drawn also to the crticism at the end. Indeed, one of the main criticisms of the standard readability agorithms is that they don't take into account 'word difficulty'. Less frequent words don't need to be complex (multiple sylabbles) in order to be difficult to understand for the language learner. 

*"As readability formulas were developed for school books, they demonstrate weaknesses compared to directly testing usability with typical readers. They neglect between-reader differences and effects of content, layout and retrieval aids."*

Consider the example lifted from the Wikipedia article: 

*"Cwm fjord-bank glyphs vext quiz."*

A score of 100 on the Flesch-Kincaid would result in a A1 (begniner) CEFR result, but certainly beginners (and advanced learners!) would have a hard time with a text containing such sentences. It quickly became apparent to me that I can address this issue and grade texts more accurately than other text analysers by incorporating the GSE wordlist, comprising of 35,000 words. These words have all bee scored in level of difficulty - frequency of occurance in the langauge and usefulness of the word. High frequency and high usefulness means this is a word that a learner should learn, and thus most Beginners will know - and thus a low score. A combination of the Flesch-Kincaid algorithm (this is still important) and the GSE wordlist score could create an app very useful in specific for language learning teachers.

### Building the App
While creating the app hasn't been a linear process, below are the major steps and challenges that I've incurred in creating this project. 

English teachers interested in how the algorithm works acan skip to stage 3: The Algorithm where we detail how we score a text on the GSE - what makes a text 'hard to read'.

#### Stage 1: Acquiring the GSE 10-90 List of Vocabulary
The GSE 10-90 wordlist, comprising of 35,000 words is freely available on the internet, and is part of the commons licensing, as research developed alongside the CEFR project. However, on Pearson's website, the words only appear 10 words at a  time, across 3,480 pages!!! 
You can view the full list on the [GSE website](https://www.english.com/gse/teacher-toolkit/user/vocabulary?page=1&sort=gse;asc&gseRange=10;90&audience=GL). That's a lot of copying and pasting and clicking to make one hate the internet for eternity! Which is why the good computer scientist uses code to automate repetitive tasks. 

Enter, 'web-scraping'. A mini project within a project to create a web bot to scrape the website i.e. copy the words off the page into a database, and then click on 'next' until the task is complete. I decided to tackle this project first, because without the list my text analyser wouldn't have the capabilities to address the issues found with other text analysers.

The package I used to create a webscraper is called 'Selenium' and is available for Python. This package is traditionaly used for testing website functionality - hence the additional capabilities of navigating a website, making it perfect for the task. I worked with a friend on the coding, our final project is published here. Deployed over night, in total it took the web bot around 15-16 hours to scrape all 35,000 words into a Sqlite3 database while I was away from the computer.

#### Stage 2: Creating the Flask App & Deploying Online
Database in hand, I knew the project was viable and I could start with creating the web app. As we practiced creating Flask applications in the CS50 Harvard University Computer Science course this was my first choice for this project. Flask is a another Python framework that incorporates Python server-side code to render HTML templates to the client. Using Python code, we can also process the requests (analyse texts) by running an algorithm on the server-side and looking up the words from the text in the SQLite3 database. The focus of this stage was not to create the project all in one step, but to have a working web app that we can then develop and refine the text analyser algorithm (stage 3).

Once I created the web app using my VS Code text editor I synced the code to github.com, creating an open project as you can see here. The next stage was completely new to me - deploying the code into a fully functional web app available to anyone online. After a quick search, I heard a lot of good things about [Railway.app](https://railway.app) which allows you to connect to a Github repository for a quick setup of the website. There is a monthly cost associated by using Railway.app, but I was blown away of how easy it was to deploy the website online, connect it to a unique URL (cefr.ai bought through GoDaddy) and automatically receive an SSL certificate for security. I now have a working website, which takes a user's text and feeds back a GSE score. The algorithm I used to generate the score was very basic and will be developed and refined in the next step.

#### Stage 3: Text Analyser: The Algorithm
This is the meat of the project, as the whole point of my site is to deliver an accurate score for the readability of a user's text. First I implemented the Flesch-Kincaid scoring as a principle component of the algorithm. Here is the well known algorithm:

**206.835 - 1.015(total words/total sentences) - 84.6(total syllables/total words)**

 My text analyser was already as good as the majority of the text analysers on the internet. The second part is to analyse the vocabulary by looking them up in the SQLite3 table of 35,000 words to get an average score for the vocabulary difficulty. I then combine the two scores at a 2:1 ratio (placing more importance on the Flesch-Kincaid index) to produce a final GSE score. But hold up a moment, let's look at the process to generate the vocabulary score:

 1. Each word is 'lemmatized' using Spacy Natural Language Processing pipeline. A word such as 'learning' is processed by the pipeline with the return root value of 'learn' that is then used to cross-reference with the GSE 35,0000 wordlist. We use lemmas instead of words, because the root words appear in the dictionary, otherwise words like 'doctors' (plural) wouldn't return the score for 'doctor' (the singular for is found in the dicitionary).
 2. Once lemmatized, the root form is then passed into an SQL query to find the corresponding GSE score in the dictionary database. All words from the user's text found in the dictionary of GSE 35,000 words are added up and divided by the number of found returns, returning the average score of the difficulty of the vocabulary of the text. 
 3. The words not found in the dictionary are saved in a list and returned to the user as part of their score report. This is to combat a drawback I found in other analysers on the internet that don't show which words were analysed. I think it's important to make the user aware of any none words, partly to help them understand their text better, and partly to show full transparency for accuracy - the user understands which words do not impact the score. Cleaning up this list was a challenge, as we had to remove all sorts of punctuation, spacing, proper nouns ('Manchester' is not in the dictionary but isn't a 'none-word') and numbers (digits and text form).

 As mentioned before, we then gave a 2:1 weighting to the Flesch-Kincaid score to produce a final GSE score returned to the user. This was because the word complexity was already partially taken into account by the inital Flesch-Kincaid algorithm - see above 'total syllables'. 
 
 Additionally, now we know the score of the text, we can also provide the user with the words from the text that are above the level. We do this so we can suggest to the teacher words that should be pre-taught. A teacher can then give an '55' text to a student at that level, and advise on the 6 words that appear in the text above this level for them to find out their meaning before they attempt the reading.

 Going forward, the algorithm should be further refined based on experience and feedback of users.

#### Stage 4 (Future): Integration of AI
CEFR.AI text analyser already offers a lot of unique benefit to teachers conducting their classes. With the new AI tools coming online, notably Large Language Models (AI) I feel there is great scope to improve it further. The first upgrade I would like to implement is an additional feature once the text has been analysed, called 'create my lesson'. The user clicks on this button to then receive 5-10 multiple choice questions about the text, along with the answer and three distractors - so four options for the student to choose from. The teacher can then click, 'download my less' to receive a word document with:
1. The text they initially inputted
2. The score and the words to pre-teach (words above the level of the text)
3. 5-10 multiple choice questions (with the answers hidden on the next page)

Currently I am experimenting with different APIs such as OpenAI, and APIs available on HuggingFace to power this capability. The first API call is needed to generate the question and answer, the second API call is needed to generate the additional three disctractors (wrong answers, but not so wrong that the learner would never choose them). 