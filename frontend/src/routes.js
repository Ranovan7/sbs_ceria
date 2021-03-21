import Home from './routes/Home.svelte';
import Login from './routes/Login.svelte';
import Lorem from './routes/Lorem.svelte';
import NotFound from './routes/NotFound.svelte';

export default {
    '/': Home,
    '/login': Login,
    '/lorem/:repeat': Lorem,
    // The catch-all route must always be last
    '*': NotFound
};
