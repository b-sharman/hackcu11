import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
  const titles = (await (await fetch('titles.txt')).text()).split('\n');

  return { titles };
};
