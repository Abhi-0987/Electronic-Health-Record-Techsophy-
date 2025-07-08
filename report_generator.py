import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any
from datetime import datetime
import os

class EHRQualityReporter:
    def __init__(self, output_dir: str = 'reports'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_report(self, data: pd.DataFrame, validation_results: Dict[str, Any]):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_dir = os.path.join(self.output_dir, f'report_{timestamp}')
        os.makedirs(report_dir)
        
        self._generate_completeness_chart(validation_results, report_dir)
        self._generate_vital_signs_distribution(data, report_dir)
        self._generate_temporal_quality_chart(data, validation_results, report_dir)
        
        html_report = self._create_html_report(data, validation_results, timestamp)
        with open(os.path.join(report_dir, 'report.html'), 'w') as f:
            f.write(html_report)
        
        print(f"Report generated successfully in {report_dir}")
    
    def _generate_completeness_chart(self, validation_results: Dict[str, Any], report_dir: str):
        completion_rates = {
            field: scores['completion_rate']
            for field, scores in validation_results['completeness'].items()
        }
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(completion_rates.keys(), completion_rates.values())
        plt.xticks(rotation=45, ha='right')
        plt.title('Data Completeness by Field')
        plt.ylabel('Completion Rate (%)')
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(os.path.join(report_dir, 'completeness.png'))
        plt.close()
    
    def _generate_vital_signs_distribution(self, data: pd.DataFrame, report_dir: str):
        vital_signs = ['systolic_bp', 'diastolic_bp', 'heart_rate', 'temperature']
        
        plt.figure(figsize=(12, 8))
        for i, vital in enumerate(vital_signs, 1):
            plt.subplot(2, 2, i)
            sns.histplot(data=data, x=vital, kde=True)
            plt.title(f'{vital.replace("_", " ").title()} Distribution')
        
        plt.tight_layout()
        plt.savefig(os.path.join(report_dir, 'vital_signs_distribution.png'))
        plt.close()
    
    def _generate_temporal_quality_chart(self, data: pd.DataFrame, validation_results: Dict[str, Any], report_dir: str):
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        daily_stats = data.groupby(data['timestamp'].dt.date).agg({
            'systolic_bp': lambda x: x.notnull().mean() * 100,
            'diastolic_bp': lambda x: x.notnull().mean() * 100,
            'heart_rate': lambda x: x.notnull().mean() * 100,
            'temperature': lambda x: x.notnull().mean() * 100
        })
        
        plt.figure(figsize=(12, 6))
        for column in daily_stats.columns:
            plt.plot(daily_stats.index, daily_stats[column], label=column, marker='o')
        
        plt.title('Temporal Data Quality Trends')
        plt.xlabel('Date')
        plt.ylabel('Completion Rate (%)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(report_dir, 'temporal_quality.png'))
        plt.close()
    
    def _create_html_report(self, data: pd.DataFrame, validation_results: Dict[str, Any], timestamp: str) -> str:
        quality_score = validation_results.get('quality_score', 0)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>EHR Data Quality Report - {timestamp}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                .quality-score {{ font-size: 24px; font-weight: bold; color: {'green' if quality_score >= 80 else 'orange' if quality_score >= 60 else 'red'}; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f8f9fa; }}
                .issue {{ color: #dc3545; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>EHR Data Quality Report</h1>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Overall Quality Score: <span class="quality-score">{quality_score:.1f}%</span></p>
            </div>
            
            <div class="section">
                <h2>Dataset Overview</h2>
                <ul>
                    <li>Total Records: {len(data)}</li>
                    <li>Time Range: {data['timestamp'].min()} to {data['timestamp'].max()}</li>
                    <li>Number of Patients: {data['patient_id'].nunique()}</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>Completeness Analysis</h2>
                <img src="completeness.png" alt="Completeness Chart" style="max-width: 100%;">
                <table>
                    <tr>
                        <th>Field</th>
                        <th>Completion Rate</th>
                        <th>Missing Count</th>
                    </tr>
                    {''.join(
                        f"<tr><td>{field}</td><td>{scores['completion_rate']:.1f}%</td><td>{scores['missing_count']}</td></tr>"
                        for field, scores in validation_results['completeness'].items()
                    )}
                </table>
            </div>
            
            <div class="section">
                <h2>Data Distribution</h2>
                <img src="vital_signs_distribution.png" alt="Vital Signs Distribution" style="max-width: 100%;">
            </div>
            
            <div class="section">
                <h2>Temporal Quality Trends</h2>
                <img src="temporal_quality.png" alt="Temporal Quality Trends" style="max-width: 100%;">
            </div>
            
            <div class="section">
                <h2>Consistency Issues</h2>
                <table>
                    <tr>
                        <th>Issue Type</th>
                        <th>Count</th>
                        <th>Details</th>
                    </tr>
                    {''.join(
                        f"<tr><td>{issue_type}</td><td>{len(issues)}</td><td>{', '.join(str(issue['issue']) for issue in issues[:3])}...</td></tr>"
                        for issue_type, issues in validation_results['consistency'].items() if issues
                    )}
                </table>
            </div>
            
            <div class="section">
                <h2>Format Issues</h2>
                <table>
                    <tr>
                        <th>Field</th>
                        <th>Issues</th>
                    </tr>
                    {''.join(
                        f"<tr><td>{field}</td><td class='issue'>{', '.join(issues)}</td></tr>"
                        for field, issues in validation_results['format'].items() if issues
                    )}
                </table>
            </div>
        </body>
        </html>
        """
        
        return html_content