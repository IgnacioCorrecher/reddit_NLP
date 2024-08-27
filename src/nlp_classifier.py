import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm.notebook import tqdm

nltk.download('stopwords')
nltk.download('wordnet')

try:
    df = pd.read_csv('../data/comments.csv', index_col='Id', skip_blank_lines=True)
    df = df.dropna()
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = re.sub(r'http\S+|www.\S+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[^A-Za-z\s]', '', text, flags=re.IGNORECASE)
    text = text.lower()
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)

df['Processed_Comment'] = df['Comment'].apply(preprocess_text)

#TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=5000) 
X = vectorizer.fit_transform(df['Comment'])

model_name = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=0)

def get_sentiment_batch(texts):
    try:
        results = sentiment_pipeline(texts, truncation=True, max_length=512, batch_size=32, device=0)
        return [result['label'] for result in results]
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return ["NEUTRAL"] * len(texts)

# Define batch size
batch_size = 512

# Initialize an empty list to store all sentiments
all_sentiments = []

# Create a tqdm progress bar for the entire dataset
with tqdm(total=len(df), desc="Processing comments") as pbar:
    for i in range(0, len(df), batch_size):
        # Get the current batch
        batch_texts = df['Processed_Comment'].iloc[i:i+batch_size].tolist()
        
        # Process the batch
        batch_sentiments = get_sentiment_batch(batch_texts)
        
        # Extend the list of all sentiments
        all_sentiments.extend(batch_sentiments)
        
        # Update the progress bar
        pbar.update(len(batch_texts))

# Assign sentiments to DataFrame
df['Sentiment'] = all_sentiments


df_output = df[['Username', 'Subreddit', 'Sentiment']].copy()

# Reset the index to turn the comment ID into a column
df_output = df_output.reset_index()

# Rename the index column to 'Comment_ID' for clarity
df_output = df_output.rename(columns={'Id': 'Comment_ID'})

# Reorder the columns as per your request
df_output = df_output[['Comment_ID', 'Username', 'Subreddit', 'Sentiment']]

# Save to CSV
output_path = '../data/comments_sentiment_summary.csv'
df_output.to_csv(output_path, index=False)

print(f"CSV file has been created at: {output_path}")