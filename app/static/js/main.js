

function formToJson(form){
    let data = new FormData(form);
    let results = {};

    for (let key of data.keys()) {
  	   results[key] = data.get(key);
  	}

    return results;
}

function toggleModal(id, callback) {
  var element = document.getElementById(id);
  if (element.classList.contains('is-active')) {
    element.classList.remove("is-active");
    element.classList.remove("is-clipped");
  } else {
    element.classList.add("is-active");
    element.classList.add("is-clipped");

    if (callback) {
      callback();
    }
  }
}

function toggleCollapsible(id, callback) {
  var element = document.getElementById(id);
  if (element.classList.contains('collapse')) {
    element.classList.add("show");
    element.classList.remove("collapse");
    console.log("Show Collapsible");
  } else {
    element.classList.add("collapse");
    element.classList.remove("show");

    if (callback) {
      callback();
    }
  }
}

function sendPostRequest(endpoint, data, callback){
  fetch(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-type': 'application/json; charset=UTF-8'
      }
    }).then(function (response) {
      if (response.ok) {
        return response.json();
      }
      return Promise.reject(response);
    }).then(function (data) {
      console.log(data);
      callback(data);
    }).catch(function (error) {
      console.warn('Something went wrong.', error);
    });
}

function showMessage(message, type) {
  var elem = document.getElementById('notification');
}

function closeNotification(id) {
  notif = document.getElementById(id);
  notif.parentNode.remove(notif);
}
