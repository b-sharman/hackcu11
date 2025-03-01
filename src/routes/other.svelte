<script lang="ts">
    import '../fonts.css';
</script>

<style>
:global(body) {
    font-family: 'Roboto', sans-serif;
}

.title {
    font-size: 2em;
    font-weight: bold;
    margin: 1em 0;
    text-align: center;
}

.textbox {
    width: 300px;
    border-radius: 4px;
    border-color: black;
    border-width: 1px;
    height: 30px;
    margin-left: 400px;
}

.magnifier {
    background-color: rgb(74, 68, 190);
    border: none;
    color: white;
    padding-left: 15px;
    padding-right: 15px;
    padding-top: 8px;
    padding-bottom: 8px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin-left: 10px;
    cursor: pointer;
    border-radius: 4px;
    cursor: pointer;
}
</style>

<p class="title">Home</p>
<input class="textbox" type="text">
<button class="magnifier">Search</button>