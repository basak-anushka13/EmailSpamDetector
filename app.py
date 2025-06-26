import string
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load your trained model and vectorizer
model = pickle.load(open('spam_model.pkl', 'rb'))
vectorizer = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))

# Route for the landing page
@app.route('/')
def index():
    return render_template('index.html')  # This is your landing page with logo, features, etc.

# Route for the spam checker form + prediction
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        message = request.form['message']

        # Clean the input message (same preprocessing as training)
        cleaned = message.lower()
        cleaned = ''.join([c for c in cleaned if c not in string.punctuation])

        # Vectorize and predict
        vec = vectorizer.transform([cleaned])
        prediction = model.predict(vec)[0]

        # Return result to the same form
        result = "🚨 SPAM!" if prediction == 1 else "✅ Not Spam"
        return render_template('home.html', prediction=result, original=message)

    return render_template('home.html')  # GET request, show the form

if __name__ == '__main__':
    app.run(debug=True)
