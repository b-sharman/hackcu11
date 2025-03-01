import type { PageLoad } from './$types';
import { VITE_API_KEY } from '$env/static/private';

export const load: PageLoad = async ({ fetch }) => {
  const data = await (await fetch('members.json')).json(); // prefetched members, since I don't think the members of Congress will change during the hackathon
  //const bioguideIds = data.members.map(o => o.bioguideId);
  //console.log(bioguideIds);

  return data;
};
