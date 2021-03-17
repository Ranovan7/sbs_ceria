<script>
	import { afterUpdate } from 'svelte';
	import { goto, stores } from '@sapper/app';
	import Nav from '../components/Nav.svelte';

    const { session, page } = stores();
    const { user, BACKEND } = $session;
	const permissions = {
		admin: ["/sdm"],
		sales: ["/penjualan"],
	}

	afterUpdate(() => {
		console.log($page.path);
		if ($page.path != "/login") {
      		checkPage($session.user);
		}
	})

	function getAuthToken() {
	    let name = "auth_token=";
	    let decodedCookie = decodeURIComponent(document.cookie);
	    let ca = decodedCookie.split(';');
	    for(let i = 0; i <ca.length; i++) {
	        let c = ca[i];
	        while (c.charAt(0) == ' ') {
	            c = c.substring(1);
	        }
	        if (c.indexOf(name) == 0) {
	            return c.substring(name.length, c.length);
	        }
	    }
	    return "";
	}

	function checkPermissions(role) {
		console.log(typeof(permissions[role]));
		return permissions[role].includes($page.path);
	}

	function checkRolePage(user) {
		if (user.role == 'sales') {
			goto(`/penjualan`);
		} else {
			goto(`/sdm`);
		}
	}

	function checkPage(user) {
		if (!user) {
			console.log("User Not Found");
			getUser().catch(error => console.log(error));
		} else {
			console.log("Already Logged In");
			if (!checkPermissions(user.role)) {
				checkRolePage(user);
			}
		}
	}

	async function getUser() {
		const response = await fetch(BACKEND + "/info", {
	        method: 'GET',
	        headers: {
	          'Content-Type': 'application/json',
	          'Authorization': `Bearer ${getAuthToken()}`,
	        },
	    });

		const parsed = await response.json();

		if (parsed.username) {
			console.log("Fetching User Data");
			$session.user = parsed;
			console.log($session.user);
			checkRolePage($session.user);
		} else {
			let message = "Mohon Login untuk mengakses Aplikasi";
			goto(`/login?message=${message}`);
		}
	}

	export let segment;
</script>

<style>

</style>

{#if !(segment === 'login')}
  <Nav {segment}/>
{/if}

<main>
	<slot></slot>
</main>
