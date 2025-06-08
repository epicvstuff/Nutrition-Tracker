class UploadComponent {
  constructor(onClassificationComplete) {
    this.onClassificationComplete = onClassificationComplete;
    this.uploadForm = document.getElementById('upload-form');
    this.uploadStatus = document.getElementById('upload-status');
    this.fileInput = this.uploadForm.querySelector('input[type="file"]');
    
    this.bindEvents();
  }

  bindEvents() {
    this.uploadForm.addEventListener('submit', this.handleUpload.bind(this));
    this.fileInput.addEventListener('change', this.handleFileSelect.bind(this));
  }

  handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
      console.log('File selected:', file.name, file.type, file.size);
      this.validateFile(file);
    }
  }

  validateFile(file) {
    // Check file type
    if (!file.type.startsWith('image/')) {
      console.error('Invalid file type:', file.type);
      this.showError('Please select an image file.');
      this.fileInput.value = '';
      return false;
    }

    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      console.error('File too large:', file.size);
      this.showError('File size must be less than 5MB.');
      this.fileInput.value = '';
      return false;
    }

    return true;
  }

  async handleUpload(event) {
    event.preventDefault();
    
    const file = this.fileInput.files[0];
    if (!file) {
      this.showError('Please select an image to upload.');
      return;
    }

    if (!this.validateFile(file)) {
      return;
    }

    try {
      this.showStatus('Uploading and classifying image...');
      console.log('Starting upload for file:', file.name);
      
      const formData = new FormData();
      formData.append('file', file);

      console.log('Sending request to:', 'http://localhost:8000/api/v1/classify');
      const response = await fetch('http://localhost:8000/api/v1/classify', {
        method: 'POST',
        body: formData
      });

      console.log('Response status:', response.status);
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Server response:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const result = await response.json();
      console.log('Classification result:', result);
      this.showSuccess('Image classified successfully!');
      this.onClassificationComplete(result);
      
    } catch (error) {
      console.error('Upload error:', error);
      this.showError('Failed to upload and classify image. Please try again.');
    }
  }

  showStatus(message) {
    console.log('Status:', message);
    this.uploadStatus.textContent = message;
    this.uploadStatus.className = 'upload-status status-info';
  }

  showSuccess(message) {
    console.log('Success:', message);
    this.uploadStatus.textContent = message;
    this.uploadStatus.className = 'upload-status status-success';
  }

  showError(message) {
    console.error('Error:', message);
    this.uploadStatus.textContent = message;
    this.uploadStatus.className = 'upload-status status-error';
  }

  reset() {
    this.uploadForm.reset();
    this.uploadStatus.textContent = '';
    this.uploadStatus.className = 'upload-status';
  }
}

export default UploadComponent; 