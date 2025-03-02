import type { PageLoad } from './$types';
import { VITE_API_KEY } from '$env/static/private';

export const load: PageLoad = async ({ fetch }) => {
  const data = await (await fetch('co_members.json')).json(); // prefetched members, since I don't think the members of Congress will change during the hackathon

  const legislation = new Set();
  for (const member of data.members) {
    const sponsored_leg = await (await fetch(
      `https://api.congress.gov/v3/member/${member.bioguideId}/sponsored-legislation?api_key=${VITE_API_KEY}`
    )).json();
    legislation.add(sponsored_leg);
    console.log(sponsored_leg);
    const cosponsored_leg = await (await fetch(
      `https://api.congress.gov/v3/member/${member.bioguideId}/cosponsored-legislation?api_key=${VITE_API_KEY}`
    )).json();
    legislation.add(cosponsored_leg);
  }

  console.log(legislation);

  return {
    members: data.members,
    legislation,
  };
};



