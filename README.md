
# Run the python code on your machine
(The tutorial is for Windows users)

First of all you have to install Python to your machine. I recommand the following video for this step: https://www.youtube.com/watch?v=4iUJZEa2xP8

Let's say that you have already downloaded the python file you want to run, first we move it to a folder that we will call it `new_work` then open it on VScode, after that you click on `Terminal` then click on `New Terminal`

![new terminal](https://github.com/user-attachments/assets/0bd58b6a-ba40-42ad-84c1-6c95ef596596)

After starting the new terminal, you will navigate to the folder path (make sure to write the path of your own folder, for me, I have my folder in the path shown on the image `E:\new_work`)
![navigate to the path](https://github.com/user-attachments/assets/5dbc7895-ffd8-4bb6-a586-c538870af5a3)

### Now we will install the requirements
That is why we have to put the `requirements.txt` file in the same folder.
we run the command: `pip install -r requirements.txt`:

![install requirements](https://github.com/user-attachments/assets/fcb10c93-23c2-4d65-a041-442e6cdfb1de)

It will take some time to install all the required libraries to assure a good execution of the code later.

# If you encounter an error like:
 ```
 pip : The term 'pip' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
At line:1 char:1 
```
run the following commands:
## 1:
`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
## 2:
`python get-pip.py`
## If you have run the previous commands and still get the same error:
I recommand to watch this video, and follow the steps in it: https://www.youtube.com/watch?v=ENHnfQ3cBQM

(You will have to close vscode if you have this issue, so when you reopen it, first you will navigate to the folder path)

then go back and install the requirements 

# Finally run the script:
run the command:
`python extract_tabular_data_from_invoice.py`
# To build a python executable file:
first of all we have to start a new virtual environment: 
```
python -m venv table_extractor
table_extractor/Scripts/activate
```
then install the dependencies :
```
pip install -r requirements.txt
pip install auto-py-to-exe
```
if you get any error when running the previous command you can run the following:
```
pip install pdfplumber==0.11.0 camelot-py==0.11.0  pandas==2.2.2 tabulate flet==0.22.1 opencv-python auto-py-to-exe
```
then run the command:
```
auto-py-to-exe
```
Then you can just configure your app and here we go!


