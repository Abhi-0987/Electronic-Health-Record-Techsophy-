# EHR Data Generation and Quality Report

This project generates synthetic Electronic Health Record (EHR) data or you can provide the data you want to analyze and provides a quality report.

## Setup and Execution

To set up and run this project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Abhi-0987/Electronic-Health-Record-Techsophy-.git
   cd Electronic-Health-Record-Techsophy-
   ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv_ehr
    ```
    On Windows, activate with:
    ```bash
    .\venv_ehr\Scripts\activate
    ```
    On macOS/Linux, activate with:
    ```bash
    source venv_ehr/bin/activate
    ```

3.  **Install Dependencies:**
    With the virtual environment activated, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    You can run the main script directly from the command line (after activating the virtual environment):
    ```terminal
    python main.py
    ```
   To analyze your own EHR data, you can provide a CSV file using the `--input` argument:
   ```bash
   python main.py --input path/to/your/data.csv
   ```

   The script will generate synthetic EHR data and a quality report in the `reports/` directory.

## Features

- **Data Quality Validation**
  - Completeness checking
  - Consistency validation
  - Outlier detection
  - Format verification

- **Advanced Analytics**
  - Automated data quality scoring
  - Pattern recognition
  - Temporal trend analysis
  - Statistical distributions

- **Comprehensive Reporting**
  - Interactive HTML reports
  - Data visualization
  - Detailed issue tracking
  - Quality metrics dashboard

**Note:** The tool expects your input CSV file to have the following columns and data types for proper validation:

### Data Format Requirements

Whether generated or provided, the EHR data should adhere to the following structure: 
- patient_id (integer)
- timestamp (datetime)
- age (integer)
- gender (string: 'M'/'F' or 'Male'/'Female')
- systolic_bp (float)
- diastolic_bp (float)
- heart_rate (float)
- temperature (float)
- diagnosis (string)
- medications (list/string)

## Output

The tool generates a comprehensive report including:

1. **Quality Score**: Overall data quality assessment
2. **Completeness Analysis**: Missing data analysis by field
3. **Consistency Check**: Identification of inconsistent values
4. **Outlier Detection**: Statistical analysis of unusual values
5. **Format Validation**: Data type and format verification
6. **Visualizations**: 
   - Data completeness charts
   - Vital signs distributions
   - Temporal quality trends

## Project Structure

```
├── data_generator.py     # Synthetic data generation
├── data_validator.py     # Data validation logic
├── report_generator.py   # Report generation module
├── main.py              # Main application script
├── requirements.txt      # Project dependencies
└── reports/             # Generated reports directory
```

## Validation Rules

The tool implements various validation rules including:

1. **Completeness Rules**
   - Missing value detection
   - Required field validation

2. **Consistency Rules**
   - Gender coding consistency
   - Vital signs range validation
   - Medication-diagnosis correlation

3. **Format Rules**
   - Data type verification
   - Date format standardization
   - Coding standard compliance

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.