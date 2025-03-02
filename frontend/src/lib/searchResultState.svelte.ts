interface searchResultStateInterface {
    results: Array<Number>,
    index: Number,
}

export const results: searchResultStateInterface = $state({
    results: [],
    index: 0,
});
