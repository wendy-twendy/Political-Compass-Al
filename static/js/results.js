function displayResults(result) {
    console.log('Displaying results:', result);
    window.quizResult = result; // Store the result globally
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
    
    resultDescription.innerHTML = `
        <h2 class="text-2xl font-bold mb-4">Your Political Compass Result</h2>
        <p class="text-lg mb-2">Economic: <span class="font-semibold">${result.economic.toFixed(2)}</span> (${economicLabel})</p>
        <p class="text-lg mb-4">Social: <span class="font-semibold">${result.libertarian_authoritarian.toFixed(2)}</span> (${libertarianAuthoritarianLabel})</p>
        
        <h3 class="text-xl font-semibold mt-6 mb-2">Your Quadrant: ${result.quadrant}</h3>
        <p class="mb-4">${result.explanation}</p>
        
        <h3 class="text-xl font-semibold mt-6 mb-2">Comparisons</h3>
        <div class="bg-gray-100 p-4 rounded-lg mb-4">
            <h4 class="text-lg font-semibold mb-2">Average User</h4>
            <p>Economic: <span class="font-semibold">${result.average_economic.toFixed(2)}</span></p>
            <p>Social: <span class="font-semibold">${result.average_libertarian_authoritarian.toFixed(2)}</span></p>
        </div>
        
        <h4 class="text-lg font-semibold mb-2">Famous Political Figures</h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            ${Object.entries(result.famous_figures).map(([name, position]) => `
                <div class="bg-white p-4 rounded-lg shadow">
                    <h5 class="font-semibold mb-2">${name}</h5>
                    <p>Economic: <span class="font-semibold">${position[0].toFixed(2)}</span></p>
                    <p>Social: <span class="font-semibold">${position[1].toFixed(2)}</span></p>
                </div>
            `).join('')}
        </div>
    `;

    // Add social media sharing buttons
    const shareContainer = document.createElement('div');
    shareContainer.className = 'flex justify-center mt-8 space-x-4';
    shareContainer.innerHTML = `
        <button onclick="shareOnTwitter()" class="bg-blue-400 text-white px-6 py-2 rounded-full hover:bg-blue-500 transition duration-200">Share on Twitter</button>
        <button onclick="shareOnLinkedIn()" class="bg-blue-800 text-white px-6 py-2 rounded-full hover:bg-blue-900 transition duration-200">Share on LinkedIn</button>
    `;
    resultDescription.parentNode.insertBefore(shareContainer, resultDescription.nextSibling);
}

// ... (rest of the code remains unchanged)
