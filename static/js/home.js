// Autoajustar altura del textarea y habilitar/deshabilitar botón de postear
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';

    const button = document.getElementById('tweet-submit');
    const content = textarea.value.trim();

    const isEmpty = (content === '') || (content === '{"ops":[{"insert":"\\n"}]}');
    button.disabled = isEmpty;
    button.classList.toggle('opacity-50', isEmpty);
}

document.addEventListener('DOMContentLoaded', function() {
    const avatarButton = document.getElementById('avatarButton');
    const dropdownMenu = document.getElementById('dropdownMenu');

    if (avatarButton && dropdownMenu) {
        avatarButton.addEventListener('click', function(event) {
            event.stopPropagation(); // Evita que el click propague al document
            dropdownMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', function(event) {
            if (!dropdownMenu.contains(event.target) && !avatarButton.contains(event.target)) {
                dropdownMenu.classList.add('hidden');
            }
        });
    }
});

// Eliminar HTML de un string
function stripHtml(html) {
    const div = document.createElement('div');
    div.innerHTML = html;
    return div.textContent || div.innerText || "";
}

// Obtener una cookie por nombre
function getCookie(name) {
    const cookies = document.cookie.split(';').map(c => c.trim());
    for (const cookie of cookies) {
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.slice(name.length + 1));
        }
    }
    return null;
}

// ================== MANEJO DE EMOJIS ==================

function toggleEmojiPicker() {
    const picker = document.getElementById('emoji-picker');
    picker.classList.toggle('hidden');

    if (picker.childElementCount === 0) {
        const emojis = ["😀", "😂", "😍", "😭", "😎", "😡", "👍", "🎉", "❤️", "🔥", "👀", "🥳"];
        emojis.forEach(emoji => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'text-2xl p-2 hover:bg-gray-700 rounded';
            button.textContent = emoji;
            button.onclick = () => insertEmoji(emoji);
            picker.appendChild(button);
        });
    }
}

function insertEmoji(emoji) {
    const textarea = document.getElementById('tweet-text');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    let text = textarea.value;

    try {
        const parsed = JSON.parse(text);
        if (parsed.ops && parsed.ops.length) {
            parsed.ops[0].insert = parsed.ops[0].insert.slice(0, start) + emoji + parsed.ops[0].insert.slice(end);
            textarea.value = JSON.stringify(parsed);
        }
    } catch {
        textarea.value = text.slice(0, start) + emoji + text.slice(end);
    }

    textarea.focus();
    textarea.selectionStart = textarea.selectionEnd = start + emoji.length;
    autoResize(textarea);
}

// ================== MANEJO DE IMÁGENES ==================

let uploadedImages = [];

function displayUploadedImages(files) {
    const existingPreview = document.getElementById('image-preview');
    if (existingPreview) existingPreview.remove();

    const previewContainer = document.createElement('div');
    previewContainer.id = 'image-preview';
    previewContainer.className = 'grid grid-cols-2 gap-2 mt-2';

    Array.from(files).forEach((file, index) => {
        if (!file.type.match('image.*')) return;

        const reader = new FileReader();
        reader.onload = e => {
            const previewDiv = document.createElement('div');
            previewDiv.className = 'relative';

            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'w-full h-32 object-cover rounded-lg';

            const deleteBtn = document.createElement('button');
            deleteBtn.innerHTML = '&times;';
            deleteBtn.className = 'absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm hover:bg-red-600';
            deleteBtn.onclick = () => removeImage(index);

            previewDiv.appendChild(img);
            previewDiv.appendChild(deleteBtn);
            previewContainer.appendChild(previewDiv);
        };
        reader.readAsDataURL(file);
    });

    document.getElementById('tweet-text').after(previewContainer);
    uploadedImages = Array.from(files);
}

function removeImage(index) {
    uploadedImages.splice(index, 1);

    const dataTransfer = new DataTransfer();
    uploadedImages.forEach(file => dataTransfer.items.add(file));
    document.getElementById('media-upload').files = dataTransfer.files;

    displayUploadedImages(uploadedImages);

    if (uploadedImages.length === 0) {
        const preview = document.getElementById('image-preview');
        if (preview) preview.classList.add('hidden');
    }
}

