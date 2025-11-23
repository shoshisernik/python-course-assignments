Introduction:
this code provides a quick way to determine any orthologs of a given fly gene.

Using the UI code, fill in your gene of interest (you will need the FBgnId), the other organism to which you will compare your gene of interest, and the folder destination. 


To run the entire code, open a terminal in the day04 folder and type in:
python ortholog_ui.py
or, open the code in visual studio and press the "run" button at the top right of the window. 

You will need to install several dependencies. To do so, type into your terminal:
uv pip install "name of dependency"
Do this for all dependencies listed in the TOML file





AI questions: 
Questions asked to ChatGPT o3: "can you please write me 2 codes. the first, a UI with a GUI that asks for the FBgnId of a gene in FlyBase.org, a browse button to select the location of where the output file will be saved/downloaded, and a pulldown menu with the option to select human, mouse, yeast, c. elegans, and various other model organisms. the second code will have the business logic and will pull the information from this ui. it needs to then search FlyBase and return the orthologs of the fly gene given for whatever model organism was selected. the file in which this data is put into can be an excel or csv. i am working in python 3.13"
"this does not work.... i am getting an error message asking me to enter a flybase id, even though i did"