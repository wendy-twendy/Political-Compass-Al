function displayResults(result) {
    console.log('Displaying results:', result);
    const plotlyChart = document.getElementById('plotly-chart');
    const resultDescription = document.getElementById('result-description');
    
    if (!plotlyChart) {
        console.error('Plotly chart container not found');
        return;
    }
    
    // Parse the plot JSON and render it using Plotly
    const plotData = JSON.parse(result.plot_json);
    Plotly.newPlot('plotly-chart', plotData.data, plotData.layout, {
        displayModeBar: false,
        responsive: true,
        staticPlot: true
    });
    
    let economicLabel = result.economic < 0 ? 'Left' : 'Right';
    let libertarianAuthoritarianLabel = result.libertarian_authoritarian < 0 ? 'Libertarian' : 'Authoritarian';
    
    resultDescription.textContent = `Your political compass position is: Economic: ${result.economic.toFixed(2)} (${economicLabel}), Social: ${result.libertarian_authoritarian.toFixed(2)} (${libertarianAuthoritarianLabel})`;
}

function downloadImage() {
    Plotly.toImage('plotly-chart', {format: 'png', width: 800, height: 800}).then(function(dataUrl) {
        var link = document.createElement('a');
        link.download = 'political_compass.png';
        link.href = dataUrl;
        link.click();
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('download-button').addEventListener('click', downloadImage);
});
