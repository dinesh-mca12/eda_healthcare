# COVID-19 Vaccination Dashboard - Tamil Nadu

## Project Overview

This project provides a comprehensive Exploratory Data Analysis (EDA) and interactive dashboard for COVID-19 vaccination data in Tamil Nadu, India. The analysis covers vaccination achievements across different districts, beneficiary categories (HCW, FLW, age groups), and vaccine types (Covishield and Covaxin).

## Objectives

- Analyze vaccination patterns and trends across Tamil Nadu districts
- Compare performance between Covishield and Covaxin vaccines
- Identify vaccination gaps and completion rates
- Provide interactive visualizations for data exploration
- Generate automated insights and recommendations

## Technologies Used

- **Python** - Core programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **Matplotlib & Seaborn** - Static visualizations
- **Plotly** - Interactive visualizations
- **Streamlit** - Interactive dashboard framework
- **Scikit-learn** - Statistical analysis
- **Jupyter Notebook** - EDA environment

## Installation Steps

1. Clone or download the project repository
2. Navigate to the project directory:
   ```bash
   cd covid_vaccination_dashboard
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### EDA Analysis

Run the Jupyter notebook for detailed exploratory data analysis:

```bash
jupyter notebook notebooks/eda_analysis.ipynb
```

### Interactive Dashboard

Launch the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

## Dashboard Features

### 1. Project Overview

- Dataset summary and key metrics
- Vaccination coverage statistics

### 2. Dataset Summary

- Data shape and structure
- Missing values analysis
- District and category breakdowns

### 3. Interactive Filters

- District selection
- Vaccine type filtering
- Dose type selection
- Beneficiary category filtering

### 4. KPI Cards

- Total vaccinations administered
- First and second dose statistics
- District performance rankings
- Completion rate percentages

### 5. Visualization Gallery

- Bar charts, line charts, pie charts
- Heatmaps, scatter plots, box plots
- Treemaps, sunburst charts, radar charts
- Interactive Plotly visualizations

### 6. Comparative Analysis

- Covishield vs Covaxin performance
- First dose vs second dose completion
- HCW vs FLW vaccination trends

### 7. Automated Insights

- Trend analysis and interpretations
- Anomaly detection
- Business impact explanations

### 8. Data Table View

- Searchable and sortable data table
- Filtered data export functionality

### 9. Advanced Analytics

- Correlation matrix analysis
- Statistical summaries
- Performance rankings

### 10. About Section

- Project objectives and methodology
- Technology stack details
- Learning outcomes

## EDA Process

The exploratory data analysis includes:

1. **Data Loading & Cleaning**
   - Automatic CSV detection and loading
   - Missing value handling
   - Data type conversions
   - Outlier detection and treatment

2. **Feature Engineering**
   - Total vaccination calculations
   - Efficiency and completion rate metrics
   - District performance scores

3. **Univariate Analysis**
   - Distribution analysis
   - Central tendency and spread measures
   - Outlier identification

4. **Bivariate Analysis**
   - Relationship exploration between variables
   - Correlation studies
   - Comparative visualizations

5. **Multivariate Analysis**
   - Complex relationship mapping
   - Clustering and pattern detection

6. **Advanced Analytics**
   - Trend analysis
   - Statistical testing
   - Predictive insights

## Key Insights

- District-wise vaccination performance variations
- Vaccine preference patterns (Covishield vs Covaxin)
- Age-group specific vaccination trends
- HCW and FLW coverage analysis
- Dose completion rate analysis
- Temporal vaccination patterns

## Future Enhancements

- Real-time data integration
- Predictive modeling for vaccination trends
- Geographic mapping with choropleth visualizations
- Mobile-responsive dashboard optimization
- Automated report generation
- Machine learning-based anomaly detection

## Data Source

The dataset contains district-wise COVID-19 vaccination data for Tamil Nadu as of June 23, 2021 (Day 150 of vaccination campaign), including achievements for Covishield and Covaxin vaccines across different beneficiary categories.

## Contact

For questions or contributions, please refer to the project documentation or create an issue in the repository.
