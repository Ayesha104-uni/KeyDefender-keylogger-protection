 document.addEventListener('DOMContentLoaded', function() {
        // Track visit
        fetch('/api/track-visit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        // Update visitor count
        function updateStats() {
            // Total visitors
            fetch('/api/visitor-stats/')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('visitorCount').textContent = 
                        data.total_visitors.toLocaleString();
                });

            // Chart data
            fetch('/api/recent-visits/')
                .then(response => response.json())
                .then(data => {
                    const ctx = document.getElementById('visitorChart').getContext('2d');
                    
                    // Destroy existing chart if exists
                    if(window.visitorChart) window.visitorChart.destroy();
                    
                    window.visitorChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: data.dates,
                            datasets: [{
                                label: 'Daily Visitors',
                                data: data.counts,
                                borderColor: '#2A2A72',
                                borderWidth: 2,
                                tension: 0.4,
                                fill: true,
                                backgroundColor: 'rgba(42, 42, 114, 0.1)'
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'bottom'
                                }
                            },
                            scales: {
                                x: {
                                    grid: { display: false },
                                    ticks: { maxTicksLimit: 10 }
                                },
                                y: {
                                    beginAtZero: true,
                                    grid: { color: '#f5f5f5' }
                                }
                            }
                        }
                    });
                });
        }

        // Initial load
        updateStats();
        // Update every 30 seconds
        setInterval(updateStats, 30000);
    });
    
document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('startScan');
    const progressBar = document.getElementById('progressBar');
    const resultsDiv = document.getElementById('scanResults');

    if (!startButton || !progressBar || !resultsDiv) {
        console.error('Critical elements missing!');
        return;
    }

    startButton.addEventListener('click', async () => {
        try {
            startButton.disabled = true;
            progressBar.style.width = '30%';
            resultsDiv.innerHTML = '<div class="scanning">Scanning system processes...</div>';

            // API call
            const response = await fetch('/api/scan-keyloggers/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const data = await response.json();
            progressBar.style.width = '100%';

            // Update results display
            let resultsHtml = '<div class="results">';
            if(data.files_detected.length > 0 || data.processes_detected.length > 0) {
                resultsHtml += `
                    <h3>Potential Threats Detected:</h3>
                    <div class="threat-list">
                        ${data.files_detected.map(f => `
                            <p><i class="fas fa-file-exclamation"></i> ${f} - REMOVED</p>
                        `).join('')}
                        ${data.processes_detected.map(p => `
                            <p><i class="fas fa-virus"></i> ${p} - TERMINATED</p>
                        `).join('')}
                    </div>
                `;
            } else {
                resultsHtml += `
                    <div class="clean-system">
                        <i class="fas fa-check-circle"></i>
                        <h3>No threats detected!</h3>
                        <p>Your system appears to be secure</p>
                    </div>
                `;
            }
            resultsDiv.innerHTML = resultsHtml;

        } catch (error) {
            console.error('Scan failed:', error);
            resultsDiv.innerHTML = `
                <div class="alert alert-danger">
                    Scan failed: ${error.message}
                </div>
            `;
        } finally {
            setTimeout(() => {
                progressBar.style.width = '0%';
                startButton.disabled = false;
            }, 2000);
        }
    });
});

