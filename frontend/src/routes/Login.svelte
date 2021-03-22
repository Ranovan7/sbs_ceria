<script>
    import { postData, getJsonData, setAuthToken } from '../utils';
    import { backend, user } from '../stores';
    import { replace } from 'svelte-spa-router';

    function login() {
        let formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        postData($backend + "/token", formData)
            .then(result => {
                if (result.access_token) {
                    setAuthToken(result.access_token);

                    getJsonData($backend + "/info")
                        .then(user_info => {
                            if (user_info.username) {
                                $user = user_info;
                                console.log($user);
                                replace("/");
                            } else {
                                alert(user_info.detail);
                            }
                        });
                } else {
                    console.log(result.detail);
                    alert(result.detail);
                }
            });
    }

    let username;
    let password;
</script>

<svelte:head>
    <title>SBSehati - Login</title>
</svelte:head>

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
          <input class="input is-primary" type="text" name="username" bind:value="{username}">
        </div>
        <div class="pt-2 pb-2">
          <label class="label" for="password">Password</label>
          <input class="input is-primary" type="password" name="password" bind:value="{password}">
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
