<script context="module">
	export function preload(page, session) {
        // return { path: page.path }
	}
</script>

<script>
    import { goto, stores } from '@sapper/app';

    const { session } = stores();
    const { user, BACKEND } = $session;

    // if (!$session.user) {
    //     console.log("User Not Found");
    //     getUser().catch(error => console.log(error));
    // } else {
    //     console.log("Already Logged In");
    //     if ($session.user.role == 'sales') {
	// 		goto(`/penjualan`);
	// 	} else {
	// 		goto(`/sdm`);
	// 	}
    // }
</script>

<style>

</style>

<svelte:head>
	<title>SDM</title>
</svelte:head>

<div class="container">
    <h1 class="title">SDM</h1>

</div>
