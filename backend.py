from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

# Load dataset
data = pd.read_csv('AnimalInformation.csv')

# Rename columns
data.columns = ['Index', 'Animal', 'Size', 'Color', 'Pettable']

# Calculate prior probabilities
Pyes = len(data[data['Pettable'] == 'Yes']) / len(data)
Pno = len(data[data['Pettable'] == 'No']) / len(data)

# Calculate conditional probabilities for Size
PmediumYes = len(data[(data['Size'] == 'Medium') & (data['Pettable'] == 'Yes')]) / len(data[data['Pettable'] == 'Yes'])
PmediumNo = len(data[(data['Size'] == 'Medium') & (data['Pettable'] == 'No')]) / len(data[data['Pettable'] == 'No'])
PsmallYes = len(data[(data['Size'] == 'Small') & (data['Pettable'] == 'Yes')]) / len(data[data['Pettable'] == 'Yes'])
PsmallNo = len(data[(data['Size'] == 'Small') & (data['Pettable'] == 'No')]) / len(data[data['Pettable'] == 'No'])
PbigYes = len(data[(data['Size'] == 'Big') & (data['Pettable'] == 'Yes')]) / len(data[data['Pettable'] == 'Yes'])
PbigNo = len(data[(data['Size'] == 'Big') & (data['Pettable'] == 'No')]) / len(data[data['Pettable'] == 'No'])

# Calculate conditional probabilities for Color
PbrownYes = len(data[(data['Color'] == 'Brown') & (data['Pettable'] == 'Yes')]) / len(data[data['Pettable'] == 'Yes'])
PbrownNo = len(data[(data['Color'] == 'Brown') & (data['Pettable'] == 'No')]) / len(data[data['Pettable'] == 'No'])
PblackYes = len(data[(data['Color'] == 'Black') & (data['Pettable'] == 'Yes')]) / len(data[data['Pettable'] == 'Yes'])
PblackNo = len(data[(data['Color'] == 'Black') & (data['Pettable'] == 'No')]) / len(data[data['Pettable'] == 'No'])
PwhiteYes = len(data[(data['Color'] == 'White') & (data['Pettable'] == 'Yes')]) / len(data[data['Pettable'] == 'Yes'])
PwhiteNo = len(data[(data['Color'] == 'White') & (data['Pettable'] == 'No')]) / len(data[data['Pettable'] == 'No'])

# API endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from frontend
        input_data = request.get_json()
        size = input_data.get('size').capitalize()  # Capitalize to match dataset (e.g., 'Medium')
        color = input_data.get('color').capitalize()  # Capitalize to match dataset (e.g., 'Brown')
        # Note: Animal name is not used in the current prediction logic but can be used for filtering if needed

        # Map size to probabilities
        size_probs = {
            'Medium': (PmediumYes, PmediumNo),
            'Small': (PsmallYes, PsmallNo),
            'Large': (PbigYes, PbigNo)  # Assuming 'large' in frontend maps to 'Big' in dataset
        }
        color_probs = {
            'Brown': (PbrownYes, PbrownNo),
            'Black': (PblackYes, PblackNo),
            'White': (PwhiteYes, PwhiteNo)
        }

        # Get conditional probabilities
        PsizeYes, PsizeNo = size_probs.get(size, (0, 0))
        PcolorYes, PcolorNo = color_probs.get(color, (0, 0))

        # Calculate probabilities
        Prob_yes = PsizeYes * PcolorYes * Pyes
        Prob_no = PsizeNo * PcolorNo * Pno

        # Make prediction
        prediction = "Can be petted" if Prob_yes > Prob_no else "Cannot be petted"

        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)