import type { PageLoad } from './$types';
import { VITE_API_KEY } from '$env/static/private';

export const load: PageLoad = async () => {
  const res = await fetch(
    `https://api.congress.gov/v3/bill?limit=5&api_key=${VITE_API_KEY}`
  );
  const json = await res.json();

  return json;
};
