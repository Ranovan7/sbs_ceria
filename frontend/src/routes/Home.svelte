<script>
    import { beforeUpdate } from 'svelte';
    import { replace } from 'svelte-spa-router';
    import { user } from '../stores';

    beforeUpdate(() => {
		if ($user.role == 'admin') {
            console.log("is Admin");
            replace("/sdm");
        } else if ($user.role == 'sales') {
            console.log("is Sales");
            replace("/penjualan");
        }
	});
</script>

<div align="center">
    <h1>SBSEHATI APP</h1>
</div>

<style>
	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}
</style>
