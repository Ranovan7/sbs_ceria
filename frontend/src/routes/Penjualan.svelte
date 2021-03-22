<script>
    import { beforeUpdate } from 'svelte';
    import { replace } from 'svelte-spa-router';
    import { user } from '../stores';

    beforeUpdate(() => {
        if ($user.role != 'sales') {
            console.log("not Sales");
            replace("/");
        }
    });
</script>

<style>

</style>

<svelte:head>
    <title>SBSehati - Penjualan</title>
</svelte:head>

<h1 class="title">Penjualan</h1>
