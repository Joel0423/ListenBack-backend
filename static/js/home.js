// ListenBack Home Page JS
// All previous functionality is preserved and improved for Tailwind UI

let userType = null;
let uid = null;
let classrooms = [];
let currentClassroom = null;
let currentLecture = null;
let rag_file_id = null;

function goHome() {
    document.getElementById('login-section').classList.remove('hidden');
    document.getElementById('home-section').classList.add('hidden');
    document.getElementById('classroom-section').classList.add('hidden');
    document.getElementById('lecture-section').classList.add('hidden');
    document.getElementById('home-btn').classList.add('hidden');
}

function login(type) {
    userType = type;
    uid = (type === 'student') ? 'Lv2BbNg70YOykAqJtHGqe5RkRoq1' : '2S1z2UrNRweQtOHEgg4QNo0aEX32';
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('home-btn').classList.remove('hidden');
    loadHome();
}

async function loadHome() {
    document.getElementById('home-section').classList.remove('hidden');
    document.getElementById('classroom-section').classList.add('hidden');
    document.getElementById('lecture-section').classList.add('hidden');
    let html = `<h2 class='text-2xl font-semibold mb-4'>Welcome, ${userType.charAt(0).toUpperCase() + userType.slice(1)}</h2>`;
    html += `<div class='mb-4'>`;
    if (userType === 'teacher') {
        html += `<button class='px-4 py-2 bg-blue-700 text-white rounded-lg mr-2' onclick='showCreateClassroom()'>Create Classroom</button>`;
    } else {
        html += `<button class='px-4 py-2 bg-green-600 text-white rounded-lg' onclick='showJoinClassroom()'>Join Classroom</button>`;
    }
    html += `</div><div id='classroom-list' class='grid grid-cols-1 md:grid-cols-2 gap-6'></div>`;
    document.getElementById('home-section').innerHTML = html;
    await fetchClassrooms();
}

async function fetchClassrooms() {
    let res = await fetch(`/classrooms?uid=${uid}`);
    let data = await res.json();
    classrooms = data.classrooms || [];
    let listHtml = '';
    if (classrooms.length === 0) listHtml = '<p class="text-gray-500">No classrooms found.</p>';
    classrooms.forEach(detail => {
        listHtml += `<div class='bg-white rounded-xl shadow-md p-6 flex flex-col justify-between'>`;
        listHtml += `<div><span class='classroom-title text-xl font-bold text-blue-900'>${detail.subject}</span><br><span class='text-gray-700'>${detail.description}</span><br>Code: <b class='text-blue-700'>${detail.code}</b></div>`;
        listHtml += `<button class='mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg' onclick='enterClassroom("${detail.classroom_id}")'>Enter</button>`;
        listHtml += `</div>`;
    });
    document.getElementById('classroom-list').innerHTML = listHtml;
}

