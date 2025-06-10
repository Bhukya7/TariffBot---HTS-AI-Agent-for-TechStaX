# append_donkeys.py
import pandas as pd
from config import HTS_CSV_PATH

# Load existing CSV
df = pd.read_csv(HTS_CSV_PATH)

# Create new entry
new_entry = {
    'HTS Number': '0101.30.00.00',
    'Indent': 0,
    'Description': 'Donkeys',
    'Unit of Quantity': 'Number',
    'General Rate of Duty': 0,
    'Special Rate of Duty': 'Free',
    'Column 2 Rate of Duty': 0,
    'Quota Quantity': None,
    'Additional Duties': None
}

# Append entry
new_df = pd.DataFrame([new_entry])
df = pd.concat([df, new_df], ignore_index=True)

# Save updated CSV
df.to_csv(HTS_CSV_PATH, index=False)
print("Appended Donkeys entry to CSV")