// ================== MANEJO DE PUBLICACIÓN ==================

async function postTweet(content, mediaFiles) {
    const formData = new FormData();
    formData.append('content', content);

    Array.from(mediaFiles).forEach(file => formData.append('media', file));

    return await fetch('/tweets/api/tweets/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    });
}

async function handleTweetSubmit(e) {
    e.preventDefault();

    const textarea = document.getElementById('tweet-text');
    let content = textarea.value.trim();
    const mediaFiles = document.getElementById('media-upload').files;

    if (!content) {
        alert('No puedes enviar un tweet vacío.');
        return;
    }

    try {
        const response = await postTweet(content, mediaFiles);
        const result = await response.json();

        if (response.ok) {
            // Limpiar el formulario
            textarea.value = '';
            document.getElementById('media-upload').value = '';
            const preview = document.getElementById('image-preview');
            if (preview) preview.remove();
            uploadedImages = [];
            autoResize(textarea);

            // Opción 1: Recargar la página para mostrar el nuevo tweet
            window.location.reload();

            // Opción 2: Alternativa sin recargar (añadir el tweet dinámicamente)
            // addNewTweetToTimeline(result.tweet);

            console.log('Tweet publicado correctamente', result);
        } else {
            console.error('Error al publicar el tweet', result.message);
            alert(`Error: ${result.message}`);
        }
    } catch (error) {
        console.error('Error de conexión', error);
        alert('Error al conectar con el servidor.');
    }
}


// ================== EVENTOS ==================

document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.getElementById('tweet-text');
    autoResize(textarea);

    document.getElementById('media-upload').addEventListener('change', e => {
        if (e.target.files.length > 0) displayUploadedImages(e.target.files);
    });

    document.getElementById('tweet-submit').addEventListener('click', handleTweetSubmit);

    document.getElementById('tweet-form').addEventListener('submit', e => {
        e.preventDefault();
        document.getElementById('tweet-submit').click();
    });
});


// ================== Buscador ==================


document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    let debounceTimer;

    // Manejador de eventos para el input
    searchInput.addEventListener('input', function(e) {
        clearTimeout(debounceTimer);
        const query = e.target.value.trim();

        if (query.length > 1) {  // Solo busca si hay al menos 2 caracteres
            debounceTimer = setTimeout(() => {
                fetchUsers(query);
            }, 300);
        } else {
            searchResults.classList.add('hidden');
        }
    });

    // Cerrar resultados al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!searchResults.contains(e.target) && e.target !== searchInput) {
            searchResults.classList.add('hidden');
        }
    });

    // Función para buscar usuarios
    function fetchUsers(query) {
        fetch(`/accounts/api/search/users/?q=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) throw new Error('Error en la búsqueda');
                return response.json();
            })
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                console.error('Error:', error);
                searchResults.innerHTML = `
                    <div class="px-4 py-2 text-red-400">
                        Error al buscar usuarios
                    </div>
                `;
                searchResults.classList.remove('hidden');
            });
    }

    // Mostrar resultados
    function displayResults(users) {
        if (users.length === 0) {
            searchResults.innerHTML = `
                <div class="px-4 py-2 text-gray-400">
                    No se encontraron usuarios
                </div>
            `;
            searchResults.classList.remove('hidden');
            return;
        }

        let html = '';
        users.forEach(user => {
            const profilePic = user.profile_picture || '/static/images/default-profile.png';
            html += `
                <a href="/accounts/profile/${user.username}/" class="flex items-center px-4 py-3 hover:bg-gray-700 transition">
                    <img src="${profilePic}"
                         alt="${user.full_name}"
                         class="w-10 h-10 rounded-full object-cover mr-3">
                    <div>
                        <div class="font-bold text-white">${user.full_name}</div>
                        <div class="text-gray-400 text-sm">@${user.username}</div>
                    </div>
                </a>
            `;
        });

        searchResults.innerHTML = html;
        searchResults.classList.remove('hidden');
    }
});