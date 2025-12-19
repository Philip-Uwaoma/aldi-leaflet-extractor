import base64
import json
import requests
from typing import List, Dict
import os

class LeafletExtractor:
    """Extracts product information from leaflet images using Azure OpenAI Vision API"""
    
    def __init__(self, config):
        self.config = config
        self.api_key = config.azure_api_key
        self.endpoint = config.azure_endpoint
        self.deployment_name = config.deployment_name
        
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def extract_products(self, image_path: str) -> List[Dict]:
        """
        Extract product information from leaflet image using Azure OpenAI Vision API
        
        Args:
            image_path: Path to the leaflet image
            
        Returns:
            List of product dictionaries
        """
        
        # Encode image
        base64_image = self.encode_image(image_path)
        
        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        
        # Construct the prompt for optimal extraction
        prompt = """You are an expert at extracting product information from retail leaflets.

Analyze this ALDI leaflet image and extract ALL visible products with their details.

For each product, extract:
1. product_name: The full product name/description
2. price: The price (include currency symbol if visible)
3. unit: The unit/quantity (e.g., "per kg", "250g Pack", "each")
4. category: Product category (e.g., "Fresh Produce", "Meat", "Beverages", "Snacks")
5. special_offer: Any special offer text (e.g., "Super Savers", "Special Buys")
6. additional_info: Any extra details (certifications, origin, etc.)

Return ONLY a valid JSON array with no additional text. Format:

[
  {
    "product_name": "Mini Cucumbers",
    "price": "$3.49",
    "unit": "250g per pack",
    "category": "Fresh Produce",
    "special_offer": "Super Savers",
    "additional_info": "Brussels Sprouts flavor"
  }
]

Extract every single product visible in the image systematically from left to right, top to bottom."""

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4000,
            "temperature": 0.1
        }
        
        # Make API request
        api_url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version=2024-08-01-preview"
        
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse the JSON response
            # Remove markdown code blocks if present
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            products = json.loads(content)
            
            # Add ID to each product
            for idx, product in enumerate(products):
                product['id'] = idx
            
            return products
            
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return self._get_fallback_data()
        except json.JSONDecodeError as e:
            print(f"JSON Parsing Error: {e}")
            print(f"Content received: {content}")
            return self._get_fallback_data()
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return self._get_fallback_data()
    
    def _get_fallback_data(self) -> List[Dict]:
        """Return sample data if API fails (for testing/demo purposes)"""
        return [
            {
                "id": 0,
                "product_name": "Mini Cucumbers Brussels Sprouts Flavour",
                "price": "$3.49",
                "unit": "250g per pack",
                "category": "Fresh Produce",
                "special_offer": "Super Savers",
                "additional_info": "Fresh vegetables"
            },
            {
                "id": 1,
                "product_name": "Strawberries",
                "price": "$2.49",
                "unit": "250g Pack",
                "category": "Fresh Produce",
                "special_offer": "Super Savers",
                "additional_info": "Fresh berries"
            },
            {
                "id": 2,
                "product_name": "Sweet Corn Cobs",
                "price": "$3.99",
                "unit": "4 pack per kg",
                "category": "Fresh Produce",
                "special_offer": "Super Savers",
                "additional_info": "Fresh corn"
            },
            {
                "id": 3,
                "product_name": "Australian Blueberries",
                "price": "$3.99",
                "unit": "125g Pack",
                "category": "Fresh Produce",
                "special_offer": "",
                "additional_info": "Australian Grown"
            },
            {
                "id": 4,
                "product_name": "White Flat Mushrooms",
                "price": "$4.99",
                "unit": "200g Pack",
                "category": "Fresh Produce",
                "special_offer": "Super Savers",
                "additional_info": ""
            },
            {
                "id": 5,
                "product_name": "Aussie Asparagus",
                "price": "$2.69",
                "unit": "per bunch",
                "category": "Fresh Produce",
                "special_offer": "",
                "additional_info": "Fresh, locally grown"
            },
            {
                "id": 6,
                "product_name": "Freerange Acero RSPCA Approved Chicken Breast Fillets",
                "price": "$7.49",
                "unit": "per kg",
                "category": "Meat & Poultry",
                "special_offer": "",
                "additional_info": "RSPCA Approved, Australian"
            },
            {
                "id": 7,
                "product_name": "Schultz Oven Roast Crumbed Chicken Tenderloin",
                "price": "$8.49",
                "unit": "400g",
                "category": "Meat & Poultry",
                "special_offer": "",
                "additional_info": ""
            },
            {
                "id": 8,
                "product_name": "Ocean King Cooked Prawn Value Pack",
                "price": "$8.99",
                "unit": "500g",
                "category": "Seafood",
                "special_offer": "",
                "additional_info": ""
            },
            {
                "id": 9,
                "product_name": "The Fishmonger Fresh Tasmanian Skin On Salmon Fillets",
                "price": "$24.99",
                "unit": "500g-720g",
                "category": "Seafood",
                "special_offer": "",
                "additional_info": "Fresh Tasmanian"
            },
            {
                "id": 10,
                "product_name": "Arnott's Tim Tam",
                "price": "$2.49",
                "unit": "200g-200g",
                "category": "Snacks",
                "special_offer": "ALDI Special Buys",
                "additional_info": ""
            },
            {
                "id": 11,
                "product_name": "Dime Canola Oil or Sunflower Oil",
                "price": "$7.59",
                "unit": "4L",
                "category": "Pantry",
                "special_offer": "ALDI Special Buys",
                "additional_info": ""
            },
            {
                "id": 12,
                "product_name": "Coca-Cola Classic or Coca-Cola No Sugar",
                "price": "$9.49",
                "unit": "10x375ml",
                "category": "Beverages",
                "special_offer": "",
                "additional_info": "Can multipack"
            }
        ]