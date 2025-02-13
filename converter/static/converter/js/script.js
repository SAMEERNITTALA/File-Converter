// converter/static/converter/js/script.js
document.getElementById('fileInput').addEventListener('change', function (e) {
    const files = e.target.files;
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const div = document.createElement('div');
        div.textContent = `${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
        fileList.appendChild(div);
    }
    document.getElementById('fileCount').textContent = `Added ${files.length} Files`;
});

function toggleDropdown() {
    const dropdown = document.getElementById('dropdownContent');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

function showOptions(type) {
    const options = document.getElementById('options');
    options.innerHTML = '';
    const imageOptions = ['BMP', 'EPS', 'GIF', 'ICO', 'JPEG', 'JPG', 'ODD', 'PNG', 'PSD', 'SVG', 'TGA', 'TIFF', 'WebP'];
    const documentOptions = ['DOC', 'DOCX', 'EXCEL', 'HTML', 'ODT', 'PPT', 'PPTX', 'PS', 'RTF', 'TEXT', 'TXT', 'WORD', 'XLS', 'XLSX'];
    const list = type === 'image' ? imageOptions : documentOptions;
    list.forEach(option => {
        const button = document.createElement('button');
        button.textContent = option;
        button.onclick = () => selectOption(option);
        options.appendChild(button);
    });
}

function selectOption(option) {
    document.getElementById('outputType').querySelector('button').textContent = option;
    toggleDropdown();
}

function openAdvancedSettings() {
    document.getElementById('advancedSettings').style.display = 'block';
}

function applySettings() {
    document.getElementById('advancedSettings').style.display = 'none';
}

// converter/static/converter/js/script.js
function convertFiles() {
    const fileInput = document.getElementById('fileInput');
    const outputFileType = document.querySelector('#outputType button').textContent.toLowerCase();

    if (!fileInput.files || fileInput.files.length === 0) {
        alert("Please select a file to convert.");
        return;
    }

    if (!outputFileType) {
        alert("Please select an output file type.");
        return;
    }

    const formData = new FormData();

    // Add files to FormData
    for (let i = 0; i < fileInput.files.length; i++) {
        formData.append('files', fileInput.files[i]);
    }

    // Add output file type
    formData.append('output_file_type', outputFileType);

    // Add CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    formData.append('csrfmiddlewaretoken', csrfToken);

    // Send POST request to backend
    fetch('/convert/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest', // Indicate AJAX request
        },
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        throw new Error('File conversion failed');
    })
    .then(blob => {
        // Trigger file download
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `converted_file.${outputFileType}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('File conversion failed. Please try again.');
    });
}