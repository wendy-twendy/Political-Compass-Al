function displayResults(result) {
    console.log('Displaying results:', result);
    window.quizResult = result; // Store the result globally
    const plotlyChart = document.getElementById('plotly-chart');
    const resultDescription = document.getElementById('result-description');
    const averageScoresChart = document.getElementById('average-scores-chart');
    const famousFiguresChart = document.getElementById('famous-figures-chart');

    if (!plotlyChart || !averageScoresChart || !famousFiguresChart) {
        console.error('One or more chart containers not found');
        return;
    }

    try {
        // Parse the plot JSON and render it using Plotly
        const plotData = JSON.parse(result.plot_json);
        Plotly.newPlot('plotly-chart', plotData.data, plotData.layout, {
            displayModeBar: false,
            responsive: true,
            staticPlot: true
        });

        // Render Average Scores plot
        if (result.average_scores_plot) {
            const averageScoresData = JSON.parse(result.average_scores_plot);
            Plotly.newPlot('average-scores-chart', averageScoresData.data, averageScoresData.layout, {
                displayModeBar: false,
                responsive: true,
                staticPlot: true
            });
        }

        // Render Famous Figures plot
        if (result.famous_figures_plot) {
            const famousFiguresData = JSON.parse(result.famous_figures_plot);
            Plotly.newPlot('famous-figures-chart', famousFiguresData.data, famousFiguresData.layout, {
                displayModeBar: false,
                responsive: true,
                staticPlot: true
            });
        }

        // Display the user's score description
        let economicLabel = result.economic < 0 ? 'Left' : 'Right';
        let libertarianAuthoritarianLabel = result.libertarian_authoritarian < 0 ? 'Libertarian' : 'Authoritarian';
        resultDescription.innerHTML = `
            <p class="text-lg font-semibold mb-2">Your political compass position:</p>
            <p>Economic: ${result.economic.toFixed(2)} (${economicLabel})</p>
            <p>Social: ${result.libertarian_authoritarian.toFixed(2)} (${libertarianAuthoritarianLabel})</p>
        `;

        const quadrantName = document.getElementById('quadrant-name');
        const quadrantDescription = document.getElementById('quadrant-description');
        
        if (quadrantName && quadrantDescription) {
            quadrantName.textContent = result.quadrant;
            quadrantDescription.textContent = result.explanation;
        }

    } catch (error) {
        console.error('Error parsing JSON or displaying results:', error);
        alert('An error occurred while displaying the results. Please try again.');
    }
}

function shareOnTwitter() {
    try {
        const economic = window.quizResult.economic.toFixed(2);
        const libertarianAuthoritarian = window.quizResult.libertarian_authoritarian.toFixed(2);
        const answers = encodeURIComponent(window.userAnswers.join(','));
        const url = encodeURIComponent(`${window.location.origin}/shared_result?economic=${economic}&libertarian_authoritarian=${libertarianAuthoritarian}&answers=${answers}`);
        const text = encodeURIComponent("Check out my Political Compass Quiz result!");
        const shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${text}`;
        window.open(shareUrl, '_blank');
    } catch (error) {
        console.error('Error sharing on Twitter:', error);
        alert('An error occurred while sharing on Twitter. Please try again.');
    }
}

function shareOnLinkedIn() {
    try {
        const economic = window.quizResult.economic.toFixed(2);
        const libertarianAuthoritarian = window.quizResult.libertarian_authoritarian.toFixed(2);
        const answers = encodeURIComponent(window.userAnswers.join(','));
        const url = encodeURIComponent(`${window.location.origin}/shared_result?economic=${economic}&libertarian_authoritarian=${libertarianAuthoritarian}&answers=${answers}`);
        const shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
        window.open(shareUrl, '_blank');
    } catch (error) {
        console.error('Error sharing on LinkedIn:', error);
        alert('An error occurred while sharing on LinkedIn. Please try again.');
    }
}
