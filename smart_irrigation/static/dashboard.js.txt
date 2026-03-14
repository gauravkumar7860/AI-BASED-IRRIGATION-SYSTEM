let chart;
const API = '/api';

// Update time
function updateTime() {
    document.getElementById('current-time').textContent = new Date().toLocaleString();
}
setInterval(updateTime, 1000);
updateTime();

// Initialize chart
async function initChart() {
    const ctx = document.getElementById('chart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Soil Moisture %',
                    data: [],
                    borderColor: '#00b894',
                    backgroundColor: 'rgba(0, 184, 148, 0.2)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Temperature °C',
                    data: [],
                    borderColor: '#fdcb6e',
                    backgroundColor: 'rgba(253, 203, 110, 0.2)',
                    tension: 0.4,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { position: 'left', beginAtZero: true },
                y1: { position: 'right', grid: { drawOnChartArea: false } }
            }
        }
    });
}

// Update all data
async function updateDashboard() {
    try {
        const res = await fetch(API + '/data');
        const data = await res.json();

        // Sensors
        document.getElementById('moisture-val').textContent = data.soil_moisture.toFixed(1) + '%';
        document.getElementById('moisture-bar').style.width = data.soil_moisture + '%';
        const moistureStatus = data.soil_moisture > 30 ? 'good' : 'low';
        document.getElementById('moisture-status').textContent = data.soil_moisture > 30 ? 'Optimal' : 'Low Water';
        document.getElementById('moisture-status').className = `status ${moistureStatus}`;

        document.getElementById('temp-val').textContent = data.temperature.toFixed(1) + '°C';
        document.getElementById('temp-bar').style.width = Math.min(100, data.temperature * 2.5) + '%';

        document.getElementById('humid-val').textContent = data.humidity + '%';
        document.getElementById('humid-bar').style.width = data.humidity + '%';

        // Pump
        const pumpCircle = document.getElementById('pump-circle');
        pumpCircle.className = data.pump_status ? 'pump-circle on' : 'pump-circle off';
        document.getElementById('pump-text').textContent = data.pump_status ? 'ON' : 'OFF';
        
        if (data.last_watered) {
            document.getElementById('last-water').textContent = `Last watered: ${data.last_watered}`;
        }

        // Weather
        document.getElementById('rain-val').textContent = data.rain_forecast + '%';

        // Chart
        const histRes = await fetch(API + '/history');
        const history = await histRes.json();
        chart.data.labels = history.map(h => h.time);
        chart.data.datasets[0].data = history.map(h => h.moisture);
        chart.data.datasets[1].data = history.map(h => h.temp);
        chart.update('none');

    } catch (e) {
        console.error('Update failed:', e);
    }
}

// Pump controls
async function pumpOn() {
    await fetch(API + '/pump', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({status: true})
    });
    updateDashboard();
}

async function pumpOff() {
    await fetch(API + '/pump', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({status: false})
    });
    updateDashboard();
}

// Auto-update every 3 seconds
initChart();
updateDashboard();
setInterval(updateDashboard, 3000);