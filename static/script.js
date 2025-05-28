const form = document.getElementById('uploadForm');
const dropzone = document.getElementById('dropzone');
const content = document.getElementById('dropzoneContent');
const fileInput = document.getElementById('fileInput');

// Clic sul dropzone apre il selettore file
dropzone.addEventListener('click', () => fileInput.click());

// Trascina sopra: evidenzia
dropzone.addEventListener('dragover', e => {
  e.preventDefault();
  dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => {
  dropzone.classList.remove('dragover');
});

// Funzione per aggiornare la lingua selezionata
function setupLanguageSelection() {
  const languageItems = document.querySelectorAll('#langList li');

  languageItems.forEach(item => {
    item.addEventListener('click', () => {
      // Rimuove il selezionato da tutti
      languageItems.forEach(el => el.classList.remove('selected'));

      // Aggiunge il selezionato a quello cliccato
      item.classList.add('selected');

      // Imposta il valore effettivo nell'input nascosto
      document.getElementById('langInput').value = item.dataset.lang;
    });
  });
}

// Esegui subito all'avvio
setupLanguageSelection();


// Droppa file
dropzone.addEventListener('drop', e => {
  e.preventDefault();
  dropzone.classList.remove('dragover');
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    fileInput.files = files;
    handleFileDisplay(files[0]);
  }
});

// Cambio manuale del file (click)
fileInput.addEventListener('change', () => {
  if (fileInput.files.length > 0) {
    handleFileDisplay(fileInput.files[0]);
  }
});

// Funzione che aggiorna il contenuto del dropzone
function handleFileDisplay(file) {
  const content = document.getElementById('dropzoneContent');
  if (!file) return;

  if (file.type.startsWith("image/")) {
    const reader = new FileReader();
    reader.onload = function (e) {
      content.innerHTML = `
        <img src="${e.target.result}" alt="Anteprima" style="max-width: 100%; max-height: 150px; border-radius: 6px;"/>
        <p>${file.name}</p>
      `;
    };
    reader.readAsDataURL(file);
  } else {
    content.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="#ccc" viewBox="0 0 24 24">
        <path d="M4 4h16v16H4z" fill="none"/>
        <path d="M14 2H6c-1.1 0-2 .9-2 2v16a2 2 0 0 0 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm1 7V3.5L18.5 9H15z" fill="#ccc"/>
      </svg>
      <p>${file.name}</p>
    `;
  }

  // (Non necessario, ma sicuro)
  setupLanguageSelection();
}

// Submit normale
form.addEventListener('submit', async function (e) {
  e.preventDefault();
  const formData = new FormData(form);
  const response = await fetch('/process', {
    method: 'POST',
    body: formData
  });
  const data = await response.json();
  document.getElementById('result').innerText = data.summary;
});
