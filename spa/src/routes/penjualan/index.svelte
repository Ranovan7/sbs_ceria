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

	export function preload() {
		// return this.fetch(`penjualan.json`).then(r => r.json()).then(posts => {
		// 	return { posts };
		// });
	}
</script>

<style>

</style>

<svelte:head>
	<title>Penjualan</title>
</svelte:head>

<div class="container">
    <h1 class="title">Penjualan</h1>

</div>
