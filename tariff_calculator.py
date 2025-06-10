# tariff_calculator.py
from database import query_by_hts_code

def calculate_duties(hts_code, product_cost, freight=None, insurance=None, unit_weight=None, quantity=None):
    """Calculate duties based on HTS code and product details."""
    df = query_by_hts_code(hts_code)
    if df.empty:
        return {"error": f"HTS code {hts_code} not found."}
    
    duty_rate = df['General_Rate_of_Duty'].iloc[0] if 'General_Rate_of_Duty' in df.columns else 0
    try:
        duty_rate = float(duty_rate.replace('%', '')) / 100 if isinstance(duty_rate, str) else duty_rate
    except:
        duty_rate = 0
    
    freight = freight or 0
    insurance = insurance or 0
    cif_value = product_cost + freight + insurance
    duty_amount = cif_value * duty_rate
    
    result = {
        "HTS_Code": hts_code,
        "CIF_Value": cif_value,
        "Duty_Rate": duty_rate,
        "Duty_Amount": duty_amount
    }
    if unit_weight and quantity:
        result["Total_Weight"] = unit_weight * quantity
    return result