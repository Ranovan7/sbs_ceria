<script>
    import { goto, stores } from '@sapper/app';
    import Notification from '../components/Notification.svelte';

    const { session, page} = stores();
    const { message } = $page.query;
    const { BACKEND } = $session;

    let password = "";
    let username = "";
    console.log(message);

    console.log(BACKEND);

    function setAuthToken(token) {
        var d = new Date();
        d.setTime(d.getTime() + (1*24*60*60*1000));
        var expires = "expires="+ d.toUTCString();
        document.cookie = 'auth_token' + "=" + token + ";" + expires + ";path=/";
    }

    const handleLogin = async () => {
        let formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        console.log(username);

        const response = await fetch(BACKEND + "/token", {
          method: "POST",
          body: formData,
        });

        const parsed = await response.json();

        if (parsed.access_token) {
          setAuthToken(parsed.access_token);
          goto("/");
        } else {
          message = parsed.detail;
          console.log(parsed.detail);
        }
    };
</script>

<svelte:head>
	<title>Login</title>
</svelte:head>

{#if message}
    <Notification {message}/>
{/if}

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
      <form on:submit|preventDefault="{handleLogin}" method="post">
        <div class="pt-2 pb-2">
          <label class="label" for="username">Username</label>
          <input class="input is-primary" type="text" name="username" bind:value="{username}">
        </div>
        <div class="pt-2 pb-2">
          <label class="label" for="password">Password</label>
          <input class="input is-primary" type="password" name="password" bind:value="{password}">
        </div>
        <div class="pt-2 pb-2">
          <input class="button is-link" type="submit" value="Login">
        </div>
      </form>
    </div>
  </div>
  <div class="column">

  </div>
</div>
