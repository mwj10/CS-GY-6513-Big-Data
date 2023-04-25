from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import datetime

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

def entitiesFromNER(ner_results):
  res = []
  for i in range(len(ner_results)):
    if ner_results[i]['entity'] == 'B-ORG':
      org = ner_results[i]['word']
      idx = i
      while idx+1<len(ner_results) and ner_results[idx+1]['entity'] == 'I-ORG':
        c = 0 #we introduce a character level pointer, and check whether # is there
        while ner_results[idx+1]['word'][c] == "#":
          c+=1 #if so, we increament the c pointer
        if c>0: #if a # instance occured, our c pointer will have incremented
          org+= "" + ner_results[idx+1]['word'][c:] #so instead of treating it as a new word, we append it to org for characters after c pointer
        else:
          org+= " " + ner_results[idx+1]['word']
        idx+=1
      res.append(org)
  return res

nlp = pipeline("ner", model=model, tokenizer=tokenizer)
def extractFromNews(news):
  ner_results = nlp(news)
  entities = entitiesFromNER(ner_results)
  return news, entities

def formatDate(date):
    # convert input string to datetime object
    dt = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')

    # format datetime object into desired string format
    output_string = dt.strftime('%m-%d-%Y')
    
    return output_string