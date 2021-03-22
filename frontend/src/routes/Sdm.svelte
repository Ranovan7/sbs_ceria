<script>
    import { beforeUpdate } from 'svelte';
    import { replace } from 'svelte-spa-router';
    import { user } from '../stores';

    beforeUpdate(() => {
        if ($user.role != 'admin') {
            console.log("not Admin");
            replace("/");
        }
    });
</script>

<style>

</style>

<svelte:head>
    <title>SBSehati - SDM</title>
</svelte:head>

<h1 class="title">SDM</h1>
