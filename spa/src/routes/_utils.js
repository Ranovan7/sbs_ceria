
async function getConfig() {
    const configStr = document.getElementById("config");
    let jsonRes = await fetch(configStr.src, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
    });
    return jsonRes.json();
}

function* iter_range(begin,end,step) {
	// Normalize our inputs
	step = step ? step : 1;

	if (typeof(end) === 'undefined') {
		end   = begin > 0 ? begin : 0;
		begin = begin < 0 ? begin : 0;
	}

	if (begin == end) {
		return;
	}

	if (begin > end) {
		step = step * -1;
	}

	for (let x = begin; x < end; x += step) {
		yield x;
	}
}

function range(begin, end, step) {
	return Array.from(iter_range(begin,end,step));
}

function getAttr(dict, key, attr) {
    if (key in dict) {
        return dict[key][attr];
    } else {
        return "-"
    }
}

async function postData(url = '', data, withAuth = true) {
    // data has to be formData
    const response = await fetch(url, {
        method: 'POST',
        body: data
    });

    return response.json();
}

async function getJsonData(url = '') {
    const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getAuthToken()}`,
        },
    });

    return response.json();
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

    return response.json();
}

function getCookies() {
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    return ca;
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
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
