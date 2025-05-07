export default fetchCSV

async function fetchCSV(url) {
    console.log('Fetching csv: ' + url)
    try {
        const response = await fetch(url);
        const data = await response.text();
        // document.getElementById('output').innerText = data;
    } catch (error) {
        console.error('Error fetching CSV:', error);
    }
    return data;
}

// fetchCSV('https://example.com/data.csv');