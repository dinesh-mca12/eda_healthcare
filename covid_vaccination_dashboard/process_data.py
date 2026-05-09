#!/usr/bin/env python3
"""
COVID-19 Vaccination Data Processing Script
==========================================

This script performs data loading, cleaning, and feature engineering
to prepare the vaccination data for analysis and dashboard.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

def main():
    print("Starting COVID-19 Vaccination Data Processing...")

    # Set up paths
    base_dir = Path.cwd()
    data_dir = base_dir / "data"
    cleaned_data_dir = base_dir / "cleaned_data"
    visuals_dir = base_dir / "visuals" / "saved_charts"
    reports_dir = base_dir / "reports"

    # Create directories
    cleaned_data_dir.mkdir(exist_ok=True)
    visuals_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)

    # Find and load data
    csv_files = list(data_dir.glob("*.csv"))
    data_file = None
    for file in csv_files:
        if 'day_150' in file.name:
            data_file = file
            break

    if data_file is None and csv_files:
        data_file = csv_files[0]

    print(f"Loading data from: {data_file}")

    # Load data
    df = pd.read_csv(data_file)

    # Basic cleaning
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.strip()

    # Convert numeric columns
    for col in df_clean.columns:
        if col != 'Health Unit District':
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    df_clean = df_clean.fillna(0)

    # Rename columns
    column_rename_map = {
        'Health Unit District': 'District',
        'Achievement towards vaccination of 1st Dosage Covishield to HCW': 'Covishield_HCW_1st',
        'Achievement towards vaccination of 2nd Dosage Covishield to HCW': 'Covishield_HCW_2nd',
        'Achievement towards vaccination of 1st Dosage Covishield to FLW': 'Covishield_FLW_1st',
        'Achievement towards vaccination of 2nd Dosage Covishield to FLW': 'Covishield_FLW_2nd',
        'Achievement towards vaccination of 1st Dosage Covishield to beneficiaries of 18 years and less than 44 years age group': 'Covishield_18_44_1st',
        'Achievement towards vaccination of 2nd Dosage Covishield to beneficiaries of 18 years and less than 44 years age group': 'Covishield_18_44_2nd',
        'Achievement towards vaccination of 1st Dosage Covishield to beneficiaries of 45 years and less than 60 years age group with Comorbidities': 'Covishield_45_60_Comorb_1st',
        'Achievement towards vaccination of 2nd Dosage Covishield to beneficiaries of 45 years and less than 60 years age group with Comorbidities': 'Covishield_45_60_Comorb_2nd',
        'Achievement towards vaccination of 1st Dosage Covishield to 60+ years beneficiaries with Comorbidities': 'Covishield_60_Comorb_1st',
        'Achievement towards vaccination of 2nd Dosage Covishield to 60+ years beneficiaries with Comorbidities': 'Covishield_60_Comorb_2nd',
        'Total Achievement of vaccination to beneficiaries under 1st Dose of Covishield': 'Covishield_Total_1st',
        'Total Achievement of vaccination to beneficiaries under 2nd Dose of Covishield': 'Covishield_Total_2nd',
        'Achievement towards vaccination of 1st Dosage Covaxin to HCW': 'Covaxin_HCW_1st',
        'Achievement towards vaccination of 2nd Dosage Covaxin to HCW': 'Covaxin_HCW_2nd',
        'Achievement towards vaccination of 1st Dosage Covaxin to FLW': 'Covaxin_FLW_1st',
        'Achievement towards vaccination of 2nd Dosage Covaxin to FLW': 'Covaxin_FLW_2nd',
        'Achievement towards vaccination of 1st Dosage Covaxin to beneficiaries of 18 years and less than 44 years age group': 'Covaxin_18_44_1st',
        'Achievement towards vaccination of 2nd Dosage Covaxin to beneficiaries of 18 years and less than 44 years age group': 'Covaxin_18_44_2nd',
        'Achievement towards vaccination of 1st Dosage Covaxin to beneficiaries of 45 years and less than 60 years age group with Comorbidities': 'Covaxin_45_60_Comorb_1st',
        'Achievement towards vaccination of 2nd Dosage Covaxin to beneficiaries of 45 years and less than 60 years age group with Comorbidities': 'Covaxin_45_60_Comorb_2nd',
        'Achievement towards vaccination of 1st Dosage Covaxin to 60+ years beneficiaries with Comorbidities': 'Covaxin_60_Comorb_1st',
        'Achievement towards vaccination of 2nd Dosage Covaxin to 60+ years beneficiaries with Comorbidities': 'Covaxin_60_Comorb_2nd',
        'Total Achievement of vaccination to beneficiaries under 1st Dose of Covaxin': 'Covaxin_Total_1st',
        'Total Achievement of vaccination to beneficiaries under 2nd Dose of Covaxin': 'Covaxin_Total_2nd',
        'Total Achievement towards vaccination of 1st Dosage Covishield and Covaxin to HCW': 'Total_HCW_1st',
        'Total Achievement towards vaccination of 2nd Dosage Covishield and Covaxin to HCW': 'Total_HCW_2nd',
        'Total Achievement towards vaccination of 1st Dosage Covishield and Covaxin to FLW': 'Total_FLW_1st',
        'Total Achievement towards vaccination of 2nd Dosage Covishield and Covaxin to FLW': 'Total_FLW_2nd',
        'Total Achievement towards vaccination of 1st Dosage Covishield and Covaxin to beneficiaries of 18 years and less than 44 years age group': 'Total_18_44_1st',
        'Total Achievement towards vaccination of 2nd Dosage Covishield and Covaxin to beneficiaries of 18 years and less than 44 years age group': 'Total_18_44_2nd',
        'Total Achievement towards vaccination of 1st Dosage Covishield and Covaxin to beneficiaries of 45 years and less than 60 years age group with Comorbidities': 'Total_45_60_Comorb_1st',
        'Total Achievement towards vaccination of 2nd Dosage Covishield and Covaxin to beneficiaries of 45 years and less than 60 years age group with Comorbidities': 'Total_45_60_Comorb_2nd',
        'Total Achievement towards vaccination of 1st Dosage Covishield and Covaxin to 60+ years beneficiaries with Comorbidities': 'Total_60_Comorb_1st',
        'Total Achievement towards vaccination of 2nd Dosage Covishield and Covaxin to 60+ years beneficiaries with Comorbidities': 'Total_60_Comorb_2nd',
        'Total Achievement towards vaccination to beneficiaries under 1st Dose of Covishield and Covaxin': 'Total_All_1st',
        'Total Achievement towards vaccination to beneficiaries under 2nd Dose of Covishield and Covaxin': 'Total_All_2nd',
        'Total Achievement towards vaccination of Covishield and Covaxin (1st and 2nd Dose)': 'Total_All_Vaccinations'
    }

    df_clean = df_clean.rename(columns=column_rename_map)

    # Feature engineering
    df_clean['Total_HCW_Vaccination'] = df_clean['Total_HCW_1st'] + df_clean['Total_HCW_2nd']
    df_clean['Total_FLW_Vaccination'] = df_clean['Total_FLW_1st'] + df_clean['Total_FLW_2nd']
    df_clean['Total_Covishield_Vaccination'] = df_clean['Covishield_Total_1st'] + df_clean['Covishield_Total_2nd']
    df_clean['Total_Covaxin_Vaccination'] = df_clean['Covaxin_Total_1st'] + df_clean['Covaxin_Total_2nd']

    df_clean['Vaccination_Efficiency'] = np.where(
        df_clean['Total_All_1st'] > 0,
        (df_clean['Total_All_2nd'] / df_clean['Total_All_1st']) * 100,
        0
    )

    # Additional features
    df_clean['Total_18_44_Vaccination'] = df_clean['Total_18_44_1st'] + df_clean['Total_18_44_2nd']
    df_clean['Total_45_60_Comorb_Vaccination'] = df_clean['Total_45_60_Comorb_1st'] + df_clean['Total_45_60_Comorb_2nd']
    df_clean['Total_60_Comorb_Vaccination'] = df_clean['Total_60_Comorb_1st'] + df_clean['Total_60_Comorb_2nd']

    df_clean['Covishield_Preference_Ratio'] = np.where(
        df_clean['Total_All_Vaccinations'] > 0,
        (df_clean['Total_Covishield_Vaccination'] / df_clean['Total_All_Vaccinations']) * 100,
        0
    )

    # District performance score (simplified)
    # Normalize using min-max scaling
    perf_cols = ['Total_All_Vaccinations', 'Vaccination_Efficiency', 'Total_HCW_Vaccination', 'Total_FLW_Vaccination']
    perf_data = df_clean[perf_cols].copy()

    for col in perf_cols:
        if perf_data[col].max() > perf_data[col].min():
            perf_data[f'{col}_norm'] = (perf_data[col] - perf_data[col].min()) / (perf_data[col].max() - perf_data[col].min())
        else:
            perf_data[f'{col}_norm'] = 0.5  # Default to middle value

    df_clean['District_Performance_Score'] = (
        perf_data['Total_All_Vaccinations_norm'] * 0.4 +
        perf_data['Vaccination_Efficiency_norm'] * 0.3 +
        perf_data['Total_HCW_Vaccination_norm'] * 0.15 +
        perf_data['Total_FLW_Vaccination_norm'] * 0.15
    )

    # Save cleaned data
    cleaned_file = cleaned_data_dir / "cleaned_vaccination_data.csv"
    df_clean.to_csv(cleaned_file, index=False)
    print(f"Cleaned data saved to: {cleaned_file}")

    # Save enhanced data
    enhanced_file = cleaned_data_dir / "enhanced_vaccination_data.csv"
    df_clean.to_csv(enhanced_file, index=False)
    print(f"Enhanced data saved to: {enhanced_file}")

    print("Data processing completed successfully!")
    print(f"Processed {len(df_clean)} districts with {len(df_clean.columns)} features")

if __name__ == "__main__":
    main()