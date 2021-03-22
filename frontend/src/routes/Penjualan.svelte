<script>
    import { onMount } from 'svelte';
    import { replace } from 'svelte-spa-router';
    import moment from 'moment';

    import 'moment/locale/id';
    moment.locale('id');

    import { user, backend } from '../stores';
    import { getJsonData } from '../utils';

    let penjualan;

    onMount(() => {
        if ($user.role != 'sales') {
            console.log("not Sales");
            replace("/");
        }

        // fetch penjualan
        getJsonData($backend + "/api/penjualan")
            .then(results => {
                if (!results.detail) {
                    penjualan = results;
                    console.log(`${penjualan.length} Penjualan`);
                } else {
                    alert(results.detail);
                }
            }).catch(err => {
                console.error('Error:', err);
            });
    });
</script>

<style>

</style>

<svelte:head>
    <title>SBSehati - Penjualan</title>
</svelte:head>

<div>
    <h1 class="title">Penjualan</h1>

    <a class="button is-link" href="#/order">Order</a>

    <table class="table mt-3" id="penjualan">
        <thead>
            <tr>
                <th>No</th>
                <th>Tanggal</th>
                <th>Sales</th>
                <th>Status</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            {#if penjualan}
                {#each penjualan as p, i}
                <tr>
                    <td>{i + 1}</td>
                    <td>{ moment(p.tgl).format('D MMMM YYYY') }</td>
                    <td>{$user.username}</td>
                    <td>
                        {#if p.accepted}
                            <span class="tag is-primary">Diterima</span>
                        {:else}
                            <span class="tag is-light">Pending</span>
                        {/if}
                    </td>
                    <td>
                        <a class="is-link">detail</a>
                    </td>
                </tr>
                {/each}
            {:else}
            <tr>
                <td colspan="5">Tidak Ada Order</td>
            </tr>
            {/if}
        </tbody>
    </table>
    <hr>
</div>
