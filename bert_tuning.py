from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import json
import torch
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=399)  

device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
model.to(device)

with open('/Users/gianfrancopuca/Desktop/GH2/src/mydetails.json', 'r') as f:
    data = json.load(f)


texts = []
labels = []
label_map = {}  
current_label = 0

for intent in data['intents']:
    if intent['tag'] not in label_map:
        label_map[intent['tag']] = current_label
        current_label += 1
    for pattern in intent['patterns']:
        texts.append(pattern)
        labels.append(label_map[intent['tag']])


print("Label Map:", label_map)

inputs = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')


print(inputs['input_ids'].shape) 

train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size= 0.2, random_state= 42)

train_encodings = tokenizer(train_texts, padding= True, truncation = True, return_tensors = 'pt')

val_encodings = tokenizer(val_texts, padding = True, truncation = True, return_tensors = 'pt')

class MyDataset(Dataset):
    def __init__(self, encodings, labels, device):
        self.encodings = {key: val.to(device) for key, val in encodings.items()}
        self.labels = torch.tensor(labels).to(device)
        self.device = device

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = MyDataset(train_encodings, train_labels, device)

val_dataset = MyDataset(val_encodings, val_labels, device)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    logits = torch.tensor(logits).to(device)
    predictions = torch.argmax(logits, dim= -1)
    accuracy = accuracy_score(labels, predictions.cpu())
    return {"accuracy": accuracy}



training_args = TrainingArguments(
    output_dir='./results',          
    num_train_epochs=10,              
    per_device_train_batch_size=16,   
    per_device_eval_batch_size=16,    
    warmup_steps=2000,                
    weight_decay=0.02,               
    logging_dir='./logs',            
    logging_steps=10, 
    evaluation_strategy= "epoch"            
)



trainer = Trainer(
    model=model,                     
    args=training_args,              
    train_dataset=train_dataset,
    eval_dataset= val_dataset,
    compute_metrics= compute_metrics
)


trainer.train()


model.save_pretrained('./fine-tuned-model')
tokenizer.save_pretrained('./fine-tuned-model')




