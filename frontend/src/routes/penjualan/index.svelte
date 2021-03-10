<script>
    import { onMount } from 'svelte';

    function get_pelanggan(dict, key, attr) {
        if (key in dict) {
            return dict[key][attr];
        } else {
            return "-"
        }
    }

    let penjualan;
    let pelanggan = {};
    let sales = {};

    onMount(() => {
        getJsonData(backend + "/api/penjualan")
            .then(data => {
                console.log(data);
                if (data) {
                    penjualan = data;
                } else {
                    alert(data.detail);
                }
            })
            .catch(error => console.log(error));

        getJsonData(backend + "/api/pelanggan")
            .then(data => {
                console.log(data);
                if (data) {
                    data.forEach(function(d) {
                        pelanggan[d.id] = d;
                    });
                } else {
                    alert(data.detail);
                }
            })
            .catch(error => console.log(error));

        getJsonData(backend + "/api/sales")
            .then(data => {
                console.log(data);
                if (data) {
                    data.forEach(function(d) {
                        sales[d.id] = d;
                    });
                } else {
                    alert(data.detail);
                }
            })
            .catch(error => console.log(error));
    });
</script>

<div class="container">
    <h1 class="title">Penjualan</h1>

    <table class="table is-bordered">
        <thead>
            <tr>
                <th>No</th>
                <th>Tanggal</th>
                <th>Pelanggan</th>
                <th>Sales</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {#if penjualan}
                {#each penjualan as p, i}
                <tr>
                    <td>{i + 1}</td>
                    <td>{p.tgl}</td>
                    <td>
                        {get_pelanggan(pelanggan, p.pelanggan_id, "nama")}
                    </td>
                    <td>
                        {get_pelanggan(sales, p.sales_id, "nama")}
                    </td>
                    <td>
                        {#if p.accepted}
                        diterima
                        {:else}
                        pending
                        {/if}
                    </td>
                </tr>
                {/each}
            {:else}
                <tr>
                    <td colspan="5" align="center">Tidak Ada Penjualan</td>
                </tr>
            {/if}
        </tbody>
    </table>
</div>
