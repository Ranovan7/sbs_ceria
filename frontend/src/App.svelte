<script>
	import "./css/bulma.min.css";

	import Router from 'svelte-spa-router';
	import { onDestroy, onMount } from 'svelte';
    import { location } from 'svelte-spa-router';

	import routes from './routes';
	import Nav from './components/Nav.svelte';
</script>

<style>

</style>

<main>
	{#if $location != '/login'}
		<Nav />
	{/if}

	<div class="container">
		<Router {routes} />
	</div>
</main>
