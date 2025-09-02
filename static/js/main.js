document.addEventListener('DOMContentLoaded', function() {
    // --- DASHBOARD JS CODE ---

    const moodChartCanvas = document.getElementById('moodChart');
    if (moodChartCanvas) {
        fetch('/api/mood_entries')
            .then(response => response.json())
            .then(data => {
                const dates = data.map(entry => entry.date);
                const scores = data.map(entry => entry.score);

                new Chart(moodChartCanvas, {
                    type: 'line',
                    data: {
                        labels: dates,
                        datasets: [{
                            label: 'Mood Score',
                            data: scores,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 5
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching mood data:', error));
    }

    document.querySelectorAll('.goal-toggle-btn').forEach(button => {
        button.addEventListener('click', function() {
            const goalItem = this.closest('.goal-item');
            goalItem.classList.toggle('completed');
        });
    });

    // --- RECIPES JS CODE ---

    const recipesContainer = document.getElementById('recipes-container');
    if (recipesContainer) {
        function createRecipeCard(recipe) {
            const recipeDiv = document.createElement('div');
            recipeDiv.classList.add('recipe-card');

            if (recipe.picture_url) {
                const img = document.createElement('img');
                img.src = recipe.picture_url;
                img.alt = `Picture of ${recipe.name}`;
                img.classList.add('recipe-image');
                recipeDiv.appendChild(img);
            }

            const title = document.createElement('h3');
            title.textContent = recipe.name;
            recipeDiv.appendChild(title);

            const summary = document.createElement('p');
            summary.textContent = recipe.summary;
            summary.classList.add('recipe-summary');
            recipeDiv.appendChild(summary);

            const steps = document.createElement('p');
            steps.textContent = recipe.steps;
            steps.classList.add('recipe-steps');
            recipeDiv.appendChild(steps);

            recipesContainer.appendChild(recipeDiv);
        }

        fetch('/api/recipes')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                data.forEach(recipe => {
                    createRecipeCard(recipe);
                });
            })
            .catch(error => {
                console.error('Error fetching recipes:', error);
                recipesContainer.textContent = 'Failed to load recipes. Please try again later.';
            });
    }
});