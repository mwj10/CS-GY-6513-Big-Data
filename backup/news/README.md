# Getting Started

First create a new file `.env` and insert the following after getting the key from Farhan:
```
NYT_KEY=ask-farhan
MEDIA_STACK_KEY=ask-farhan
```

In order to run a cold start process of extracting, transforming and loading the data for sentiment analysis, open up the `main-script.ipynb` and run the cells by following the instructions laid out there. The cold start process is the assumption that our application goes live for the first time, and there aren't any historical data stored.