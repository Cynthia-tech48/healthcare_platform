
// ----------- Mood Tracker Chart -----------
document.addEventListener('DOMContentLoaded', () => {
    const moodCanvas = document.getElementById('moodChart');
    if (moodCanvas) {
        fetch('/api/mood_entries')
            .then(res => res.json())
            .then(data => {
                const labels = data.map(e => e.date);
                const values = data.map(e => e.score);
                const ctx = moodCanvas.getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Mood score (last entries)',
                            data: values,
                            fill: true,
                            tension: 0.3,
                            backgroundColor: 'rgba(34,197,94,0.1)',
                            borderColor: '#22c55e',
                            pointRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                min: 0,
                                max: 10
                            }
                        }
                    }
                });
            })
            .catch(err => console.error('Error fetching mood data:', err));
    }
});

// ----------- Toggle Goal Completion -----------
document.querySelectorAll('.goal-complete-btn').forEach(btn => {
    btn.addEventListener('click', e => {
        const form = btn.closest('form');
        if (form) form.submit();
    });
});

// ----------- Delete Goal Confirmation -----------
document.querySelectorAll('.goal-delete-btn').forEach(btn => {
    btn.addEventListener('click', e => {
        if (!confirm('Are you sure you want to delete this goal?')) {
            e.preventDefault();
        }
    });
});

// ----------- Simple Form Validation Example -----------
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', e => {
        const requiredFields = form.querySelectorAll('[required]');
        let valid = true;
        requiredFields.forEach(f => {
            if (!f.value.trim()) valid = false;
        });
        if (!valid) {
            e.preventDefault();
            alert('Please fill in all required fields.');
        }
    });
});
