# ALDI Leaflet Product Extractor

## 🎯 Project Overview

This application uses Azure OpenAI's GPT-4 Vision API to automatically extract product information from retail leaflet images. It provides a complete web-based solution with a modern UI for uploading images, viewing extracted products in a table format, and exporting data to JSON.

## 🏗️ Architecture & Design Decisions

### 1. **Technology Stack**

#### Backend: Flask (Python)
**Why Flask?**
- Lightweight and perfect for this API-focused application
- Easy to set up and deploy
- Excellent for rapid prototyping
- Built-in development server for local testing
- Good integration with Python libraries (PIL, requests)

#### Frontend: Vanilla JavaScript + HTML/CSS
**Why Vanilla JS?**
- No build tools or complex setup required
- Faster development for this scope
- Easy to understand and modify
- Modern CSS Grid and Flexbox for responsive design
- No dependency management overhead

#### AI: Azure OpenAI GPT-4 Vision
**Why Azure OpenAI?**
- State-of-the-art vision-language model
- Excellent OCR and understanding capabilities
- Can extract structured data from images
- Reliable API with good documentation
- Enterprise-grade security and compliance

### 2. **Design Patterns Used**

#### Separation of Concerns
- **app.py**: API routes and server logic
- **extractor.py**: AI vision processing logic
- **config.py**: Configuration management
- **Frontend files**: UI and user interaction

#### Configuration Management
- Environment variables via `.env` file
- Centralized config class
- Easy to switch between development/production

#### Error Handling
- Try-catch blocks throughout
- Fallback data for testing without API
- User-friendly error messages
- Proper HTTP status codes

### 3. **Data Flow**

```
User uploads image → Flask receives file → Save to uploads/
                                         ↓
                                  Encode to base64
                                         ↓
                          Send to Azure OpenAI Vision API
                                         ↓
                              Parse JSON response
                                         ↓
                          Save to output/data.json
                                         ↓
                      Return to frontend → Display in table
```

### 4. **Key Features Implemented**

#### Image Upload
- Drag & drop interface
- File browser button
- File type validation
- File size display

#### AI Processing
- Base64 image encoding
- Structured prompt engineering for optimal extraction
- JSON parsing with error handling
- Fallback data for testing

#### Product Display
- Responsive data table
- Clickable rows for details
- Modal popup for full product info
- Category badges and special offer highlighting

#### Data Export
- JSON file generation
- Download functionality
- Persistent storage in output/ directory

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Python 3.8+** installed
2. **pip** (Python package manager)
3. **Azure OpenAI Service** account with:
   - API Key
   - Endpoint URL
   - GPT-4 Vision deployment

## 🚀 Setup Instructions

### Step 1: Clone or Create Project Structure

Create the following directory structure:

```
aldi-leaflet-extractor/
├── backend/
│   ├── app.py
│   ├── extractor.py
│   ├── config.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── uploads/          (will be created automatically)
├── output/           (will be created automatically)
├── .env
└── README.md
```

### Step 2: Get Azure OpenAI Credentials

