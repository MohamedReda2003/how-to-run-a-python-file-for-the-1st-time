
# Run the python code on your machine
(The tutorial is for Windows users)

First of all you have to install Python to your machine. I recommand the following video for this step: https://www.youtube.com/watch?v=4iUJZEa2xP8

Let's say that you have already downloaded the python file you want to run, first we move it to a folder that we will call it `new_work` then open it on VScode, after that you click on `Terminal` then click on `New Terminal`

![new terminal](https://cdn.discordapp.com/attachments/1087001413101559829/1265983536460992543/image.png?ex=66a37e8b&is=66a22d0b&hm=99f0044546b39d756c12c6cc550e2dcfc9074c87ab01d99fe75646eade81c9ea&)

After starting the new terminal, you will navigate to the folder path (make sure to write the path of your own folder, for me, I have my folder in the path shown on the image `E:\new_work`)
![navigate to the path](https://cdn.discordapp.com/attachments/1087001413101559829/1265984300277567519/image.png?ex=66a37f42&is=66a22dc2&hm=a207ae7db56981dcccb99983f7c08dea7c85a24e336fb115f81902c5a1a9d65b&)

### Now we will install the requirements
That is why we have to put the `requirements.txt` file in the same folder.
we run the command: `pip install -r requirements.txt`
![install requirements](https://cdn.discordapp.com/attachments/1087001413101559829/1265991074032386121/image.png?ex=66a38591&is=66a23411&hm=5dc5ebd08a3b21997dea958e29813bfb5f14acd51cc969133f01d322a7351d0c&)
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


