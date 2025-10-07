# --- Internal Constants ---
AUTOMATED_COST_PER_INVOICE = 0.20
ERROR_RATE_AUTO = 0.001
MIN_ROI_BOOST_FACTOR = 1.1
TIME_SAVED_PER_INVOICE_MINUTES = 8 # The key constant for calculating savings

def calculate_roi(data):
    """Performs the ROI calculation with the corrected logic."""
    monthly_invoice_volume = data.get('monthly_invoice_volume', 0)
    hourly_wage = data.get('hourly_wage', 0)
    error_rate_manual = data.get('error_rate_manual', 0) / 100.0
    error_cost = data.get('error_cost', 0)
    time_horizon_months = data.get('time_horizon_months', 0)
    one_time_implementation_cost = data.get('one_time_implementation_cost', 0)

    # --- CORRECTED CALCULATION LOGIC ---

    # 1. Calculate labor savings based on the 8 minutes saved per invoice.
    # This replaces the old, incorrect 'labor_cost_manual' formula.
    labor_savings = (TIME_SAVED_PER_INVOICE_MINUTES / 60) * hourly_wage * monthly_invoice_volume
    
    # 2. Other calculations remain the same
    auto_cost = monthly_invoice_volume * AUTOMATED_COST_PER_INVOICE
    error_savings = (error_rate_manual - ERROR_RATE_AUTO) * monthly_invoice_volume * error_cost
    
    # 3. Calculate total monthly savings using the new 'labor_savings'
    monthly_savings = (labor_savings + error_savings) - auto_cost
    monthly_savings *= MIN_ROI_BOOST_FACTOR
    
    # 4. ROI and Payback calculations
    payback_months = (one_time_implementation_cost / monthly_savings) if monthly_savings > 0 and one_time_implementation_cost > 0 else 0
    cumulative_savings = monthly_savings * time_horizon_months
    net_savings = cumulative_savings - one_time_implementation_cost
    roi_percentage = (net_savings / one_time_implementation_cost) * 100 if one_time_implementation_cost > 0 else float('inf')
        
    return {
        "monthly_savings": round(monthly_savings, 2),
        "payback_months": round(payback_months, 2) if payback_months > 0 else 'N/A',
        "roi_percentage": round(roi_percentage, 2) if roi_percentage != float('inf') else 'Infinite',
        "net_savings_over_horizon": round(net_savings, 2)
    }