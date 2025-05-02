
import pandas as pd

# Load vehicle cost centre reference
vehicle_map = pd.read_csv("vehicle_cost_centres.csv")
vehicle_map['registration'] = vehicle_map['registration'].str.upper().str.strip()

# Normalize entries if needed
vehicle_map['cost_centre'] = vehicle_map['cost_centre'].replace({'Shep': 'Shepp'})

def calculate_cost_by_cost_centre(file_path):
    df = pd.read_excel(file_path, sheet_name='Export')
    df.columns = [col.lower() for col in df.columns]
    df['registration'] = df['registration'].str.upper().str.strip()

    # Fix known registration issues
    df['registration'] = df['registration'].replace({
        'EAS90L': 'ESA90L',
        '1QQ4UK': '2BK7CA',
        '1UG4PJ': 'EOS53F'
    })

    # Merge with vehicle cost centre reference
    merged = df.merge(vehicle_map, on='registration', how='left')

    # Normalize "Shep" to "Shepp"
    merged['cost_centre'] = merged['cost_centre'].replace({'Shep': 'Shepp'})

    # Group by cost centre
    summary = (
        merged.groupby('cost_centre')['totalshellcardamount(incl)']
        .sum()
        .round(2)
        .reset_index()
        .sort_values(by='totalshellcardamount(incl)', ascending=False)
    )

    # Calculate and validate total
    total_actual = merged['totalshellcardamount(incl)'].sum().round(2)
    total_row = pd.DataFrame([{
        'cost_centre': 'Total',
        'totalshellcardamount(incl)': total_actual
    }])

    summary = pd.concat([summary, total_row], ignore_index=True)
    return summary
