import pandas as pd
from data_generator import generate_synthetic_ehr_data
from data_validator import EHRDataValidator
from report_generator import EHRQualityReporter
import argparse
import os

def main(input_file: str = None, output_dir: str = 'reports'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if input_file and os.path.exists(input_file):
        print(f"Loading data from {input_file}")
        data = pd.read_csv(input_file)
        
        if 'timestamp' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
    else:
        print("Generating synthetic EHR data for demonstration")
        data = generate_synthetic_ehr_data(1000)
        
        synthetic_data_path = os.path.join(output_dir, 'synthetic_ehr_data.csv')
        data.to_csv(synthetic_data_path, index=False)
        print(f"Synthetic data saved to {synthetic_data_path}")
    
    # Initialize components
    validator = EHRDataValidator()
    reporter = EHRQualityReporter(output_dir)
    
    print("\nValidating data...")
    validation_results = validator.validate_data(data)
    
    quality_score = validator.calculate_quality_score(validation_results)
    validation_results['quality_score'] = quality_score
    
    print("\nGenerating quality report...")
    reporter.generate_report(data, validation_results)
    
    print(f"\nValidation Summary:")
    print(f"Overall Quality Score: {quality_score:.1f}%")
    print(f"Total Records: {len(data)}")
    print(f"Time Range: {data['timestamp'].min()} to {data['timestamp'].max()}")
    print(f"Number of Patients: {data['patient_id'].nunique()}")
    
    print("\nMajor Issues Detected:")
    for field, scores in validation_results['completeness'].items():
        if scores['completion_rate'] < 90:
            print(f"- Low completion rate for {field}: {scores['completion_rate']:.1f}%")
    
    consistency_issues = sum(len(issues) for issues in validation_results['consistency'].values())
    if consistency_issues > 0:
        print(f"- Found {consistency_issues} consistency issues")
    
    format_issues = sum(len(issues) for issues in validation_results['format'].values())
    if format_issues > 0:
        print(f"- Found {format_issues} format issues")
    
    print(f"\nDetailed report has been generated in the '{output_dir}' directory")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EHR Data Quality Auditor')
    parser.add_argument('--input', type=str, help='Path to input CSV file (optional)')
    parser.add_argument('--output', type=str, default='reports',
                        help='Output directory for reports (default: reports)')
    
    args = parser.parse_args()
    main(args.input, args.output)