<script lang='ts'>
import type { PageProps } from './$types';

let { members, legislation }: PageProps = $props();

</script>

<h1>Colorado Statistics</h1>

<p>{members.length} Congresspersons</p>
<p>Sponsored {legislation.length} bills</p>
