import Home from './routes/Home.svelte';
import Login from './routes/Login.svelte';
import Sdm from './routes/Sdm.svelte';
import Penjualan from './routes/Penjualan.svelte';
import Lorem from './routes/Lorem.svelte';
import NotFound from './routes/NotFound.svelte';

export default {
    '/': Home,
    '/login': Login,
    '/sdm': Sdm,
    '/penjualan': Penjualan,
    '/lorem/:repeat': Lorem,
    // The catch-all route must always be last
    '*': NotFound
};
