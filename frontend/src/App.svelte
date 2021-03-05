<script>
	import "../node_modules/bulma/css/bulma.min.css";
	import { Router, Route, Link } from "svelte-routing";
	import { link } from "svelte-routing";
	import Home from "./pages/Home.svelte";
	import Login from "./pages/Login.svelte";
	import Sdm from "./pages/Sdm.svelte";
	import Penjualan from "./pages/Penjualan.svelte";
	export let url = "";
</script>

<main>
	<Router url="{url}">
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
	         <a class="navbar-item" href="/" use:link>
			 	Dashboard
			 </a>
			 <a class="navbar-item" href="/sdm" use:link>
	         	SDM
			 </a>
	         <div class="navbar-item has-dropdown is-hoverable">
	           <a class="navbar-link" href="#">Transaksi</a>
	           <div class="navbar-dropdown">
			     <a class="navbar-item" href="/penjualan" use:link>
	             	Penjualan
				 </a>
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
	       </div>

	       <div class="navbar-end">
	         <div class="navbar-item">
	           <div class="buttons">
			  		<a class="navbar-item" href="/login" use:link>
						Login
					</a>
	           </div>
	         </div>
	       </div>
	    </div>

	  </nav>
	  <div>
		<Route path="/login" component="{Login}" />
		<Route path="/sdm" component="{Sdm}" />
		<Route path="/penjualan" component="{Penjualan}" />
	    <Route path="/"><Home /></Route>
	  </div>
	</Router>
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
