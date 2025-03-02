import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  return await (await fetch(`http://localhost:5000/member?bioguideId=${params.bioguideId}`)).json();
};
