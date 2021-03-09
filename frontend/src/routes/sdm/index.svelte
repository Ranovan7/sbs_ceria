<script>
    import { onMount } from 'svelte';

    let user;
    onMount(() => {
        getJsonData(backend + "/info")
            .then(data => {
                console.log(data);
                if (data.username) {
                    if (data.role != "admin") {
                        console.log("You're not Admin");
                        window.location.href = '/penjualan';
                    }
                } else {
                    alert(data.detail);
                }
            })
            .catch(error => console.log(error));
    });
</script>

<div class="container">
    <h1 class="title">SDM</h1>
</div>
