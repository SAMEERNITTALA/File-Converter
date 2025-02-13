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

function convertFiles() {
    alert('Conversion started...');
    location.reload();
}