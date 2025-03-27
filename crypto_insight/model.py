# Project: Crypto Insight 1.0
# Description: This file contains the code for extracting text from PDF files, preprocessing the text, and performing sentiment analysis and named entity recognition on the extracted text. It also includes a class for retrieving answers based on user queries using the BM25 algorithm.
# Authors: Amit Lakhera, Varsha, Pardipta, Krishnopriya, Vikas, Aditi, Laxmi 
# Date: 26-Feb-2025
# Version: 1.0
# Python Version: 3.8
# Libraries Used: pdfplumber, nltk, string, spacy, numpy, sklearn, textblob, rank_bm25
# Input: PDF files containing text
# Output: Extracted text, cleaned text, sentiment analysis, named entities, and answers to user queries
# Usage: Run the script and enter queries about cryptocurrencies to get relevant answers from the extracted text.
# Note: The PDF files should be placed in the 'crypto_insight' folder in the same directory as this script.
# The extracted text, cleaned text, and answers will be displayed in the console.
# The sentiment analysis and named entities will be printed for each user query.    
# The script will continue to prompt for user queries until 'STOP' is entered.


# Import necessary libraries
import pdfplumber
import nltk
import string
import spacy
import numpy as np 
import re
import unidecode
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
from rank_bm25 import BM25Okapi
from spacy.pipeline import EntityRuler
from tqdm import tqdm
from nltk.stem import WordNetLemmatizer, PorterStemmer

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

# Step 1: Extract text from PDF files
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # Ensure the extracted text is not None
                text += page_text + "\n"
    return text

# Get the current working directory
current_directory = os.getcwd()

# Get the relative path (which is just '.' for the current directory)
relative_path = os.path.relpath(current_directory, os.getcwd())

# List of PDF file paths
pdf_files = ['Crypto_Article1.pdf','Crypto_Article2.pdf','Crypto_Article3.pdf', 'Crypto_Article4.pdf','Crypto_Article5.pdf']  

# Extract text from multiple PDFs
all_text = ""
all_sentences = []

# Iterate through each PDF file and extract text
for pdf_path in pdf_files:
    file_path = "".join([relative_path, '\\crypto_insight\\' ,pdf_path])
    all_text += extract_text_from_pdf(file_path) + "\n"
    
# Step 2: Preprocess the extracted text
if all_text:
    sentences = sent_tokenize(all_text)  # Sentence tokenization
    all_sentences.extend(sentences)

# Save the extracted text to a file
with open("output.txt", "w", encoding="utf-8") as text_file:
    text_file.write("\n".join(all_sentences))  # Join sentences with new lines

# Load stopwords
stop_words = set(stopwords.words("english"))

# Initialize lemmatizer and stemmer
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# List of crypto-related terms to keep intact
crypto_terms = {"bitcoin", "btc", "ethereum", "eth", "blockchain", "crypto", "nft", "defi", "web3", "dao", "altcoin","solana","hamster","dogecoin"
                "stablecoin", "smart contract", "staking", "mining", "wallet", "coin", "token", "airdrop", "fomo", "hodl"}

# preprocess_text function to clean and tokenize the text
def PreProcessText(text):
    # Convert to lowercase
    text = text.lower()

    # Remove unwanted special characters (like â€™, emojis, etc.)
    text = unidecode.unidecode(text)  # Normalize special characters
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # Remove non-ASCII characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove punctuations except spaces

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    cleaned_words = []

    for word in text.split():
        if word in crypto_terms:  # Preserve crypto-related words
            cleaned_words.append(word)
        elif word not in stop_words:
            stemmed_word = stemmer.stem(word)  # Apply stemming
            lemmatized_word = lemmatizer.lemmatize(stemmed_word)  # Apply lemmatization
            cleaned_words.append(lemmatized_word)
    return cleaned_words

# Read the extracted text
with open("output.txt", "r", encoding="utf-8") as file:
    raw_text = file.read()

# Apply preprocessing
cleaned_tokens = PreProcessText(raw_text)

# Save the cleaned text as a new file
with open("cleaned_output.txt", "w", encoding="utf-8") as file:
    file.write(" ".join(cleaned_tokens))

# Step 3: Process and push the cleaned text
def ProcessAndPush(text: str):
    #sentences = sent_tokenize(text)  # Sentence splitting
    # Using TF-IDF embeddings as nltk doesn't have built-in word vectors
    vectorizer = TfidfVectorizer(max_features=5000)
    embeddings = vectorizer.fit_transform(sentences).toarray()
    # Simulating "pushing" data (storing embeddings)
    data_store = {sent: vec for sent, vec in zip(sentences, embeddings)}
    return data_store  # This is where you'd actually push to a database

