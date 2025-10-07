from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from fpdf import FPDF
import io

# Import from our other files
from config import Config
from models import db, Scenario
from logic import calculate_roi

# --- App Initialization ---
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

# --- API Endpoints ---
@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    results = calculate_roi(data)
    return jsonify(results)

@app.route('/scenarios', methods=['POST'])
def save_scenario():
    data = request.json
    if not data or not data.get('scenario_name'):
        return jsonify({"error": "scenario_name is required"}), 400
        
    new_scenario = Scenario(**data)
    db.session.add(new_scenario)
    db.session.commit()
    return jsonify({"message": "Scenario saved!", "id": new_scenario.id}), 201

@app.route('/scenarios', methods=['GET'])
def get_all_scenarios():
    scenarios = Scenario.query.order_by(Scenario.id.desc()).all()
    return jsonify([s.to_dict() for s in scenarios])

@app.route('/report/generate', methods=['POST'])
def generate_report():
    data = request.json
    results = data.get('results', {})
    inputs = data.get('inputs', {})
    email = data.get('email')

    if not all([results, inputs, email]):
        return jsonify({"error": "Missing results, inputs, or email"}), 400

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'Invoicing Automation ROI Report', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Monthly Savings: ${results.get('monthly_savings')}", 0, 1)
    pdf.cell(0, 8, f"Payback Period: {results.get('payback_months')} months", 0, 1)
    pdf.cell(0, 8, f"Total ROI: {results.get('roi_percentage')}%", 0, 1)
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    return send_file(
        pdf_buffer, as_attachment=True,
        download_name='ROI_Report.pdf', mimetype='application/pdf'
    )

# --- NEW: Endpoints to Get, Update, and Delete a Single Scenario ---

@app.route('/scenarios/<int:id>', methods=['GET'])
def get_scenario(id):
    """Get a single scenario by its ID."""
    scenario = db.get_or_404(Scenario, id)
    return jsonify(scenario.to_dict())

@app.route('/scenarios/<int:id>', methods=['PUT'])
def update_scenario(id):
    """Update an existing scenario."""
    scenario = db.get_or_404(Scenario, id)
    data = request.json
    
    # Update fields from the request data
    for key, value in data.items():
        setattr(scenario, key, value)
        
    db.session.commit()
    return jsonify(scenario.to_dict())

@app.route('/scenarios/<int:id>', methods=['DELETE'])
def delete_scenario(id):
    """Delete a scenario."""
    scenario = db.get_or_404(Scenario, id)
    db.session.delete(scenario)
    db.session.commit()
    return jsonify({"message": f"Scenario with ID {id} has been deleted."})

# --- Main Execution ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True, port=5000)