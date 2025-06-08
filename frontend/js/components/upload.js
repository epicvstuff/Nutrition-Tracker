class UploadComponent {
  constructor(onFoodClassified) {
    this.onFoodClassified = onFoodClassified;
    this.uploadForm = document.getElementById('upload-form');
    this.uploadStatus = document.getElementById('upload-status');
    
    this.bindEvents();
  }

  bindEvents() {
    this.uploadForm.addEventListener('submit', this.handleUpload.bind(this));
  }

  async handleUpload(event) {
    event.preventDefault();
    this.uploadStatus.textContent = 'Uploading and classifying image...';

    const fileInput = this.uploadForm.querySelector('input[type="file"]');
    const file = fileInput.files[0];
    
    if (!file) {
      this.uploadStatus.textContent = 'Please select an image file.';
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/classify', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }

      const data = await response.json();
      if (data.error) {
        throw new Error(data.error);
      }

      this.handleClassificationSuccess(data);
    } catch (error) {
      this.handleError(error);
    }
  }

  handleClassificationSuccess(data) {
    this.onFoodClassified(data);
    this.uploadStatus.textContent = `Image classified as: ${data.predicted_class}. You can adjust details if needed.`;
    this.uploadStatus.className = 'upload-status success';
  }

  handleError(error) {
    console.error('Upload error:', error);
    this.uploadStatus.textContent = 'Error during classification. Please try again.';
    this.uploadStatus.className = 'upload-status error';
  }
}

export default UploadComponent; 