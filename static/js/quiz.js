document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM content loaded');
    const quizForm = document.getElementById('quiz-form');
    const quizContainer = document.getElementById('quiz-container');
    const resultsContainer = document.getElementById('results-container');

    if (!quizForm || !quizContainer || !resultsContainer) {
        console.error('Required elements not found');
        return;
    }

    quizForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Quiz form submitted');
        
        const formData = new FormData(quizForm);
        const answers = [];

        for (let i = 1; i <= 20; i++) {
            const answer = formData.get(`q${i}`);
            if (answer === null) {
                console.warn(`Answer for question ${i} is missing`);
            }
            answers.push(parseInt(answer) || 3); // Default to neutral if parsing fails
        }

        console.log('Answers:', answers);

        try {
            console.log('Sending quiz data to server');
            const response = await fetch('/submit_quiz', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(answers),
            });

            if (response.ok) {
                console.log('Quiz submission successful');
                const result = await response.json();
                console.log('Result:', result);
                displayResults(result);
                quizContainer.classList.add('hidden');
                resultsContainer.classList.remove('hidden');
            } else {
                console.error('Failed to submit quiz:', response.status, response.statusText);
                alert('Failed to submit quiz. Please try again.');
            }
        } catch (error) {
            console.error('Error submitting quiz:', error);
            alert('An error occurred while submitting the quiz. Please try again.');
        }
    });
});
