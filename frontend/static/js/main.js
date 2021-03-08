

var backend = "localhost:8000";
var user = {
    'username': null,
    'role': null
}
var auth_token = getAuthToken();
var notifications = [];

function addNotif(message, type) {
    notifications = [...notifications, {
        message: message,
        type: type
    }];
    notifications = notifications;
    console.log(notifications);
}

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json'
          'Authorization': auth_token,
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

function getCookies() {
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    return ca;
}

function getAuthToken() {
    let name = "Authorization=";
    let ca = getCookies();
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function authorizeUser(auth_token) {
    if (auth_token) {
        console.log(auth_token);
    } else {
        window.location.href = '/login';
        return ""
    }
}
