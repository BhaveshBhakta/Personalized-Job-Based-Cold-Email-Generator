const fileInput = document.getElementById('resume_file');
const fileUploadArea = document.getElementById('fileUploadArea');
const fileInfo = document.getElementById('fileInfo');
const form = document.getElementById('emailForm');
const submitBtn = document.getElementById('submitBtn');

// File uploading interactions

fileUploadArea.addEventListener('click', () => fileInput.click());

fileUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadArea.classList.add('dragover');
});

fileUploadArea.addEventListener('dragleave', () => {
    fileUploadArea.classList.remove('dragover');
});

fileUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        updateFileInfo(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        updateFileInfo(e.target.files[0]);
    }
});

function updateFileInfo(file) {
    const fileSize = (file.size / 1024 / 1024).toFixed(2);
    fileInfo.innerHTML = `
                <div class="file-selected">
                    <i class="fas fa-file-alt"></i>
                    <span class="file-name">${file.name}</span>
                    <span class="file-size">${fileSize} MB</span>
                    <button type="button" class="remove-file" onclick="removeFile()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
    fileInfo.style.display = 'block';
}

function removeFile() {
    fileInput.value = '';
    fileInfo.style.display = 'none';
}

// Form submission handling

form.addEventListener('submit', (e) => {
    submitBtn.classList.add('loading');
});

// Copy to clipboard function

function copyToClipboard() {
    const emailContent = document.querySelector('#emailContent pre').textContent;
    navigator.clipboard.writeText(emailContent).then(() => {
        showNotification('Email copied to clipboard!', 'success');
    });
}

// Download email function

function downloadEmail() {
    const emailContent = document.querySelector('#emailContent pre').textContent;
    const blob = new Blob([emailContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'cold-email.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    showNotification('Email downloaded!', 'success');
}

// Notification system

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check' : 'exclamation'}"></i>
                ${message}
            `;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// URL validation

document.getElementById('job_url').addEventListener('blur', function () {
    const url = this.value;
    if (url && !isValidURL(url)) {
        this.classList.add('invalid');
        showNotification('Please enter a valid URL', 'error');
    } else {
        this.classList.remove('invalid');
    }
});

function isValidURL(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}