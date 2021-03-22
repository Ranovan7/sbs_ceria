<script>
    import { onMount } from 'svelte';
    import { replace } from 'svelte-spa-router';
    import moment from 'moment';

    import 'moment/locale/id';
    moment.locale('id');

    import { user, backend } from '../stores';
    import { getJsonData } from '../utils';

    let pelanggan = [];
    let barang = [];
    let item_count = 1;

    onMount(async () => {
        if ($user.role != 'sales') {
            console.log("not Sales");
            replace("/");
        }

        // fetch pelanggan
        getJsonData($backend + "/api/pelanggan")
            .then(results => {
                if (!results.detail) {
                    pelanggan = results;
                    console.log(`${pelanggan.length} Pelanggan`);
                } else {
                    alert(results.detail);
                }
            }).catch(err => {
                console.error('Error:', err);
            });

        // fetch barang
        getJsonData($backend + "/api/barang")
            .then(results => {
                if (!results.detail) {
                    barang = results;
                    console.log(`${barang.length} Barang`);
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
    <title>SBSehati - Order</title>
</svelte:head>

<div>
    <h1 class="title">Order</h1>
    <div class="columns">
        <div class="column is-three-fifths">
            <div class="columns">
                <div class="column is-half">
                    <div class="field">
                        <label class="label">Tanggal</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="Text input">
                        </div>
                    </div>
                </div>
                <div class="column is-half">
                    <div class="field">
                        <label class="label">Pelanggan</label>
                        <div class="control">
                            <div class="select">
                                <select name="pelanggan_id">
                                    {#each pelanggan as p, i}
                                    <option value="{p.id}">{p.nama}</option>
                                    {/each}
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <p class="card-header-title">
                      Item
                    </p>
                </div>
                <div class="card-content">
                    {#each Array(item_count) as _, i}
                    <div class="columns">
                        <div class="column is-half">
                            <div class="field">
                                <label class="label">Barang</label>
                                <div class="control">
                                    <div class="select">
                                        <select name="barang_id">
                                            {#each barang as b, i}
                                            <option value="{b.id}">{b.obat.nama} - {b.batch}</option>
                                            {/each}
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="column is-half">
                            <div class="field">
                                <label class="label">Qty</label>
                                <div class="control">
                                    <input class="input" type="number" step="1">
                                </div>
                            </div>
                        </div>
                    </div>
                    {/each}
                    <div align="center">
                        <button class="button is-small is-link" on:click={() => item_count++}>
                            Tambah Item
                        </button>
                    </div>
                </div>
            </div>

            <div class="pt-5">
                <button class="button is-link">
                    Order
                </button>
            </div>
        </div>
    </div>
</div>
