from flask import Flask, request, jsonify,render_template
import google.generativeai as palm
import warnings
from flask_cors import CORS
from pymongo import MongoClient
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time


client = MongoClient('mongodb://localhost:27017/')
db = client['dark_patterns']

app = Flask(__name__)
CORS(app)


# Configure the generativeAI API key
palm.configure(api_key='AIzaSyAGeAIOgmRyusKhWf9qfU0um2ZiN1Na8sY')

# Get a supported model for text generation
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name


@app.route('/')
def home():
    return render_template('form.html')


@app.route('/detect_dp', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()
        input_text = data.get('input_text', '')

        # Construct the prompt
        prompt = f"""
                    {input_text}. This statement was found on an e-commerce site, is this statement a dark pattern. ANSWER: Yes or No
                    """
        # Generate text using the generativeAI API
        print(prompt)
        prediction = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            max_output_tokens=800,
        )


        result = prediction.result

        if(result=='Yes'):
            return jsonify({'message': True})
        else:
            return jsonify({'message': False})

        

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit():
    dark_patterns = request.form.get('dark_patterns')
    feedback = request.form.get('feedback')
    ratings = int(request.form.get('ratings'))

    # Store data in MongoDB
    db.submissions.insert_one({
        'dark_patterns': dark_patterns,
        'feedback': feedback,
        'ratings': ratings
    })

    return render_template('form.html',response_text = "Form submitted successfully! Thank you for the response")
if __name__ == '__main__':
    app.run(debug=True)
