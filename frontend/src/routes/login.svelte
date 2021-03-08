<script>
    import { onMount } from 'svelte';

    console.log(user);

    function login() {
        let username = document.getElementsByName("username")[0].value;
        let password = document.getElementsByName("password")[0].value;

        addNotif("Info Salah", "danger");

        let logging_in = postData(backend + "/token");
        console.log(logging_in);
    }
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
