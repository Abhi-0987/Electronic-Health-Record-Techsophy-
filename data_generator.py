import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta

def generate_synthetic_ehr_data(num_records=1000):
    np.random.seed(int(time.time())) # Seed with current time for variability
    
    # Generate patient demographics
    patient_ids = range(1, num_records + 1)
    ages = np.random.normal(45, 15, num_records).astype(int)
    ages = np.clip(ages, 18, 90)
    
    genders = np.random.choice(['M', 'F'], num_records)
    
    # Generate vital signs with some missing and outlier values
    systolic_bp = np.random.normal(120, 15, num_records)
    diastolic_bp = np.random.normal(80, 10, num_records)
    heart_rate = np.random.normal(75, 12, num_records)
    temperature = np.random.normal(98.6, 0.6, num_records)
    
    # Introduce some missing values
    mask = np.random.random(num_records) < 0.1
    systolic_bp[mask] = np.nan
    mask = np.random.random(num_records) < 0.1
    diastolic_bp[mask] = np.nan
    
    # Generate diagnoses
    diagnoses = np.random.choice(
        ['Hypertension', 'Diabetes', 'Asthma', 'COPD', 'Anxiety'],
        num_records
    )
    
    # Generate medications with some inconsistencies
    medications = [
        np.random.choice(
            ['Lisinopril', 'Metformin', 'Albuterol', 'None'],
            np.random.randint(0, 3)
        ) for _ in range(num_records)
    ]
    
    # Generate timestamps for the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    timestamps = [start_date + timedelta(
        days=np.random.randint(0, 365),
        hours=np.random.randint(0, 24),
        minutes=np.random.randint(0, 60)
    ) for _ in range(num_records)]
    
    # Create DataFrame
    data = pd.DataFrame({
        'patient_id': patient_ids,
        'timestamp': timestamps,
        'age': ages,
        'gender': genders,
        'systolic_bp': systolic_bp,
        'diastolic_bp': diastolic_bp,
        'heart_rate': heart_rate,
        'temperature': temperature,
        'diagnosis': diagnoses,
        'medications': medications
    })
    
    # Introduce some data quality issues
    # 1. Inconsistent date formats
    num_timestamp_issues = np.random.randint(20, 80) # Randomize number of issues
    data.loc[np.random.choice(data.index, num_timestamp_issues, replace=False), 'timestamp'] = \
        data.loc[np.random.choice(data.index, num_timestamp_issues, replace=False), 'timestamp'].apply(
            lambda x: x.strftime('%Y/%m/%d %H:%M:%S')
        )
    
    # 2. Inconsistent gender coding
    num_gender_issues = np.random.randint(10, 50) # Randomize number of issues
    data.loc[np.random.choice(data.index, num_gender_issues, replace=False), 'gender'] = \
        data.loc[np.random.choice(data.index, num_gender_issues, replace=False), 'gender'].replace({'M': 'Male', 'F': 'Female'})
    
    # 3. Some outlier vital signs
    num_outlier_issues = np.random.randint(10, 40) # Randomize number of issues
    outlier_indices = np.random.choice(data.index, num_outlier_issues, replace=False)
    data.loc[outlier_indices, 'systolic_bp'] = np.random.uniform(180, 200, len(outlier_indices))
    data.loc[outlier_indices, 'heart_rate'] = np.random.uniform(120, 150, len(outlier_indices))
    
    return data

if __name__ == '__main__':

    ehr_data = generate_synthetic_ehr_data(1000)
    
    ehr_data.to_csv('synthetic_ehr_data.csv', index=False)
    print("Generated synthetic EHR data and saved to 'synthetic_ehr_data.csv'")