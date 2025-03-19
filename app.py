from flask import Flask, request, jsonify
import cv2
import numpy as np
import io
from PIL import Image
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import threading

# Load environment variables
load_dotenv()

# Set the DeepFace home directory
os.environ["DEEPFACE_HOME"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

from deepface import DeepFace

# Add a model initialization lock
model_init_lock = threading.Lock()

# Load threshold from environment
THRESHOLD = float(os.environ.get("THRESHOLD", 16.0))

def init_deepface():
    """
    Initialize DeepFace model to avoid delays on the first request.
    """
    print("Initializing DeepFace model...")
    dummy_img = np.zeros((112, 112, 3), dtype=np.uint8)
    try:
        with model_init_lock:
            DeepFace.represent(dummy_img, model_name="Facenet512", enforce_detection=False)
            print("Facenet512 model loaded successfully!")
    except Exception as e:
        print(f"Error initializing model: {e}")

# Initialize model before starting Flask
init_deepface()

app = Flask(__name__)
CORS(app)

def preprocess_image(image, target_size=(112, 112)):
    image = cv2.resize(image, target_size)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def detect_face(image):
    """
    Detects the largest face in an image using Haar cascades.
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]
    return image[y:y+h, x:x+w]

@app.route('/compare_faces', methods=['POST'])
def compare_faces():
    try:
        if 'image_url' not in request.form or 'image2' not in request.files:
            return jsonify({'error': 'Missing image URL or image file'}), 400

        image_url = request.form['image_url']
        image2_file = request.files['image2']

        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            image1_pil = Image.open(io.BytesIO(response.content))
            image1_cv2 = cv2.cvtColor(np.array(image1_pil), cv2.COLOR_RGB2BGR)

        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'Error fetching image from URL: {e}'}), 400

        allowed_extensions = {'.jpg', '.jpeg', '.png'}
        _, image2_ext = os.path.splitext(image2_file.filename.lower())

        if image2_ext not in allowed_extensions:
            return jsonify({'error': 'Invalid image file format. Allowed formats are jpg, jpeg, and png'}), 400

        image2_bytes = image2_file.read()
        image2_pil = Image.open(io.BytesIO(image2_bytes))
        image2_cv2 = cv2.cvtColor(np.array(image2_pil), cv2.COLOR_RGB2BGR)

        photo1 = detect_face(image1_cv2)
        if photo1 is None:
            return jsonify({'error': 'No face found in the image from URL'}), 400

        photo2 = detect_face(image2_cv2)
        if photo2 is None:
            return jsonify({'error': 'No face found in the uploaded image'}), 400

        photo1 = preprocess_image(photo1)
        photo2 = preprocess_image(photo2)

        try:
            with model_init_lock:
                photo1_embedding = DeepFace.represent(photo1, model_name="Facenet512", enforce_detection=False)
                photo2_embedding = DeepFace.represent(photo2, model_name="Facenet512", enforce_detection=False)

            photo1_embedding = np.array(photo1_embedding[0]["embedding"])
            photo2_embedding = np.array(photo2_embedding[0]["embedding"])

            euclidean_distance = np.linalg.norm(photo1_embedding - photo2_embedding)

            # Use the threshold from environment variable
            is_match = euclidean_distance < THRESHOLD

            return jsonify({
                'euclidean_distance': float(euclidean_distance),
                'is_match': bool(is_match),
                'threshold': THRESHOLD
            })

        except ValueError as e:
            return jsonify({'error': f"DeepFace error: {e}"}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)