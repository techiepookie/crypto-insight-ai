from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pdfplumber
import nltk
import string
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from rank_bm25 import BM25Okapi
from textblob import TextBlob
from collections import defaultdict

# Initialize Flask app
def create_app():
    app = Flask(__name__)
    CORS(app)

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Helper functions and classes
def extract_text_from_pdf(*pdf_paths):
    """Extract text from multiple PDFs and combine into a single string."""
    text = ''
    for pdf_path in pdf_paths:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            print(f"Processed: {pdf_path}")
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
    return text
class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.update({'crypto', 'bitcoin', 'blockchain', 'solana'})

    def clean_text(self, text):
        translator = str.maketrans('', '', string.punctuation.replace('.', ''))
        return text.lower().translate(translator).replace('\n', ' ')

def tokenize_sentences(text):
    try:
        return sent_tokenize(text)
    except:
        return [s.strip() for s in text.split('. ') if s]

# Enhanced CryptoNewsQA class
class EnhancedCryptoQA:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.sentences = []
        self.bm25_index = None
        self.initialize_system()
    
    def initialize_system(self):
        try:
            # List all PDFs to process
            pdf_files = [
                'crypto_news_1.pdf',
                'crypto_news_2.pdf',
                'dogecoin_report.pdf',
                'ethereum_whitepaper.pdf',
                'bitcoin_analysis.pdf',
                'solana_overview.pdf',
                # Add more PDFs here
            ]
             #Extract and combine text from all PDFs
            raw_text = extract_text_from_pdf(*pdf_files)
            cleaned_text = self.preprocessor.clean_text(raw_text)
            self.sentences = tokenize_sentences(cleaned_text)
            
            if not self.sentences:
                raise ValueError("No text extracted from PDFs")
                
            self.create_index()
            print(f"System initialized with {len(self.sentences)} sentences from {len(pdf_files)} PDFs")
        except Exception as e:
            print(f"Initialization error: {e}")
            self.sentences = []
            self.bm25_index = None

    def create_index(self):
        """Create BM25 index from tokenized sentences."""
        tokenized_sentences = [sentence.split() for sentence in self.sentences]
        self.bm25_index = BM25Okapi(tokenized_sentences)
        print("BM25 index created successfully")
    def create_index(self):
        tokenized_sentences = [sentence.split() for sentence in self.sentences]
        self.bm25_index = BM25Okapi(tokenized_sentences)

    def get_answers(self, question):
        query = self.preprocessor.clean_text(question).split()
        scores = self.bm25_index.get_scores(query)
        top_indices = np.argsort(scores)[-3:][::-1]
        return [self.sentences[i] for i in top_indices if scores[i] > 0]

    def analyze_sentiment(self, text):
        """Simple sentiment analysis using TextBlob"""
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
    
    def extract_entities(self, text):
        """Basic entity extraction (custom implementation)"""
        entities = {
            'cryptos': {'bitcoin', 'ethereum', 'solana', 'cardano','dogecoin'},
            'companies': {'coinbase', 'binance', 'kraken','uniswap','chainlink'}
        }
        
        found = {
            'cryptocurrencies': [],
            'organizations': [],
            'numbers': []
        }
        
        for word in text.split():
            # Detect cryptocurrency mentions
            if word in entities['cryptos']:
                found['cryptocurrencies'].append(word.title())
            # Detect company mentions
            elif word in entities['companies']:
                found['organizations'].append(word.title())
            # Detect numeric values
            elif word.isdigit() or (word.replace('.', '', 1).isdigit() and word.count('.') < 2):
                found['numbers'].append(word)
        
        return {k: list(set(v)) for k, v in found.items()}
    
    def generate_insights(self, sentences):
        """Generate simple insights from matched sentences"""
        insights = {
            'sentiments': [],
            'entities': defaultdict(list),
            'trends': []
        }
        
        for sentence in sentences:
            # Sentiment analysis
            polarity = self.analyze_sentiment(sentence)
            insights['sentiments'].append(polarity)
            
            # Entity extraction
            entities = self.extract_entities(sentence)
            for key, values in entities.items():
                insights['entities'][key].extend(values)
            
            # Trend detection (simple keyword matching)
            trend_triggers = {
                'rising': ['increase', 'rise', 'up', 'bullish'],
                'falling': ['decrease', 'drop', 'down', 'bearish']
            }
            
            for trend, keywords in trend_triggers.items():
                if any(keyword in sentence for keyword in keywords):
                    insights['trends'].append(trend)
        
        # Process results
        insights['average_sentiment'] = sum(insights['sentiments'])/len(insights['sentiments']) if insights['sentiments'] else 0
        insights['entities'] = {k: list(set(v)) for k, v in insights['entities'].items()}
        insights['trends'] = list(set(insights['trends']))
        
        return insights

# Initialize QA system
qa_system = EnhancedCryptoQA()

# Flask routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question', '')
    answers = qa_system.get_answers(question)
    insights = qa_system.generate_insights(answers)
    
    if insights['average_sentiment'] < 0.05:  # Low confidence threshold  
        return jsonify({
            "answers": answers,
            "insights": insights,
            "message": "The answer might be inappropriate because of low training data. Please ask another question."
        })
    else:
        return jsonify({
            "answers": answers,
            "insights": insights
        })
    

if __name__ == '__main__':
    app.run(debug=True)
