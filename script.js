document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const convertBtn = document.getElementById('convert-btn');
    const downloadLink = document.getElementById('download-link');

    let editor;

    // Initialize EasyMDE
    editor = new EasyMDE({
        element: document.getElementById('editor'),
        spellChecker: false,
        renderingConfig: {
            singleLineBreaks: false,
            codeSyntaxHighlighting: true,
        }
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const file = fileInput.files[0];
        if (!file) {
            alert('Please select a PDF file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        convertBtn.disabled = true;
        convertBtn.textContent = 'Converting...';

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (response.ok) {
                editor.value(data.markdown);
                downloadLink.style.display = 'inline-block';
                downloadLink.textContent = 'Download Markdown';
                downloadLink.onclick = function(e) {
                    e.preventDefault();
                    const markdownContent = editor.value();
                    const blob = new Blob([markdownContent], { type: 'text/markdown' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = file.name.replace(/\.pdf$/i, '.md');
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                };
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            convertBtn.disabled = false;
            convertBtn.textContent = 'Convert';
        }
    });
});

// Shutdown server when browser closes
window.addEventListener('beforeunload', function() {
    navigator.sendBeacon('/shutdown', '');
});