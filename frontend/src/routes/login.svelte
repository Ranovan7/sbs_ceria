<script>
    // import { onMount } from 'svelte';

    // console.log(user);

    function login() {
        let username = document.getElementsByName("username")[0].value;
        let password = document.getElementsByName("password")[0].value;

        addNotif("Info Salah", "danger");

        postData(backend + "/token", {username: username, password: password})
            .then(data => {
                if (data.access_token) {
                    setAuthToken(data.access_token);
                    window.location.href = '/';
                } else {
                    alert(data.detail);
                }
            })
            .catch(error => console.log(error));
    }

    // let user = "";
</script>

<br>
<br>

<div class="columns">
  <div class="column">

  </div>
  <div class="column">
    <div class="container box">
      <h1 class="title">
        SBSehati
      </h1>
        <div class="pt-2 pb-2">
          <label class="label" for="username">Username</label>
          <input class="input is-primary" type="text" name="username" value="">
        </div>
        <div class="pt-2 pb-2">
          <label class="label" for="password">Password</label>
          <input class="input is-primary" type="password" name="password" value="">
        </div>
        <div class="pt-2 pb-2">
          <!-- <input class="button is-link" type="submit" value="Login"> -->
          <button class="button is-link" on:click={login}>Login</button>
        </div>
    </div>
  </div>
  <div class="column">

  </div>
</div>
