// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const extractBtn = document.getElementById('extractBtn');
const selectedFileDiv = document.getElementById('selectedFile');
const statusMessage = document.getElementById('statusMessage');
const resultsSection = document.getElementById('resultsSection');
const productsTableBody = document.getElementById('productsTableBody');
const productCount = document.getElementById('productCount');
const downloadBtn = document.getElementById('downloadBtn');
const productModal = document.getElementById('productModal');
const closeModal = document.querySelector('.close-modal');
const productDetails = document.getElementById('productDetails');
const btnLoader = document.getElementById('btnLoader');

// State
let selectedFile = null;
let productsData = [];

// Event Listeners
browseBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFileSelect);
uploadArea.addEventListener('click', () => fileInput.click());
extractBtn.addEventListener('click', handleExtract);
downloadBtn.addEventListener('click', downloadJSON);
closeModal.addEventListener('click', () => productModal.style.display = 'none');

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect();
    }
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === productModal) {
        productModal.style.display = 'none';
    }
});

// Handle file selection
function handleFileSelect() {
    const file = fileInput.files[0];
    
    if (file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            showStatus('Please select an image file', 'error');
            return;
        }
        
        selectedFile = file;
        selectedFileDiv.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
        selectedFileDiv.style.display = 'block';
        extractBtn.disabled = false;
        hideStatus();
    }
}

// Handle product extraction
async function handleExtract() {
    if (!selectedFile) return;
    
    // Disable button and show loading
    extractBtn.disabled = true;
    extractBtn.classList.add('loading');
    hideStatus();
    
    // Create FormData
    const formData = new FormData();
    formData.append('image', selectedFile);
    
    try {
        const response = await fetch('http://localhost:5000/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            productsData = data.products;
            displayProducts(data.products);
            showStatus(`Successfully extracted ${data.total_products} products!`, 'success');
            resultsSection.style.display = 'block';
            
            // Smooth scroll to results
            setTimeout(() => {
                resultsSection.scrollIntoView({ behavior: 'smooth' });
            }, 300);
        } else {
            showStatus(data.error || 'Failed to extract products', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showStatus('Network error: Please ensure the server is running', 'error');
    } finally {
        extractBtn.disabled = false;
        extractBtn.classList.remove('loading');
    }
}

// Display products in table
function displayProducts(products) {
    productsTableBody.innerHTML = '';
    productCount.textContent = products.length;
    
    products.forEach((product, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${escapeHtml(product.product_name)}</td>
            <td class="price-cell">${escapeHtml(product.price)}</td>
            <td>${escapeHtml(product.unit)}</td>
            <td>${escapeHtml(product.category)}</td>
            <td>
                ${product.special_offer ? 
                    `<span class="special-offer-badge">${escapeHtml(product.special_offer)}</span>` 
                    : '-'}
            </td>
            <td>
                <button class="view-btn" onclick="viewProduct(${index})">View</button>
            </td>
        `;
        
        // Make row clickable
        row.style.cursor = 'pointer';
        row.addEventListener('click', (e) => {
            // Don't trigger if clicking the button
            if (!e.target.classList.contains('view-btn')) {
                viewProduct(index);
            }
        });
        
        productsTableBody.appendChild(row);
    });
}

// View product details
function viewProduct(index) {
    const product = productsData[index];
    
    productDetails.innerHTML = `
        <div class="detail-row">
            <div class="detail-label">Product ID:</div>
            <div class="detail-value">${index + 1}</div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Product Name:</div>
            <div class="detail-value">${escapeHtml(product.product_name)}</div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Price:</div>
            <div class="detail-value" style="font-weight: 700; color: var(--secondary-color); font-size: 1.2rem;">
                ${escapeHtml(product.price)}
            </div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Unit/Quantity:</div>
            <div class="detail-value">${escapeHtml(product.unit)}</div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Category:</div>
            <div class="detail-value">${escapeHtml(product.category)}</div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Special Offer:</div>
            <div class="detail-value">
                ${product.special_offer ? 
                    `<span class="special-offer-badge">${escapeHtml(product.special_offer)}</span>` 
                    : 'None'}
            </div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Additional Info:</div>
            <div class="detail-value">${escapeHtml(product.additional_info) || 'None'}</div>
        </div>
    `;
    
    productModal.style.display = 'block';
}

// Download JSON
function downloadJSON() {
    const dataStr = JSON.stringify(productsData, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'products_data.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showStatus('JSON file downloaded successfully!', 'success');
}

// Show status message
function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.style.display = 'block';
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(hideStatus, 5000);
    }
}

// Hide status message
function hideStatus() {
    statusMessage.style.display = 'none';
}

// Utility function to format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Load existing products on page load
window.addEventListener('load', async () => {
    try {
        const response = await fetch('http://localhost:5000/api/products');
        const data = await response.json();
        
        if (data.products && data.products.length > 0) {
            productsData = data.products;
            displayProducts(data.products);
            resultsSection.style.display = 'block';
        }
    } catch (error) {
        console.log('No existing products to load');
    }
});