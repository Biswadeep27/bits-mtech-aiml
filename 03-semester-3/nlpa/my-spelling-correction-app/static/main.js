document.addEventListener('DOMContentLoaded', () => {
    const manualText = document.getElementById('manual-text');
    const manualCorrectedText = document.getElementById('manual-corrected-text');
    const fileForm = document.getElementById('file-form');
    const fileInput = document.getElementById('file-input');
    const fileCorrectedText = document.getElementById('file-corrected-text');

    // Handle real-time text correction
    manualText.addEventListener('keyup', async () => {
        const text = manualText.value;
        if (text) {
            const response = await fetch('/correct', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            });
            const result = await response.json();
            manualCorrectedText.innerText = result.corrected_text;
        } else {
            manualCorrectedText.innerText = '';
        }
    });

    // Handle file upload and correction
    fileForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = async (e) => {
                const text = e.target.result;
                const response = await fetch('/correct', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: text })
                });
                const result = await response.json();
                fileCorrectedText.innerText = result.corrected_text;
            };
            reader.readAsText(file);
        }
    });
});
