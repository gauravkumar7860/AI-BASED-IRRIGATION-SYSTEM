from flask import Flask, render_template, jsonify, request
import random
from datetime import datetime

app = Flask(__name__)

# Simulated sensor data
class SensorData:
    def __init__(self):
        self.data = {
            'soil_moisture': 45,
            'temperature': 28.5,
            'humidity': 65,
            'pump_status': False,
            'rain_forecast': 10,
            'last_watered': None
        }
        self.history = []

    def update_data(self):
        # Generate realistic sensor values
        self.data['soil_moisture'] = round(random.uniform(20, 60), 1)
        self.data['temperature'] = round(random.uniform(20, 38), 1)
        self.data['humidity'] = round(random.uniform(40, 90), 1)
        self.data['rain_forecast'] = random.randint(0, 100)

        # Add to history
        self.history.append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'moisture': self.data['soil_moisture'],
            'temp': self.data['temperature']
        })

        if len(self.history) > 30:
            self.history.pop(0)

        return self.data.copy()

    def toggle_pump(self, status):
        self.data['pump_status'] = status
        if status:
            self.data['last_watered'] = datetime.now().strftime('%H:%M:%S')
        return self.data.copy()


# Global sensor instance
sensor = SensorData()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/data')
def get_data():
    return jsonify(sensor.update_data())


@app.route('/api/history')
def get_history():
    return jsonify(sensor.history)


@app.route('/api/pump', methods=['POST'])
def pump_control():
    status = request.json.get('status', False)
    data = sensor.toggle_pump(status)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
