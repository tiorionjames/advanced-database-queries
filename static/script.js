const entryList = document.getElementById('entry-list');
const createButton = document.getElementsByTagName('button')[0];
const entryDetails = document.getElementById('entry-details');
if(entryList) {
    loadJournalEntries();
}
if(createButton) {
    createButton.addEventListener('click', createNewEntry);
}
if(entryDetails) {
    loadJournalEntry();
}

async function loadJournalEntry() {
    const noteId = location.href.match(/(\d+)$/)[1];
    try {
        const response = await fetch(`/api/entries/${noteId}`);
        if (!response.ok) { 
            throw new Error(`${response.status}`);
        }
        const entry = await response.json();

        document.getElementById('posted_date').innerHTML = entry.posted_date;
        document.getElementById('title').innerHTML = entry.title || '(none)';
        document.getElementById('body').innerHTML = entry.body;
        document.getElementById('edit-link').href = `/update-entry.html?id=${entry.id}`;
    } catch (error) {
        console.error('Error occurred while loading journal entry', error);
    }
}

async function createNewEntry(event) {
    event.preventDefault();
    const body = JSON.stringify({
        posted_date: document.getElementById('posted_date').value,
        title: document.getElementById('title').value,
        body: document.getElementById('body').value
    });
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'        
    };

    try {
        const response = await fetch('/api/entries', {
            'method': 'POST',
            headers,
            body
        });
        if (!response.ok) { 
            throw new Error(`${response.status}`);
        }
        location.href = '/all-entries.html';
    } catch (error) {
        console.error('Error occurred while creating a new journal entry', error);
    }
}

async function loadJournalEntries() {
    try {
        const response = await fetch('/api/entries');
        if (!response.ok) { 
            throw new Error(`${response.status}`);
        }
        const entries = await response.json();

        for(let entry of entries) {
            const node = document.createElement('div');
            // node.href=`/entry.html?id=${entry.id}`;
            node.classList.add('entry');
            node.innerHTML = `
                    <a href="/entry.html?id=${entry.id}"><div class="posted_date">${entry.posted_date}</div></a>
                    <a href="/entry.html?id=${entry.id}"><div class="title">${entry.title || '(none)'}</div></a>
                    <div class="delete" data-entry-id="${entry.id}"><button>X</button></div>
            `;
            entryList.appendChild(node);
            entryList.addEventListener('click', handleDelete);
        }
    } catch (error) {
        console.error('error occurred while loading all entries', error);
    }
}

async function handleDelete(event) {
    const parentNode = event.target.parentElement;
    if(! parentNode.classList.contains('delete')) {
        return;
    }
    const entryId = parentNode.dataset.entryId;
    try {
        const response = await fetch(`/api/entries/${entryId}`, {
            method: 'DELETE'
        });
        if (!response.ok) { 
            throw new Error(`${response.status}`);
        }
        location.href = '/all-entries.html';
    } catch (error) {
        console.error('Error occurred while deleting a journal entry', error);
    }
}
