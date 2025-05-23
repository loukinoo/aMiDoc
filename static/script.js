document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const response = await fetch('/process', {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    document.getElementById('result').innerText = data.summary;
  });
  