import json
from qa_system import EnhancedCryptoQA  # Import the QA system class

# Load test data
with open('test.json', 'r') as f:
    test_data = json.load(f)

# Initialize QA system
qa_system = EnhancedCryptoQA()  # Create an instance of the QA system

def evaluate_model(qa_system, test_data, k=3):
    precision_scores = []
    recall_scores = []

    for item in test_data:
        question = item['question']
        relevant_sentences = set(item['relevant_sentences'])
        
        # Get model predictions
        predicted_sentences = qa_system.get_answers(question)
        
        # Calculate precision and recall
        predicted_set = set(predicted_sentences[:k])
        relevant_set = set(relevant_sentences)
        
        # True positives: Sentences that are both predicted and relevant
        true_positives = predicted_set.intersection(relevant_set)
        
        # Precision@K: Fraction of predicted sentences that are relevant
        precision = len(true_positives) / k
        precision_scores.append(precision)
        
        # Recall@K: Fraction of relevant sentences that are predicted
        recall = len(true_positives) / len(relevant_set)
        recall_scores.append(recall)
    
    # Calculate averages
    avg_precision = sum(precision_scores) / len(precision_scores)
    avg_recall = sum(recall_scores) / len(recall_scores)
    
    # F1 Score: Harmonic mean of precision and recall
    f1_score = 2 * (avg_precision * avg_recall) / (avg_precision + avg_recall) if (avg_precision + avg_recall) > 0 else 0
    
    return {
        'precision@k': avg_precision,
        'recall@k': avg_recall,
        'f1_score': f1_score
    }

# Evaluate the model
results = evaluate_model(qa_system, test_data, k=3)
print("Evaluation Results:")
print(f"Precision@3: {results['precision@k']:.2f}")
print(f"Recall@3: {results['recall@k']:.2f}")
print(f"F1 Score: {results['f1_score']:.2f}")