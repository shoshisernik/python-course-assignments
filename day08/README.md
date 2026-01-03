Explanation of code

This code takes a dataset from kaggle of thousands of recipes and organizes them into dietary categories. My goal with this project is to compare different diets and try to make some general claim about the nutritional content someone on a particular diet may get. I am a vegan, so it is interesting for me to see on average how much protein, calories, fats, etc. I am getting relative to other people who eat dairy, meat, or fish. 






Dependencies: 
numpy, pandas, matplotlib, seaborn, kaggle

to install: uv pip install numpy pandas matplotlib seaborn kaggle


Kaggle setup: 

1. Creat a Kaggle account and get your API key
    -create the account on kaggle.com, then follow these steps: 
        1. click on your profile in the top right corner
        2. go to settings
        3. scroll to API section
        4. click "generate new token"

2. Set up your Kaggle API
    1. install the Kaggle python package: uv pip install kaggle
    2. create a kaggle.json file in this folder and put this in it: 
        -{
  "username": "YOUR_KAGGLE_USERNAME",
  "key": "YOUR_API_KEY"
}
    3. make sure the kaggle.json file is saved to the right location for your operating system

3. test that the setup worked
    -test by typing into terminal: kaggle datasets list

    -you should see a list of datasets. 
4. You can then download any particular dataset that you wish to analyze or just run the code provided in this folder, which already does this
7. do not commit kaggle.json to GitHub, instead add it to .gitignore