1. Go to [Azure Portal](https://portal.azure.com)
2. Create an Azure OpenAI resource (if you don't have one)
3. Deploy a GPT-4 Vision model:
   - Go to Azure OpenAI Studio
   - Click "Deployments"
   - Create new deployment
   - Select "gpt-4" with vision capability
   - Note the deployment name
4. Get your credentials:
   - Go to your Azure OpenAI resource
   - Click "Keys and Endpoint"
   - Copy `KEY 1` and `Endpoint`

### Step 3: Configure Environment Variables

1. Create a `.env` file in the project root:

```bash
AZURE_OPENAI_API_KEY=your_actual_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_DEPLOYMENT_NAME=your-deployment-name
```

**Example:**
```bash
AZURE_OPENAI_API_KEY=abcd1234efgh5678ijkl9012mnop3456
AZURE_OPENAI_ENDPOINT=https://mycompany-openai.openai.azure.com/
AZURE_DEPLOYMENT_NAME=gpt-4-vision-preview
```

### Step 4: Install Python Dependencies

Open your terminal in VSCode and run:

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- flask-cors (CORS support)
- python-dotenv (environment variables)
- requests (HTTP library)
- Pillow (image processing)

### Step 5: Run the Application

1. **Start the Flask server:**

```bash
cd backend
python app.py
```

You should see:
```
============================================================
ALDI Leaflet Product Extractor Server
============================================================
Server running at: http://localhost:5000
Azure OpenAI configured: True
============================================================
```

2. **Open your browser:**
   - Navigate to: `http://localhost:5000`
   - You should see the application interface

## 📖 How to Use

### 1. Upload a Leaflet Image

**Method A: Drag & Drop**
- Drag your leaflet image file onto the upload area

**Method B: Browse**
- Click "Choose File" button
- Select your leaflet image

### 2. Extract Products

- Click the "Extract Products" button
- Wait for processing (usually 5-15 seconds)
- Products will appear in the table below

### 3. View Product Details

**Method A: Click on any row in the table**
- A modal popup will show full product details

**Method B: Click "View" button**
- Same modal popup with details

### 4. Export Data

- Click "Download JSON" button
- Save the `products_data.json` file
- Use this data in other applications

## 📁 Output Format

The application generates a JSON file with this structure:

```json
[
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
  }
]
```

## 🔧 API Endpoints

### POST /api/upload
Upload and process a leaflet image

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
  "success": true,
  "products": [...],
  "total_products": 13
}
```

### GET /api/products
Retrieve all stored products

**Response:**
```json
{
  "products": [...]
}
```

### GET /api/product/<id>
Get specific product details

**Response:**
```json
{
  "success": true,
  "product": {...}
}
```

## 🎨 UI Features

### Modern Design
- Gradient backgrounds
- Card-based layout
- Smooth animations
- Responsive design (mobile-friendly)

### Interactive Elements
- Hover effects on table rows
- Loading spinners
- Status messages
- Modal dialogs

### User Experience
- Drag & drop upload
- Clear feedback messages
- Automatic scrolling to results
- Downloadable data

## 🔍 Troubleshooting

### Issue: "Azure OpenAI configured: False"

**Solution:**
1. Check your `.env` file exists in project root
2. Verify credentials are correct
3. No quotes around values in `.env`
4. Restart the Flask server

### Issue: "Network error: Please ensure the server is running"

**Solution:**
1. Check Flask server is running (`python app.py`)
2. Check console for error messages
3. Verify port 5000 is not blocked
4. Try restarting the server

### Issue: Products not extracting correctly

**Solution:**
1. Ensure image is clear and readable
2. Check Azure OpenAI quota/limits
3. Verify deployment name is correct
4. Look at console logs for API errors

### Issue: CORS errors in browser console

**Solution:**
- Already handled by flask-cors
- If still occurring, check server is on localhost:5000
- Try clearing browser cache

## 📊 Testing Without Azure API

The application includes fallback data for testing. If Azure API is not configured, it will return sample products automatically. This allows you to:
- Test the UI
- See the data structure
- Develop without API costs

## 🔐 Security Considerations

1. **API Keys**: Never commit `.env` file to version control
2. **Input Validation**: File type checking on frontend and backend
3. **Error Handling**: Sensitive data not exposed in error messages
4. **CORS**: Properly configured for local development

## 🚀 Future Enhancements

Potential improvements:
1. **Database Integration**: Store products in SQLite/PostgreSQL
2. **User Authentication**: Multi-user support
3. **Batch Processing**: Upload multiple images
4. **PDF Support**: Extract from PDF leaflets
5. **Advanced Filtering**: Search and filter products
6. **Price Tracking**: Track price changes over time
7. **Export Options**: CSV, Excel formats
8. **Cloud Deployment**: Deploy to Azure/AWS

## 📝 Development Notes

### Prompt Engineering
The key to accurate extraction is the carefully crafted prompt in `extractor.py`. It:
- Specifies exact JSON format
- Lists all required fields
- Provides examples
- Uses clear instructions
- Requests systematic scanning

### Error Handling Strategy
- Multiple fallback layers
- User-friendly messages
- Console logging for debugging
- Graceful degradation

### Performance Optimization
- Base64 encoding done once
- Minimal API calls
- Client-side validation
- Efficient JSON parsing

## 📞 Support

If you encounter issues:
1. Check troubleshooting section
2. Review console logs (browser + server)
3. Verify Azure OpenAI configuration
4. Check Azure service status

## 📄 License

This project is for educational/demonstration purposes.

## 🙏 Acknowledgments

- Azure OpenAI for vision capabilities
- Flask framework
- Modern CSS techniques
- MDN Web Docs for frontend reference

---

**Built with ❤️ for automated product extraction**