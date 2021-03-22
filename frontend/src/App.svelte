<script>
	import "./css/bulma.min.css";

	import Router from 'svelte-spa-router';
	import { onMount } from 'svelte';
    import { location, replace } from 'svelte-spa-router';

	import routes from './routes';
	import { getCookie, getAuthToken, getJsonData } from './utils';
	import { backend, user } from './stores';

	import Nav from './components/Nav.svelte';

	onMount(async () => {
		$backend = `process.env.BACKEND`;
		console.log($backend);
		console.log($location);

		if ($location != '/login') {
			const auth_token = getAuthToken();

			if (auth_token) {
				getJsonData($backend + "/info")
					.then(user_info => {
						if (user_info.username) {
							$user = user_info;
							console.log($user);
						} else {
							alert(user_info.detail);
						}
					});
			} else {
				alert("Not Authenticated, please Login");
				replace('/login');
			}
		}
	});
</script>

<style>

</style>

<svelte:head>
    <title>SBSehati</title>
</svelte:head>

<main>
	{#if $location != '/login'}
		<Nav />
	{/if}

	<div class="container">
		<Router {routes} />
	</div>
</main>
