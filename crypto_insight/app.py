from flask import Flask, request, jsonify, render_template
from model import process_query, valid_query, COINS 
from flask_cors import CORS
from logger import log_query

app = Flask(__name__)
CORS(app)

# Health-check and homepage endpoint (GET)
@app.route("/", methods=['GET', 'POST'])
def index():
    # Try to render an index.html template if available; otherwise return a simple message.
    try:
        return render_template("index.html")
    except Exception as e:
        return jsonify({"message": "Crypto Insights is Down right now please try again later!"}), 200

# Query endpoint (POST)
@app.route("/query", methods=["POST"])
def handle_query():
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided."}), 400
    
    coin = data.get("coin", "").lower().strip()
    query = data.get("query", "").strip()
    
    if not coin or not query:
        return jsonify({"error": "Please provide both coin and query."}), 400

    # Validate coin against the list defined in model.py
    if coin not in COINS:
        return jsonify({"error": f"Unsupported coin. Choose from: {', '.join(COINS)}."}), 400

    # Validate that the query contains some crypto-related keywords
    if not valid_query(query):
        return jsonify({"error": "Query seems unrelated to crypto. Try asking something like 'What's the trend of Bitcoin this week?'"}), 400

    # Process the query using model.py
    result = process_query(coin, query)

    # Extract for logging__________________________________________________
    top_results = result.get("raw_top_results", [])
    sentiment = result.get("sentiment", "unknown")

    # Log the query
    log_query(coin, query, sentiment, top_results)
    # Removing raw_top_results so it doesn't show on the frontend
    result.pop("raw_top_results", None)
    # Logging ends________________________________________________________
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)