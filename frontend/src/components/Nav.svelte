<script>
    import { user } from '../stores';
    import { replace } from 'svelte-spa-router';

    function logout() {
        document.cookie = "auth_token= ; expires = Thu, 01 Jan 1970 00:00:00 GMT";
		console.log("Logout");
        replace("/login");
    }
</script>

<style>

</style>

<nav class="navbar" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="https://bulma.io">
      <img src="https://bulma.io/images/bulma-logo.png" width="112" height="28">
    </a>

    <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample" onclick="document.querySelector('.navbar-menu').classList.toggle('is-active');">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div id="navbarMain" class="navbar-menu">
     <div class="navbar-start">
       <a class="navbar-item" href="#/">Dashboard</a>
       <a class="navbar-item" href="#/sdm">
         SDM
       </a>
       <div class="navbar-item has-dropdown is-hoverable">
         <a class="navbar-link">Transaksi</a>
         <div class="navbar-dropdown">
           <a class="navbar-item" href="#/penjualan">Penjualan</a>
           <a class="navbar-item">Pembelian</a>
         </div>
       </div>
       <div class="navbar-item has-dropdown is-hoverable">
         <a class="navbar-link">Keuangan</a>
         <div class="navbar-dropdown">
           <a class="navbar-item">Tagihan</a>
           <a class="navbar-item">Hutang</a>
         </div>
       </div>
       <div class="navbar-item has-dropdown is-hoverable">
         <a class="navbar-link">Produk</a>
         <div class="navbar-dropdown">
           <a class="navbar-item">Stok</a>
           <a class="navbar-item">Statistik</a>
         </div>
       </div>
     </div>

     <div class="navbar-end">
        <div class="navbar-item">
            <p>{$user.username} ({$user.role})</p>
        </div>
       <div class="navbar-item">
         <div class="buttons">
            {#if !$user}
                <a class="button is-link is-light" href="#/login">
                Login
                </a>
            {:else}
                <button class="button is-secondary is-light" on:click="{logout}">
                Logout
                </button>
            {/if}
         </div>
       </div>
     </div>
  </div>

</nav>
