<script>
    import { onMount } from 'svelte';

	import Navbar from '$components/Navbar.svelte';
    import Notification from '$components/Notification.svelte';

    export let page = "";
    export let user;

    onMount(() => {
        page = window.location.href.split('/')[3];
        console.log(page);
        if (page != "login") {
            authorizeUser(getAuthToken());

            getJsonData(backend + "/info")
                .then(data => {
                    console.log(data);
                    if (data.username) {
                        user = data;
                    } else {
                        alert(data.detail);
                    }
                })
                .catch(error => console.log(error));
        }
	});
</script>

<main>
    {#if page != 'login'}
    	<Navbar />
    {/if}

    <!-- {#each notifications as notif}
        <div class="container">
            <div class="notification is-{notif.type} mt-1 mb-1" id="notif" transition:fly={{ x: 350, duration: 500 }}>
                <button
                    class="delete"
                    on:click={() => nodeRef.parentNode.removeChild(nodeRef)}>
                </button>
                {notif.message}
            </div>
        </div>
    {/each} -->

	<slot></slot>
</main>

<style>

</style>
