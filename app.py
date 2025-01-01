import os
from flask import Flask, request, render_template, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)

# Path to Tesseract executable (adjust for your system)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust this path

# Predefined answer key
answer_key = {
    "Q1": "Python is a programming language.",
    "Q2": "Flask is a micro web framework."
}

def validate_answer(question, extracted_text):
    correct_answer = answer_key.get(question, "")
    if correct_answer.lower() in extracted_text.lower():
        return "Correct"
    return "Incorrect"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/validate", methods=["POST"])
def validate():
    results = {}
    for question in answer_key.keys():
        if question in request.files:
            # Save the uploaded image
            image = request.files[question]
            image_path = os.path.join("uploads", image.filename)
            image.save(image_path)

            # Extract text from the image
            extracted_text = pytesseract.image_to_string(Image.open(image_path))

            # Validate the extracted text
            results[question] = validate_answer(question, extracted_text)
            os.remove(image_path)  # Clean up the saved image
        else:
            results[question] = "No image provided"
    return jsonify(results)

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)  # Create uploads directory if it doesn't exist
    app.run(debug=True)

