<script>
    export let message = "This is a message";
    export let type = "danger";

    let nodeRef
</script>

<div class="container">
    <div bind:this={nodeRef}>
        <div class="notification is-{type} mt-1 mb-1" id="notif">
            <button
                class="delete"
                on:click={() => nodeRef.parentNode.removeChild(nodeRef)}>
            </button>
            {message}
        </div>
    </div>
</div>
