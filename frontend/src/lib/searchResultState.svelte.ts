interface searchResultStateInterface {
    results: Array<Number>,
}

export const results: searchResultStateInterface = $state({
    results: [],
});
