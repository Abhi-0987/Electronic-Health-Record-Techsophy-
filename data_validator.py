import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Any
from sklearn.ensemble import IsolationForest

class EHRDataValidator:
    def __init__(self):
        self.validation_rules = {
            'completeness': self._check_completeness,
            'consistency': self._check_consistency,
            'outliers': self._check_outliers,
            'format': self._check_format
        }
        
        self.vital_signs_ranges = {
            'systolic_bp': (70, 180),
            'diastolic_bp': (40, 120),
            'heart_rate': (40, 120),
            'temperature': (95, 104)
        }
        
        self.expected_dtypes = {
            'patient_id': 'int64',
            'timestamp': 'datetime64[ns]',
            'age': 'int64',
            'gender': 'object',
            'systolic_bp': 'float64',
            'diastolic_bp': 'float64',
            'heart_rate': 'float64',
            'temperature': 'float64',
            'diagnosis': 'object',
            'medications': 'object'
        }
    
    def validate_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {}
        for check_name, check_func in self.validation_rules.items():
            results[check_name] = check_func(data)
        return results
    
    def _check_completeness(self, data: pd.DataFrame) -> Dict[str, float]:
        completeness_scores = {}
        for column in data.columns:
            completeness_scores[column] = {
                'completion_rate': (1 - data[column].isnull().mean()) * 100,
                'missing_count': data[column].isnull().sum()
            }
        return completeness_scores
    
    def _check_consistency(self, data: pd.DataFrame) -> Dict[str, List[Dict[str, Any]]]:
        consistency_issues = {
            'gender_coding': self._check_gender_consistency(data),
            'vital_signs': self._check_vital_signs_consistency(data),
            'medication_diagnosis': self._check_medication_diagnosis_consistency(data)
        }
        return consistency_issues
    
    def _check_gender_consistency(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        valid_codes = {'M', 'F', 'Male', 'Female'}
        invalid_records = data[~data['gender'].isin(valid_codes)]
        return self._format_issues(invalid_records, 'Invalid gender coding')
    
    def _check_vital_signs_consistency(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        issues = []
        for vital_sign, (min_val, max_val) in self.vital_signs_ranges.items():
            invalid_records = data[
                (data[vital_sign] < min_val) | 
                (data[vital_sign] > max_val)
            ]
            if not invalid_records.empty:
                issues.extend(self._format_issues(
                    invalid_records,
                    f'{vital_sign} out of range ({min_val}-{max_val})'
                ))
        return issues
    
    def _check_medication_diagnosis_consistency(
        self,
        data: pd.DataFrame
    ) -> List[Dict[str, Any]]:
        medication_diagnosis_pairs = {
            'Lisinopril': 'Hypertension',
            'Metformin': 'Diabetes',
            'Albuterol': 'Asthma'
        }
        
        issues = []
        for medication, diagnosis in medication_diagnosis_pairs.items():
            inconsistent_records = data[
                (data['medications'].apply(lambda x: medication in x)) & 
                (data['diagnosis'] != diagnosis)
            ]
            if not inconsistent_records.empty:
                issues.extend(self._format_issues(
                    inconsistent_records,
                    f'Inconsistent {medication}-{diagnosis} pair'
                ))
        return issues
    
    def _check_outliers(self, data: pd.DataFrame) -> Dict[str, List[Dict[str, Any]]]:
        numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
        outliers = {}
        
        for column in numerical_columns:
            if column in ['patient_id', 'age']:
                continue
                
            valid_data = data[column].dropna().values.reshape(-1, 1)
            if len(valid_data) > 0:
                iso_forest = IsolationForest(contamination=0.1, random_state=42)
                predictions = iso_forest.fit_predict(valid_data)
                outlier_indices = np.where(predictions == -1)[0]
                
                if len(outlier_indices) > 0:
                    outlier_records = data.iloc[outlier_indices]
                    outliers[column] = self._format_issues(
                        outlier_records,
                        f'Outlier detected in {column}'
                    )
        
        return outliers
    
    def _check_format(self, data: pd.DataFrame) -> Dict[str, List[str]]:
        format_issues = {}
        
        for column, expected_type in self.expected_dtypes.items():
            if column not in data.columns:
                format_issues[column] = [f'Column {column} is missing']
                continue
                
            current_type = str(data[column].dtype)
            if current_type != expected_type:
                format_issues[column] = [
                    f'Incorrect data type: expected {expected_type}, got {current_type}'
                ]
        
        if 'timestamp' in data.columns:
            invalid_timestamps = data[
                pd.to_datetime(data['timestamp'], errors='coerce').isnull()
            ]
            if not invalid_timestamps.empty:
                format_issues['timestamp'] = [
                    f'Invalid timestamp format in {len(invalid_timestamps)} records'
                ]
        
        return format_issues
    
    def _format_issues(
        self,
        records: pd.DataFrame,
        issue_description: str
    ) -> List[Dict[str, Any]]:
        return [{
            'patient_id': row['patient_id'],
            'timestamp': row['timestamp'],
            'issue': issue_description,
            'values': {col: row[col] for col in records.columns}
        } for _, row in records.iterrows()]
    
    def calculate_quality_score(self, validation_results: Dict[str, Any]) -> float:
        scores = []
        
        completeness_scores = [
            score['completion_rate'] 
            for score in validation_results['completeness'].values()
        ]
        scores.append(np.mean(completeness_scores) * 0.4)
        
        consistency_issues = sum(
            len(issues) for issues in validation_results['consistency'].values()
        )
        consistency_score = max(0, 100 - (consistency_issues * 2))
        scores.append(consistency_score * 0.3)
        
        format_issues = sum(
            len(issues) for issues in validation_results['format'].values()
        )
        format_score = max(0, 100 - (format_issues * 5))
        scores.append(format_score * 0.3)
        
        return sum(scores)