# Step 4: Added for Sentiment Analysis using TextBlob - Amit Lakhera

# Function to analyze sentiment using TextBlob
def AnalyzeCryptoSentiment(text):
    blob = TextBlob(text)
    score = blob.sentiment.polarity
    if score > 0:
        return "Positive", score
    elif score < 0:
        return "Negative", score
    else:
        return "Neutral", score



# Load the pre-trained SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define a custom entity list for crypto-related terms
custom_crypto_entities = [
    {"label": "CRYPTOCURRENCY", "pattern": "Bitcoin"},
    {"label": "CRYPTOCURRENCY", "pattern": "Ethereum"},
    {"label": "CRYPTOCURRENCY", "pattern": "Solana"},
    {"label": "CRYPTOCURRENCY", "pattern": "Dogecoin"},
    {"label": "CRYPTOCURRENCY", "pattern": "Cardano"},
    {"label": "EXCHANGE", "pattern": "Binance"},
    {"label": "EXCHANGE", "pattern": "Coinbase"},
    {"label": "EXCHANGE", "pattern": "Kraken"},
    {"label": "EXCHANGE", "pattern": "FTX"},
    {"label": "DEFI_PLATFORM", "pattern": "Uniswap"},
    {"label": "DEFI_PLATFORM", "pattern": "Aave"},
    {"label": "DEFI_PLATFORM", "pattern": "Compound"},
    {"label": "NFT_PLATFORM", "pattern": "OpenSea"},
    {"label": "NFT_PLATFORM", "pattern": "Rarible"},
    {"label": "TOKEN", "pattern": "USDT"},
    {"label": "TOKEN", "pattern": "USDC"},
    {"label": "TOKEN", "pattern": "DAI"},
]

# Named Entity Recognition
def ExtractCryptoEntities(text):
    # Extract crypto-related entities from text
    doc = nlp(text)
    
    # Include both default and custom entities
    crypto_entity_types = [
        "ORG", "MONEY", "PRODUCT", "GPE", "LAW", "EVENT", 
        "CARDINAL", "PERCENT", "DATE", "TIME",
        "CRYPTOCURRENCY", "EXCHANGE", "DEFI_PLATFORM", "NFT_PLATFORM", "TOKEN"
    ]
    entities = {ent.text: ent.label_ for ent in doc.ents if ent.label_ in crypto_entity_types}
    return entities

# Step 5: Answer Retrieval using BM25
class CryptoAnswerRetrieval:
    def __init__(self, sentences):
        self.sentences = sentences
        self.tokenized_sentences = [PreProcessText(sent) for sent in sentences]
        self.bm25 = BM25Okapi(self.tokenized_sentences)
    
    #  Search function to retrieve answers based on user query
    def search(self, query, top_n=3):
        query_tokens = PreProcessText(query.lower())
        bm25_scores = self.bm25.get_scores(query_tokens)
        ranked_answers = sorted(zip(self.sentences, bm25_scores), key=lambda x: x[1], reverse=True)
        return ranked_answers[:top_n]

# Process user query
def ProcessUserQuery(user_query):

    # Preprocess the user query
    cleaned_data = " ".join(cleaned_tokens)
    
    # Perform sentiment analysis on the cleaned data
    data_store = ProcessAndPush(cleaned_data)
    
    # Perform sentiment analysis on the user query
    sentiment, score = AnalyzeCryptoSentiment(user_query)
    
    # Extract named entities from the user query
    retriever = CryptoAnswerRetrieval(list(data_store.keys()))
    
    # Retrieve top-ranked answers using BM25
    ranked_answers = retriever.search(user_query, top_n=3)
    
    print(f"\nUser Query: {user_query}\n")
    print(f"\nUser Query Sentiment Score: {score})\n")
    print("Top-ranked Answers:")
    
    for i, (answer, bm25_score) in enumerate(ranked_answers):
        print(f"{i+1}. {answer[:500]}... (BM25 Score: {bm25_score:.2f})")
    return ranked_answers

# Main loop to process user queries
condition = 'none'
while condition.lower() != 'stop':
    print("Please write 'STOP' to exit !!")
    user_query = input("Enter your query about crypto: ")
    condition = user_query
    if condition.lower() == 'stop':
        break
    ranked_answers = ProcessUserQuery(user_query)