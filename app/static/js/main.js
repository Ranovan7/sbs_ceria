
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

async function postData(url = '', data) {
    // data has to be formData
    const response = await fetch(url, {
        method: 'POST',
        body: data
    });

    const result = await response.json();

    return result;
}

async function getJsonData(url = '') {
    const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getAuthToken()}`,
        },
    });

    const result = await response.json();

    return result;
}

async function postJsonData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAuthToken()}`,
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    return result;
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookies() {
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    return ca;
}

function setAuthToken(token) {
    // console.log(token);
    setCookie('auth_token', token, 1);
}

function getAuthToken() {
    let name = "auth_token=";
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

function closeModalEl(modal_id) {
    // const modal = new bootstrap.Modal(document.getElementById(modal_id));
    // modal.hide();

    let modal = document.getElementById(modal_id);
    modal.classList.remove("show");
    modal.style.display = 'none';
    modal.removeAttribute("role");
    modal.removeAttribute("aria-modal");
    modal.setAttribute("aria-hidden", "true");

    let backdrops = document.getElementsByClassName("modal-backdrop");
    for (let el of backdrops) {
        console.log(el);
        el.parentNode.removeChild(el);
    }
}
