<script>
    let message = "This is a message";
    let type = "danger";

    let nodeRef
</script>

<div bind:this={nodeRef}>
    <div class="notification is-{type} mt-1 mb-1" id="notif" transition:fly={{ x: 350, duration: 500 }}>
        <button
            class="delete"
            on:click={() => nodeRef.parentNode.removeChild(nodeRef)}>
        </button>
        {message}
    </div>
</div>
