Introduction:
this code provides a quick way to determine genome location for any drosophila gene in FlyBase.

Using the UI code, fill in your gene of interest and the folder destination. 

Then, run the file "code_geneloc_flybase.py".
This code will use the information provided in the "UI_geneloc_flybase.py" file. 

To run the entire code, open a terminal in the day04 folder and type in:
python UI_geneloc_flybase.py
or, open the code in visual studio and press the "run" button at the top right of the window. 

You will need to install 2 dependencies. To do so, type into your terminal:
uv pip install "name of dependency"
Do this for all dependencies listed in the TOML file





AI questions: 
I asked chatGPT to help write two programs: one as the UI with an input and the other as the actual code that would pull the information from the UI script. I then tried to understand the code that it gave me, and edited with my file names. 
I then used the claude Haiku 4.5 within VSC to trouble shoot the code. I first added a GUI to the UI with the AI. 
Then, I worked with the AI to find the best URL to use for FlyBase, as the code was having problems interacting with FlyBase's API.