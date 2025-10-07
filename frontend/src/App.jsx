import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

const hints = {
  scenario_name: '(e.g., Q4 Pilot)',
  monthly_invoice_volume: '(e.g., 2000)',
  num_ap_staff: '(e.g., 3)',
  avg_hours_per_invoice: '(e.g., 0.17 for 10 mins)',
  hourly_wage: '(e.g., 30)',
  error_rate_manual: '(e.g., 0.5 for 0.5%)',
  error_cost: '(e.g., 100)',
  time_horizon_months: '(e.g., 36)',
  one_time_implementation_cost: '(e.g., 50000)',
};

function App() {
  const [formData, setFormData] = useState({
    scenario_name: '',
    monthly_invoice_volume: '',
    num_ap_staff: '',
    avg_hours_per_invoice: '',
    hourly_wage: '',
    error_rate_manual: '',
    error_cost: '',
    time_horizon_months: '',
    one_time_implementation_cost: '',
  });
  
  // NEW: State for the checkbox, starts unchecked (false)
  const [includeCost, setIncludeCost] = useState(false);
  
  const [results, setResults] = useState(null);
  const [scenarios, setScenarios] = useState([]);

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const getNumericFormData = () => {
    const numericData = {};
    for (const key in formData) {
      if (key !== 'scenario_name') {
        numericData[key] = parseFloat(formData[key]) || 0;
      } else {
        numericData[key] = formData[key];
      }
    }
    // NEW: If the checkbox is unchecked, force the cost to 0
    if (!includeCost) {
        numericData.one_time_implementation_cost = 0;
    }
    return numericData;
  };

  const handleCalculate = async (e) => {
    e.preventDefault();
    const apiData = getNumericFormData();
    try {
      const response = await axios.post(`${API_URL}/simulate`, apiData);
      setResults(response.data);
    } catch (error) {
      console.error('Error calculating ROI:', error);
      alert('Failed to calculate ROI. Is the backend server running?');
    }
  };
  
  const handleSave = async () => {
    const apiData = getNumericFormData();
    if (!apiData.scenario_name) {
        alert("Please provide a name for the scenario before saving.");
        return;
    }
    try {
      await axios.post(`${API_URL}/scenarios`, apiData);
      alert('Scenario Saved!');
      loadScenarios();
    } catch (error) {
      console.error('Error saving scenario:', error);
    }
  };

  const loadScenarios = async () => {
    try {
      const response = await axios.get(`${API_URL}/scenarios`);
      setScenarios(response.data);
    } catch (error) {
      console.error('Error loading scenarios:', error);
    }
  };

  useEffect(() => {
    loadScenarios();
  }, []);

  return (
    <div className="container">
      <h1>Invoicing ROI Simulator (React)</h1>

      <form onSubmit={handleCalculate}>
        <h2>Your Current Process & Investment</h2>
        <div className="form-grid">
          {/* Loop through all form data EXCEPT the implementation cost */}
          {Object.keys(formData).filter(key => key !== 'one_time_implementation_cost').map((key) => (
            <div key={key}>
              <label htmlFor={key}>
                {key.replace(/_/g, ' ')}
                <span className="format-hint">{hints[key]}</span>
              </label>
              <input
                type={key === 'scenario_name' ? 'text' : 'number'}
                id={key}
                step="any"
                value={formData[key]}
                onChange={handleInputChange}
                placeholder={hints[key]}
                required
              />
            </div>
          ))}
        </div>
        
        {/* NEW: Checkbox to control the implementation cost field */}
        <div className="checkbox-container">
            <input 
                type="checkbox" 
                id="includeCost"
                checked={includeCost}
                onChange={(e) => setIncludeCost(e.target.checked)}
            />
            <label htmlFor="includeCost">Include One-Time Implementation Cost?</label>
        </div>

        {/* NEW: Conditionally show the implementation cost input */}
        {includeCost && (
            <div className="form-grid" style={{marginTop: '1.5rem'}}>
                 <div>
                    <label htmlFor="one_time_implementation_cost">
                        One Time Implementation Cost
                        <span className="format-hint">{hints['one_time_implementation_cost']}</span>
                    </label>
                    <input
                        type="number"
                        id="one_time_implementation_cost"
                        step="any"
                        value={formData.one_time_implementation_cost}
                        onChange={handleInputChange}
                        placeholder={hints['one_time_implementation_cost']}
                        required
                    />
                </div>
            </div>
        )}

        <div style={{marginTop: '1.5rem'}}>
            <button type="submit">Calculate ROI</button>
            <button type="button" onClick={handleSave}>Save Scenario</button>
        </div>
      </form>
      
      {results && (
        <div className="results-grid">
          <div className="result-box">
            <h3>Monthly Savings</h3>
            <p>${results.monthly_savings.toLocaleString()}</p>
          </div>
          <div className="result-box">
            <h3>Payback Period</h3>
            <p>{results.payback_months} mo</p>
          </div>
          <div className="result-box">
            <h3>Total ROI</h3>
            <p>{results.roi_percentage}%</p>
          </div>
        </div>
      )}

      <div className="scenarios-section">
        <h2>Saved Scenarios</h2>
        <ul>
          {scenarios.map((scenario) => (
            <li key={scenario.id}>{scenario.scenario_name}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;