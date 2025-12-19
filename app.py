from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from extractor import LeafletExtractor
from config import Config

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Initialize configuration
config = Config()

# Create necessary directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('output', exist_ok=True)

# Initialize extractor
extractor = LeafletExtractor(config)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('../frontend', path)

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """Handle image upload and processing"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        
        # Extract products from image
        products = extractor.extract_products(filepath)
        
        # Save to JSON file
        output_path = os.path.join('output', 'data.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'products': products,
            'total_products': len(products)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """Retrieve stored products"""
    try:
        output_path = os.path.join('output', 'data.json')
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                products = json.load(f)
            return jsonify({'products': products})
        else:
            return jsonify({'products': []})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product_detail(product_id):
    """Get details of a specific product"""
    try:
        output_path = os.path.join('output', 'data.json')
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                products = json.load(f)
            
            if 0 <= product_id < len(products):
                return jsonify({
                    'success': True,
                    'product': products[product_id]
                })
            else:
                return jsonify({'error': 'Product not found'}), 404
        else:
            return jsonify({'error': 'No products available'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

'''if __name__ == '__main__':
    print("=" * 60)
    print("ALDI Leaflet Product Extractor Server")
    print("=" * 60)
    print(f"Server running at: http://localhost:5000")
    print(f"Azure OpenAI configured: {config.is_configured()}")
    print("=" * 60)
    app.run(debug=True, port=5000)'''

if __name__ == '__main__':
    
    PORT = int(os.environ.get("PORT", 5000))  # Use Railway/Azure port if set
    print("=" * 60)
    print("ALDI Leaflet Product Extractor Server")
    print("=" * 60)
    print(f"Server running at: http://localhost:{PORT}")
    print(f"Azure OpenAI configured: {config.is_configured()}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=PORT, debug=True)
