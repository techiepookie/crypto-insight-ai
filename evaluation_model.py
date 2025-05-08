import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import seaborn as sns
import matplotlib.pyplot as plt

import json
import csv
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer('all-MiniLM-L6-v2')


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as a:
        return json.load(a)

def is_valid_entry(entry):
    coin = entry.get('coin', '').lower()
    query = entry.get('query', '')
    answers = entry.get('answers', [])

    
    if coin == 'general crypto':  # If coin is general crypto always valid
        return True

   
    if not query or not answers:   # If query or answers empty, invalid
        return False

    input_query = query.lower()
    input_coin = coin.lower()



    # Check if coin is in query
    coin_in_query = input_coin in input_query


    # Check if coin is in any answer text
    coin_in_answers = any(input_coin in answer.get('text', '').lower() for answer in answers)

    # Semantic similarity check between coin and answers
    coin_embedding = model.encode(coin, convert_to_tensor=True)
    answer_texts = [answer.get('text', '') for answer in answers]
    answer_embeddings = model.encode(answer_texts, convert_to_tensor=True)
    cosine_scores = util.cos_sim(coin_embedding, answer_embeddings)[0]



    threshold = 0.6
    similarity_valid = any(score >= threshold for score in cosine_scores)

    # Validation logic combining keyword and semantic similarity
    if coin_in_answers or similarity_valid:
        if coin_in_query:
            return True
        else:
            return True
    else:
        return False

def save_results(results, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['coin', 'query','status', 'answers'])
        for coin, query, status, answers in results:
            
            # Extract first  'text' from each answer dict
            answer_texts = [answer.get('text', '') for answer in answers]
            text = answer_texts[0] if len(answer_texts) > 0 else ''
            
            # Format as single string with labels
            answers_str = f"text: {text}" 
            writer.writerow([coin, query, status,answers_str])

def main():
    data = load_data('query_logs.json')
    results = []
    for entry in data:
        valid = is_valid_entry(entry)
        status = 'valid' if valid else 'invalid'
        # Save coin, query, status, and answers as is from JSON in correct order
        results.append((entry.get('coin', ''), entry.get('query', ''), status, entry.get('answers', [])))
    save_results(results, 'validation_results.csv')

if __name__ == '__main__':
    main()


# === 1. Load Data ===
vectorised_file = 'vectorised.csv'
df = pd.read_csv(vectorised_file)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

X = df.drop(columns=['status'])
y = df['status']

# === 2. Train/Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === 3. Define Classifiers ===
models = {
    'SVM': SVC(C=10, kernel='rbf', class_weight='balanced'),
    'Logistic Regression': LogisticRegression(class_weight='balanced', max_iter=1000),
    'Random Forest': RandomForestClassifier(class_weight='balanced', random_state=42)
}

# === 4. Evaluate Each Model ===
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n=== {name} ===")
    print(classification_report(y_test, y_pred))
    print("Accuracy:", acc)

# === 5. Confusion Matrix for Best Model (e.g., Random Forest) ===
best_model = models['Random Forest']
y_pred_best = best_model.predict(X_test)
cm = confusion_matrix(y_test, y_pred_best)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix - Random Forest')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.savefig('confusion_matrix.png')
plt.show()

# === 6. Predict on Full Data (Optional) ===
y_pred_full = best_model.predict(X)
pred_df = pd.DataFrame({'prediction': y_pred_full})
pred_df.to_csv('predictions.csv', index=False)
print("\nPredictions saved to predictions.csv")
