<script>
    let pageName="Home Page";

    export let name = "World";

	let rando;

	$: result = Math.round(rando * 100);

	function setRando() {
		rando = Math.random();
	}
</script>

<main>
	<button on:click={setRando}>Randomize</button>

	<p>Your Score is { result }</p>

	{#if result > 75}
		<p>Winner 🧁🧁🧁</p>
	{:else if result > 50}
		<p>Decent Enough 🍡🍡🍡</p>
	{:else}
		<p>Loser 💩💩💩</p>
	{/if}
</main>

<style>
    main {
        text-align: center;
        padding: 1em;
        max-width: 240px;
        margin: 0 auto;
    }

    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
    }

    @media (min-width: 640px) {
        main {
            max-width: none;
        }
    }
</style>
