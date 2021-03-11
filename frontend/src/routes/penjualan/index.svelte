<script>
    import { onMount } from 'svelte';

    // import Modal from '$components/Modal.svelte'

    let penjualan;
    let pelanggan = {};
    let sales = {};
    let barang = [];
    let nbarang = 1;
    let formOrder = {
        tgl: '2021-01-01',
        pelanggan_id: '',
    };

    const addNBarang = () => {
		nbarang += 1;
	};

    function getSalesId() {
        let sid = 0;
        Object.values(sales).forEach(s => {
            console.log(s.id);
            sid = s.id;
        });
        return sid;
    }

    function addOrder() {
        let date = new Date(formOrder['tgl']);
        // let formData = new FormData();
        // formData.append('sales_id', username);
        // formData.append('pelanggan_id', username);
        // formData.append('tgl', username);
        let order = {
            sales_id: getSalesId(),
            pelanggan_id: parseInt(document.getElementById(`pelanggan`).value),
            tgl: date.toISOString()
        }

        let barangs = [];
        let i = 0;
        while (true) {
            let barang_id = document.getElementById(`barang-${i}`);
            let qty = document.getElementById(`qty-${i}`);

            if (!barang_id) {
                break;
            }

            barangs.push({
                barang_id: parseInt(barang_id.value),
                qty: parseInt(qty.value)
            });
            i += 1;
        }
        order['item_penjualan'] = barangs;

        console.log(order);
        postJsonData(backend + "/api/penjualan", order)
            .then(data => {
                console.log(data);
                if (data.id) {
                    alert("Success");
                    penjualan.push(data);
                    penjualan = penjualan;

                    toggleModal('penjualanForm');
                } else {
                    alert(data.detail);
                }
            })
            .catch(error => console.log(error));
     }

    onMount(() => {
        getJsonData(backend + "/info")
            .then(data => {
                console.log(data);
                if (data.username) {
                    if (data.role != "sales") {
                        console.log("You're not Sales");
                        window.location.href = '/sdm';
                    }
                } else {
                    alert(data.detail);
                }
            })
            .catch(error => console.log(error));

        getJsonData(backend + "/api/penjualan")
            .then(data => {
                // console.log(data);
                if (data) {
                    penjualan = data;
                } else {
                    alert(data.detail);
                }
            })
            .catch(error => console.log(error));

        getJsonData(backend + "/api/pelanggan")
            .then(data => {
                // console.log(data);
                if (data) {
                    data.forEach(function(d) {
                        pelanggan[d.id] = d;
                        // console.log(Object.values(pelanggan));
                    });
                    // console.log(pelanggan);
                } else {
                    alert(data.detail);
                }
            })
            .catch(error => console.log(error));

        getJsonData(backend + "/api/sales")
            .then(data => {
                // console.log(data);
                if (data) {
                    data.forEach(function(d) {
                        sales[d.id] = d;
                    });
                } else {
                    alert(data.detail);
                }
            })
            .catch(error => console.log(error));

        getJsonData(backend + "/api/barang")
            .then(data => {
                // console.log(data);
                if (data) {
                    barang = data;
                } else {
                    alert(data.detail);
                }
            })
            .catch(error => console.log(error));
    });

    let nodeRef;
</script>

<div class="container">
    <h1 class="title">Penjualan</h1>

    <button class="button is-link" onclick="toggleModal('penjualanForm')">Order</button>

    <div class="modal" id="penjualanForm">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">Order</p>
                <button class="delete" aria-label="close" onclick="toggleModal('penjualanForm')"></button>
            </header>
            <section class="modal-card-body">
                <div class="pt-2 pb-2">
                    <label class="label" for="expired_date">Tanggal</label>
                    <input type="date" class="input is-link date-picker" name="expired_date" bind:value={formOrder.tgl}>
                </div>
                <div class="is-four-fifths pt-2 pb-2" style="z-index: 10000">
                  <label class="label" for="pelanggan">Pelanggan</label>
                  <div class="select is-link">
                    <select id="pelanggan" name="pelanggan" class="is-link">
                      {#each Object.values(pelanggan) as p}
                        <option value="{p.id}">{p.nama}</option>
                      {/each}
                    </select>
                  </div>
                </div>
                {#each range(0, nbarang, 1) as i}
                    <div class="columns pt-2 pb-2">
                        <div class="column is-four-fifth" style="z-index: 10000">
                          <label class="label" for="barang-{i}">Barang</label>
                          <div class="select is-link">
                            <select id="barang-{i}" name="barang-{i}" class="is-link">
                              {#each Object.values(barang) as b}
                                <option value="{b.id}">{b.obat.nama} ({b.batch})</option>
                              {/each}
                            </select>
                          </div>
                        </div>
                        <div class="column">
                            <label class="label" for="expired_date">Quantity</label>
                            <input type="number" class="input is-link" id="qty-{i}" name="qyt-{i}" step="1">
                        </div>
                    </div>
                {/each}
                <div>
                    <button class="button is-link" on:click={addNBarang}>+</button>
                </div>
            </section>
            <footer class="modal-card-foot">
                <button class="button is-primary" on:click={addOrder}>Kirim</button>
                <button class="button" onclick="toggleModal('penjualanForm')">Cancel</button>
            </footer>
        </div>
    </div>

    <table class="table is-bordered mt-3">
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
                        {getAttr(pelanggan, p.pelanggan_id, "nama")}
                    </td>
                    <td>
                        {getAttr(sales, p.sales_id, "nama")}
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