function showCreateClassroom() {
    document.getElementById('home-section').innerHTML += `<div id='create-classroom' class='mt-6'><h3 class='text-lg font-semibold mb-2'>Create Classroom</h3><input id='subject' class='border rounded-lg px-3 py-2 mb-2 w-full' placeholder='Subject'><br><input id='desc' class='border rounded-lg px-3 py-2 mb-2 w-full' placeholder='Description'><br><button class='px-4 py-2 bg-blue-700 text-white rounded-lg' onclick='createClassroom()'>Create</button></div>`;
}
async function createClassroom() {
    let subject = document.getElementById('subject').value;
    let desc = document.getElementById('desc').value;
    let fd = new FormData();
    fd.append('uid', uid);
    fd.append('subject', subject);
    fd.append('description', desc);
    let res = await fetch('/classrooms', { method: 'POST', body: fd });
    if (res.ok) { document.getElementById('create-classroom').remove(); await fetchClassrooms(); }
}
function showJoinClassroom() {
    document.getElementById('home-section').innerHTML += `<div id='join-classroom' class='mt-6'><h3 class='text-lg font-semibold mb-2'>Join Classroom</h3><input id='join-code' class='border rounded-lg px-3 py-2 mb-2 w-full' placeholder='Classroom Code'><br><button class='px-4 py-2 bg-green-600 text-white rounded-lg' onclick='joinClassroom()'>Join</button></div>`;
}
async function joinClassroom() {
    let code = document.getElementById('join-code').value;
    let fd = new FormData();
    fd.append('uid', uid);
    fd.append('code', code);
    let res = await fetch('/classrooms/join', { method: 'POST', body: fd });
    if (res.ok) { document.getElementById('join-classroom').remove(); await fetchClassrooms(); }
}
async function enterClassroom(classroom_id) {
    document.getElementById('home-section').classList.add('hidden');
    document.getElementById('classroom-section').classList.remove('hidden');
    document.getElementById('lecture-section').classList.add('hidden');
    currentClassroom = classroom_id;
    let res = await fetch(`/classrooms/details?classroom_id=${classroom_id}`);
    let data = await res.json();
    let html = `<div class='flex items-start mb-4'><button class='px-4 py-2 bg-gray-300 text-blue-900 rounded-lg border border-gray-400 mr-4' onclick='loadHome()'>Back</button></div>`;
    html += `<h2 class='text-2xl font-bold text-blue-900 mb-2 text-center'>${data.subject}</h2><p class='mb-4 text-gray-700 text-center'>${data.description}</p>`;
    html += `<div id='lecture-list' class='flex flex-col items-center justify-center min-h-[40vh] w-full'></div>`;
    if (userType === 'teacher') {
        html += `<div class='flex justify-center'><button class='px-4 py-2 bg-blue-700 text-white rounded-lg mb-4' onclick='showCreateLecture()'>Create Lecture</button></div>`;
    }
    document.getElementById('classroom-section').innerHTML = html;
    await fetchLectures(classroom_id);
}
async function fetchLectures(classroom_id) {
    let res = await fetch(`/classrooms/lectures?classroom_id=${classroom_id}`);
    let data = await res.json();
    let lectures = data.lectures || [];
    let listHtml = '';
    if (lectures.length === 0) listHtml = '<p class="text-gray-500 text-center">No lectures found.</p>';
    listHtml += `<div class='flex flex-col items-center w-full'>`;
    lectures.forEach(l => {
        listHtml += `<div class='bg-white rounded-xl shadow-md p-6 flex flex-col justify-between w-full max-w-xl mb-4 text-center'>`;
        listHtml += `<span class='text-lg font-semibold text-blue-900 mb-2'>${l.title}</span>`;
        listHtml += `<button class='mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg' onclick='enterLecture("${l.lecture_id}")'>View</button>`;
        listHtml += `</div>`;
    });
    listHtml += `</div>`;
    document.getElementById('lecture-list').innerHTML = listHtml;
}
function showCreateLecture() {
    document.getElementById('classroom-section').innerHTML += `<div id='create-lecture' class='mt-6'><h3 class='text-lg font-semibold mb-2'>Create Lecture</h3><input id='lecture-title' class='border rounded-lg px-3 py-2 mb-2 w-full' placeholder='Title'><br><input type='file' id='lecture-file' class='mb-2'><br><button class='px-4 py-2 bg-blue-700 text-white rounded-lg' onclick='createLecture()'>Upload</button></div>`;
}
async function createLecture() {
    let title = document.getElementById('lecture-title').value;
    let file = document.getElementById('lecture-file').files[0];
    let fd = new FormData();
    fd.append('classroom_id', currentClassroom);
    fd.append('title', title);
    fd.append('file', file);
    let res = await fetch('/lectures/upload', { method: 'POST', body: fd });
    if (res.ok) { document.getElementById('create-lecture').remove(); await fetchLectures(currentClassroom); }
}
async function enterLecture(lecture_id) {
    document.getElementById('home-section').classList.add('hidden');
    document.getElementById('classroom-section').classList.add('hidden');
    document.getElementById('lecture-section').classList.remove('hidden');
    currentLecture = lecture_id;
    let res = await fetch(`/lectures?classroom_id=${currentClassroom}&lecture_id=${lecture_id}`);
    let data = await res.json();
    let lecture = data.lecture;
    rag_file_id = lecture.rag_file_id;
    let html = `<div class='flex justify-between items-center mb-4'><button class='px-4 py-2 bg-gray-300 text-blue-900 rounded-lg border border-gray-400 mr-4' onclick='enterClassroom("${currentClassroom}")'>Back</button></div>`;
    html += `<div class='flex flex-col md:flex-row gap-8'>`;
    html += `<div class='flex-1 bg-white rounded-xl shadow-md p-8 mb-6'>`;
    html += `<h2 class='text-2xl font-bold text-blue-900 mb-2'>${lecture.title}</h2>`;
    if (lecture.media_url) {
        if (lecture.media_url.endsWith('.mp4')) {
            html += `<video src='${lecture.media_url}' controls class='w-full max-w-md rounded-lg shadow mb-4 border border-blue-200'></video>`;
        } else {
            html += `<audio src='${lecture.media_url}' controls class='w-full max-w-md rounded-lg shadow mb-4 border border-blue-200'></audio>`;
        }
    }
    if (lecture.transcription) {
        html += `<div class='bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4'><h4 class='text-lg font-semibold text-blue-700 mb-2'>Transcript</h4><pre class='whitespace-pre-wrap text-gray-800 text-sm'>${lecture.transcription}</pre></div>`;
    }
    html += `</div>`;
    html += `<div class='flex-1'><div class='bg-white rounded-xl shadow-md p-8 border border-gray-200'><h3 class='text-lg font-semibold mb-4 text-blue-900'>Chat</h3><div class='chat-history space-y-2 mb-4' id='chat-history'></div><div class='flex'><input class='chat-input border rounded-lg px-3 py-2 flex-1 mr-2' id='chat-input' placeholder='Ask a question...'><button class='px-4 py-2 bg-blue-700 text-white rounded-lg' onclick='askQuestion()'>Ask</button></div></div></div>`;
    html += `</div>`;
    document.getElementById('lecture-section').innerHTML = html;
    await fetchChatHistory();
}
async function askQuestion() {
    let question = document.getElementById('chat-input').value;
    if (!question) return;
    let res = await fetch(`/ask?uid=${uid}&lecture_id=${currentLecture}&rag_file_id=${rag_file_id}&question=${encodeURIComponent(question)}`);
    let data = await res.json();
    let historyDiv = document.getElementById('chat-history');
    historyDiv.innerHTML += `<div class=''><span class='font-semibold text-blue-900'>You:</span> ${question}</div><div class=''><span class='font-semibold text-green-700'>Bot:</span> ${data.answer}</div>`;
    document.getElementById('chat-input').value = '';
}
async function fetchChatHistory() {
    let res = await fetch(`/ask/history?uid=${uid}&lecture_id=${currentLecture}`);
    let data = await res.json();
    let history = data.history || [];
    let historyDiv = document.getElementById('chat-history');
    historyDiv.innerHTML = '';
    history.forEach(h => {
        if (h.role === 'user') {
            historyDiv.innerHTML += `<div class=''><span class='font-semibold text-blue-900'>You:</span> ${h.parts[0]}</div>`;
        } else if (h.role === 'model') {
            historyDiv.innerHTML += `<div class=''><span class='font-semibold text-green-700'>Bot:</span> ${h.parts[0]}</div>`;
        }
    });
}
