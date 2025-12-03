# file_conversion_web_app
A simple web app that coverts PDF files to Markdown files. (more formats coming soon!)

I created this as a quick add-on tool that I needed for another project.

Utlilizes Python and its "Markitdown" library for the main app and file type conversion logic. The flask library as well as HTML, CSS, and JavaScript were used to create the actual web app UI.

Installation/Set-Up:
1. Download the following files:
   a. app.py
   b. converter.py
   c. styles.css
   d. script.js
   e. index.html
   f. requirements.txt
2. Create this file structure -
     main_directory/
     |-- app.py
     |-- converter.py
     |-- requirements.txt
     |-- static/
     |   |-- css\
     |   |   |-- styles.css
     |   |-- js\
     |       |-- script.js
     |-- templates\
     |   |-- index.html
     |-- outputs\
     |__ uploads\
   *notes: The outputs and uploads directories should be auto-created upon first run of the web app.

Running/Usage Instructions:
1. Create/activate you virtual environment (you will need Python 3.8 or higher) and run the command: pip install -r requirements.txt
2. Open the "app.py" file and run it.
3. A link to the Flask development server should appear in you terminal, paste this link into your browser. (Ex.: Running on http://###.#.#.#:####)
4. Click on the "upload" button to upload a pdf file. (only one file at a time)
5. Press the "convert" button to convert you pdf file to a markdown file. A text box will appear directly below the "convert" button with a preview of your file in the markdown format. You can make any neccessary edits here.
6. Scroll down and press the "download" button to download your final markdown file.
