#!/usr/bin/env python3
"""
COVID-19 Vaccination Dashboard - Tamil Nadu
==========================================

Interactive Streamlit dashboard for COVID-19 vaccination data analysis.
Provides comprehensive visualizations, filtering, and insights.

Author: Data Analysis Team
Date: 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os
from pathlib import Path

# Suppress warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="COVID-19 Vaccination Dashboard - Tamil Nadu",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    * {
        color: #000000 !important;
    }
    body, .main, .sidebar, .stMarkdown, h1, h2, h3, h4, h5, h6, p, div, span {
        color: #000000 !important;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.25rem solid #1f77b4;
        color: #000000 !important;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.25rem solid #17a2b8;
        margin: 1rem 0;
        color: #000000 !important;
    }
    .stMetric {
        color: #000000 !important;
    }
    .stSelectbox, .stRadio, .stCheckbox, .stTextInput {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the cleaned vaccination data"""
    try:
        base_dir = Path(__file__).resolve().parent.parent
        data_path = base_dir / "cleaned_data" / "cleaned_vaccination_data.csv"
        df = pd.read_csv(data_path)

        # Load enhanced data if available
        enhanced_path = base_dir / "cleaned_data" / "enhanced_vaccination_data.csv"
        if enhanced_path.exists():
            df_enhanced = pd.read_csv(enhanced_path)
            return df_enhanced
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run the EDA notebook first to generate cleaned data.")
        return None

def main():
    """Main dashboard function"""

    # Load data
    df = load_data()
    if df is None:
        return

    # Main header
    st.markdown('<h1 class="main-header">💉 COVID-19 Vaccination Dashboard - Tamil Nadu</h1>', unsafe_allow_html=True)
    st.markdown("### Comprehensive Analysis of Vaccination Program (June 2021)")

    # Sidebar filters
    st.sidebar.title("🎛️ Dashboard Controls")

    # District selector
    districts = ["All"] + sorted(df['District'].unique().tolist())
    selected_district = st.sidebar.selectbox("Select District", districts)

    # Filter data based on selection
    if selected_district != "All":
        filtered_df = df[df['District'] == selected_district]
        st.sidebar.info(f"Showing data for: {selected_district}")
    else:
        filtered_df = df
        st.sidebar.info("Showing data for all districts")

    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Overview", "📈 Analysis", "🔍 Comparisons", "🧠 Multivariate",
        "📋 Insights", "📊 Data Table", "ℹ️ About"
    ])

    with tab1:
        show_overview_tab(filtered_df, df)

    with tab2:
        show_analysis_tab(filtered_df, df)

    with tab3:
        show_comparisons_tab(filtered_df, df)

    with tab4:
        show_multivariate_tab(filtered_df, df)

    with tab5:
        show_insights_tab(filtered_df, df)

    with tab6:
        show_data_table_tab(filtered_df, df)

    with tab7:
        show_about_tab()

def show_overview_tab(filtered_df, full_df):
    """Overview tab with key metrics and summary"""

    st.header("📊 Project Overview & Key Metrics")

    # Key metrics cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_vaccinations = filtered_df['Total_All_Vaccinations'].sum()
        st.metric(
            "Total Vaccinations",
            f"{total_vaccinations:,.0f}",
            help="Total COVID-19 vaccine doses administered"
        )

    with col2:
        total_first_dose = filtered_df['Total_All_1st'].sum()
        st.metric(
            "First Dose",
            f"{total_first_dose:,.0f}",
            help="Total first dose vaccinations"
        )

    with col3:
        total_second_dose = filtered_df['Total_All_2nd'].sum()
        st.metric(
            "Second Dose",
            f"{total_second_dose:,.0f}",
            help="Total second dose vaccinations"
        )

    with col4:
        if 'Vaccination_Efficiency' in filtered_df.columns:
            avg_efficiency = filtered_df['Vaccination_Efficiency'].mean()
            st.metric(
                "Avg Completion Rate",
                f"{avg_efficiency:.1f}%",
                help="Average vaccination completion rate"
            )

    # Dataset summary
    st.subheader("📋 Dataset Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"**Total Districts:** {len(full_df)}")
    with col2:
        st.info(f"**Data Points:** {len(full_df) * len(full_df.columns)}")
    with col3:
        missing_pct = (filtered_df.isnull().sum().sum() / (len(filtered_df) * len(filtered_df.columns))) * 100
        st.info(f"**Data Completeness:** {100-missing_pct:.1f}%")

    # Top districts visualization
    st.subheader("🏆 Top Performing Districts")

    if 'District_Performance_Score' in full_df.columns:
        top_districts = full_df.nlargest(10, 'District_Performance_Score')

        fig = px.bar(
            top_districts,
            x='District',
            y='District_Performance_Score',
            title='Top 10 Districts by Performance Score',
            color='District_Performance_Score',
            color_continuous_scale='Blues'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    # Vaccine distribution
    st.subheader("💉 Vaccine Type Distribution")

    if 'Total_Covishield_Vaccination' in filtered_df.columns and 'Total_Covaxin_Vaccination' in filtered_df.columns:
        vaccine_data = pd.DataFrame({
            'Vaccine': ['Covishield', 'Covaxin'],
            'Doses': [
                filtered_df['Total_Covishield_Vaccination'].sum(),
                filtered_df['Total_Covaxin_Vaccination'].sum()
            ]
        })

        fig = px.pie(
            vaccine_data,
            values='Doses',
            names='Vaccine',
            title='Vaccine Distribution',
            color_discrete_sequence=['#FF9999', '#66B2FF']
        )
        st.plotly_chart(fig, use_container_width=True)

def show_analysis_tab(filtered_df, full_df):
    """Analysis tab with detailed visualizations"""

    st.header("📈 Detailed Analysis")

    # Vaccination by category
    st.subheader("👥 Vaccination by Beneficiary Category")

    if all(col in filtered_df.columns for col in ['Total_HCW_Vaccination', 'Total_FLW_Vaccination', 'Total_18_44_Vaccination']):
        category_data = pd.DataFrame({
            'Category': ['HCW', 'FLW', '18-44 Years', '45-60 Comorb', '60+ Comorb'],
            'Vaccinations': [
                filtered_df['Total_HCW_Vaccination'].sum(),
                filtered_df['Total_FLW_Vaccination'].sum(),
                filtered_df['Total_18_44_Vaccination'].sum(),
                filtered_df['Total_45_60_Comorb_Vaccination'].sum(),
                filtered_df['Total_60_Comorb_Vaccination'].sum()
            ]
        })

        fig = px.bar(
            category_data,
            x='Category',
            y='Vaccinations',
            title='Vaccination Distribution by Category',
            color='Vaccinations',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Efficiency analysis
    st.subheader("🎯 Vaccination Efficiency Analysis")

    if 'Vaccination_Efficiency' in filtered_df.columns:
        fig = px.histogram(
            filtered_df,
            x='Vaccination_Efficiency',
            nbins=20,
            title='Distribution of Vaccination Completion Rates',
            color_discrete_sequence=['#17a2b8']
        )
        st.plotly_chart(fig, use_container_width=True)

    # Scatter plot: First vs Second dose
    st.subheader("📊 First Dose vs Second Dose Relationship")

    if 'Total_All_1st' in filtered_df.columns and 'Total_All_2nd' in filtered_df.columns:
        fig = px.scatter(
            filtered_df,
            x='Total_All_1st',
            y='Total_All_2nd',
            hover_name='District',
            title='First Dose vs Second Dose Correlation'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap of correlations
    st.subheader("🔗 Correlation Matrix")

    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        corr_matrix = filtered_df[numeric_cols].corr()

        fig = px.imshow(
            corr_matrix,
            title='Correlation Matrix of Vaccination Metrics',
            color_continuous_scale='RdBu',
            zmin=-1, zmax=1
        )
        st.plotly_chart(fig, use_container_width=True)

def show_comparisons_tab(filtered_df, full_df):
    """Comparisons tab for vaccine and category analysis"""

    st.header("🔍 Comparative Analysis")

    # Covishield vs Covaxin comparison
    st.subheader("💉 Covishield vs Covaxin Performance")

    if all(col in filtered_df.columns for col in ['Total_Covishield_Vaccination', 'Total_Covaxin_Vaccination']):
        comparison_data = []
        for _, row in filtered_df.iterrows():
            comparison_data.extend([
                {'District': row['District'], 'Vaccine': 'Covishield', 'Vaccinations': row['Total_Covishield_Vaccination']},
                {'District': row['District'], 'Vaccine': 'Covaxin', 'Vaccinations': row['Total_Covaxin_Vaccination']}
            ])

        comparison_df = pd.DataFrame(comparison_data)

        fig = px.bar(
            comparison_df,
            x='District',
            y='Vaccinations',
            color='Vaccine',
            title='Covishield vs Covaxin Distribution by District',
            barmode='group'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    # HCW vs FLW comparison
    st.subheader("🏥 HCW vs FLW Vaccination Coverage")

    if 'Total_HCW_Vaccination' in filtered_df.columns and 'Total_FLW_Vaccination' in filtered_df.columns:
        hcw_flw_data = []
        for _, row in filtered_df.iterrows():
            hcw_flw_data.extend([
                {'District': row['District'], 'Category': 'HCW', 'Vaccinations': row['Total_HCW_Vaccination']},
                {'District': row['District'], 'Category': 'FLW', 'Vaccinations': row['Total_FLW_Vaccination']}
            ])

        hcw_flw_df = pd.DataFrame(hcw_flw_data)

        fig = px.bar(
            hcw_flw_df,
            x='District',
            y='Vaccinations',
            color='Category',
            title='Healthcare Workers vs Frontline Workers Vaccination',
            barmode='stack'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    # Age group comparison
    st.subheader("🎂 Age Group Vaccination Comparison")

    if all(col in filtered_df.columns for col in ['Total_18_44_Vaccination', 'Total_45_60_Comorb_Vaccination', 'Total_60_Comorb_Vaccination']):
        age_data = []
        for _, row in filtered_df.iterrows():
            age_data.extend([
                {'District': row['District'], 'Age_Group': '18-44 Years', 'Vaccinations': row['Total_18_44_Vaccination']},
                {'District': row['District'], 'Age_Group': '45-60 Comorb', 'Vaccinations': row['Total_45_60_Comorb_Vaccination']},
                {'District': row['District'], 'Age_Group': '60+ Comorb', 'Vaccinations': row['Total_60_Comorb_Vaccination']}
            ])

        age_df = pd.DataFrame(age_data)

        fig = px.bar(
            age_df,
            x='District',
            y='Vaccinations',
            color='Age_Group',
            title='Vaccination by Age Group',
            barmode='stack'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)


def show_multivariate_tab(filtered_df, full_df):
    """Advanced multivariate visualizations."""

    st.header("🧠 Multivariate Visualizations")
    st.markdown(
        "Explore hierarchical, multi-dimensional, and performance visualizations for deeper district-level insights."
    )

    if all(col in filtered_df.columns for col in [
        'Total_Covishield_Vaccination', 'Total_Covaxin_Vaccination',
        'Total_HCW_Vaccination', 'Total_FLW_Vaccination',
        'Total_All_Vaccinations', 'Vaccination_Efficiency',
        'District_Performance_Score', 'Covishield_Preference_Ratio'
    ]):
        # Bubble chart
        bubble_df = filtered_df.copy()
        bubble_df['Bubble_Size'] = np.where(
            bubble_df['Total_HCW_Vaccination'] > 0,
            (bubble_df['Total_HCW_Vaccination'] / bubble_df['Total_HCW_Vaccination'].max()) * 80 + 20,
            20
        )

        fig = px.scatter(
            bubble_df,
            x='Total_All_Vaccinations',
            y='Vaccination_Efficiency',
            size='Bubble_Size',
            color='District_Performance_Score',
            hover_name='District',
            title='Bubble Chart: Total Vaccinations vs Efficiency (Size = HCW Coverage)',
            color_continuous_scale='Viridis',
            labels={
                'Total_All_Vaccinations': 'Total Vaccinations',
                'Vaccination_Efficiency': 'Completion Rate (%)',
                'District_Performance_Score': 'Performance Score'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

        # Treemap
        treemap_data = []
        for _, row in filtered_df.iterrows():
            treemap_data.extend([
                {'District': row['District'], 'Vaccine': 'Covishield', 'Category': 'HCW', 'Vaccinations': row['Covishield_HCW_1st'] + row['Covishield_HCW_2nd']},
                {'District': row['District'], 'Vaccine': 'Covaxin', 'Category': 'HCW', 'Vaccinations': row['Covaxin_HCW_1st'] + row['Covaxin_HCW_2nd']},
                {'District': row['District'], 'Vaccine': 'Covishield', 'Category': 'FLW', 'Vaccinations': row['Covishield_FLW_1st'] + row['Covishield_FLW_2nd']},
                {'District': row['District'], 'Vaccine': 'Covaxin', 'Category': 'FLW', 'Vaccinations': row['Covaxin_FLW_1st'] + row['Covaxin_FLW_2nd']}
            ])
        treemap_df = pd.DataFrame(treemap_data)

        fig = px.treemap(
            treemap_df,
            path=['District', 'Vaccine', 'Category'],
            values='Vaccinations',
            title='Treemap: Vaccination Hierarchy by District, Vaccine, and Category',
            color='Vaccinations',
            color_continuous_scale='RdBu'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Sunburst
        sunburst_data = []
        for _, row in filtered_df.iterrows():
            sunburst_data.extend([
                {'District': row['District'], 'Vaccine': 'Covishield', 'Category': 'HCW', 'Vaccinations': row['Covishield_HCW_1st'] + row['Covishield_HCW_2nd']},
                {'District': row['District'], 'Vaccine': 'Covishield', 'Category': 'FLW', 'Vaccinations': row['Covishield_FLW_1st'] + row['Covishield_FLW_2nd']},
                {'District': row['District'], 'Vaccine': 'Covaxin', 'Category': 'HCW', 'Vaccinations': row['Covaxin_HCW_1st'] + row['Covaxin_HCW_2nd']},
                {'District': row['District'], 'Vaccine': 'Covaxin', 'Category': 'FLW', 'Vaccinations': row['Covaxin_FLW_1st'] + row['Covaxin_FLW_2nd']}
            ])
        sunburst_df = pd.DataFrame(sunburst_data)

        fig = px.sunburst(
            sunburst_df,
            path=['District', 'Vaccine', 'Category'],
            values='Vaccinations',
            title='Sunburst: Multi-level Vaccination Breakdown',
            color='Vaccinations',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Parallel coordinates
        parallel_data = filtered_df[[
            'District', 'Total_All_Vaccinations', 'Vaccination_Efficiency',
            'District_Performance_Score', 'Covishield_Preference_Ratio'
        ]].copy()
        parallel_data = parallel_data.fillna(0)

        fig = px.parallel_coordinates(
            parallel_data,
            color='District_Performance_Score',
            labels={
                'Total_All_Vaccinations': 'Total Vaccinations',
                'Vaccination_Efficiency': 'Completion Rate',
                'District_Performance_Score': 'Performance Score',
                'Covishield_Preference_Ratio': 'Covishield %'
            },
            color_continuous_scale='Viridis',
            title='Parallel Coordinates: District Profiles Across Key Metrics'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Clustered heatmap
        st.subheader("🔥 Correlation Heatmap: Vaccination Metrics")
        heatmap_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
        if len(heatmap_cols) > 1:
            corr_matrix = filtered_df[heatmap_cols].corr()
            fig = px.imshow(
                corr_matrix,
                title='Correlation Heatmap of All Vaccination Metrics',
                color_continuous_scale='RdBu',
                zmin=-1, zmax=1,
                aspect='auto'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Distribution analysis
        st.subheader("📊 Distribution Analysis: Key Metrics")
        col1, col2 = st.columns(2)

        with col1:
            # Histogram - Total Vaccinations
            fig = px.histogram(
                filtered_df,
                x='Total_All_Vaccinations',
                nbins=15,
                title='Distribution: Total Vaccinations',
                color_discrete_sequence=['#1f77b4']
            )
            st.plotly_chart(fig, use_container_width=True)

            # Histogram - Efficiency
            fig = px.histogram(
                filtered_df,
                x='Vaccination_Efficiency',
                nbins=15,
                title='Distribution: Completion Rate (%)',
                color_discrete_sequence=['#ff7f0e']
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Box plot - Performance Score
            fig = px.box(
                filtered_df,
                y='District_Performance_Score',
                title='District Performance Score Distribution',
                points='all',
                hover_data=['District']
            )
            st.plotly_chart(fig, use_container_width=True)

            # Box plot - Covishield Preference
            fig = px.box(
                filtered_df,
                y='Covishield_Preference_Ratio',
                title='Covishield Preference Ratio Distribution',
                points='all',
                hover_data=['District']
            )
            st.plotly_chart(fig, use_container_width=True)

        # Scatter matrix - Key relationships
        st.subheader("🔗 Key Metric Relationships")
        scatter_cols = ['Total_All_Vaccinations', 'Vaccination_Efficiency', 'District_Performance_Score']
        if all(col in filtered_df.columns for col in scatter_cols):
            # Create pairwise scatter plots
            for i, col1 in enumerate(scatter_cols):
                for col2 in scatter_cols[i+1:]:
                    col_a, col_b = st.columns(2)
                    if col_a:
                        fig = px.scatter(
                            filtered_df,
                            x=col1,
                            y=col2,
                            hover_name='District',
                            title=f'{col1} vs {col2}',
                            color='District_Performance_Score',
                            color_continuous_scale='Viridis'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        break


def show_insights_tab(filtered_df, full_df):
    """Insights tab with automated analysis and recommendations"""

    st.header("📋 Automated Insights & Recommendations")

    # Generate insights based on data
    insights = generate_insights(filtered_df, full_df)

    for category, items in insights.items():
        st.subheader(f"📊 {category.replace('_', ' ').title()}")

        for item in items:
            st.markdown(f'<div class="insight-box">{item}</div>', unsafe_allow_html=True)

    # Performance ranking
    st.subheader("🏆 District Performance Ranking")

    if 'District_Performance_Score' in full_df.columns:
        ranking_df = full_df[['District', 'District_Performance_Score']].sort_values(
            'District_Performance_Score', ascending=False
        ).head(10)

        st.dataframe(ranking_df)

        # Performance distribution
        fig = px.box(
            full_df,
            y='District_Performance_Score',
            title='Distribution of District Performance Scores',
            points='all',
            hover_data=['District']
        )
        st.plotly_chart(fig, use_container_width=True)

def show_data_table_tab(filtered_df, full_df):
    """Data table tab with filtering and export capabilities"""

    st.header("📊 Data Table View")

    # Data filtering options
    col1, col2 = st.columns(2)

    with col1:
        sort_by = st.selectbox("Sort by", filtered_df.select_dtypes(include=[np.number]).columns.tolist())

    with col2:
        sort_order = st.radio("Sort order", ["Descending", "Ascending"], horizontal=True)

    # Sort data
    ascending = sort_order == "Ascending"
    display_df = filtered_df.sort_values(sort_by, ascending=ascending)

    # Search functionality
    search_term = st.text_input("Search districts", "")
    if search_term:
        display_df = display_df[display_df['District'].str.contains(search_term, case=False, na=False)]

    # Display data table
    st.dataframe(display_df, use_container_width=True)

    # Export functionality
    if st.button("📥 Download Filtered Data as CSV"):
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="filtered_vaccination_data.csv",
            mime="text/csv"
        )

    # Summary statistics
    st.subheader("📈 Summary Statistics")
    st.dataframe(display_df.describe(), use_container_width=True)

def show_about_tab():
    """About tab with project information"""

    st.header("ℹ️ About This Project")

    st.markdown("""
    ## COVID-19 Vaccination Dashboard - Tamil Nadu

    ### 🎯 Objective
    This interactive dashboard provides comprehensive analysis of COVID-19 vaccination data for Tamil Nadu districts, offering insights into vaccination patterns, performance metrics, and strategic recommendations.

    ### 📊 Data Source
    - **Dataset**: District-wise COVID-19 vaccination data (June 23, 2021 - Day 150)
    - **Coverage**: All 39 districts of Tamil Nadu
    - **Metrics**: Covishield and Covaxin vaccination across HCW, FLW, and age groups

    ### 🛠️ Technologies Used
    - **Frontend**: Streamlit
    - **Visualization**: Plotly
    - **Data Processing**: Pandas, NumPy
    - **Analysis**: Scikit-learn

    ### 📈 Key Features
    - Interactive filtering by district
    - Real-time data visualization
    - Automated insights generation
    - Performance ranking system
    - Comparative analysis tools
    - Data export capabilities

    ### 👥 Target Audience
    - Health department officials
    - Policy makers
    - Researchers
    - Data analysts
    - General public

    ### 📞 Contact
    For questions or feedback, please refer to the project documentation.

    ---
    *Developed as part of COVID-19 vaccination analysis project*
    """)

def generate_insights(filtered_df, full_df):
    """Generate automated insights based on data analysis"""

    insights = {
        'key_metrics': [],
        'performance_analysis': [],
        'trends_identified': [],
        'recommendations': []
    }

    # Key metrics insights
    total_vacc = filtered_df['Total_All_Vaccinations'].sum()
    avg_efficiency = filtered_df['Vaccination_Efficiency'].mean() if 'Vaccination_Efficiency' in filtered_df.columns else 0

    insights['key_metrics'].extend([
        f"💉 Total vaccinations administered: {total_vacc:,.0f} doses",
        f"🎯 Average completion rate: {avg_efficiency:.1f}%",
        f"📊 Districts analyzed: {len(filtered_df)}",
        f"🏆 Top performing district: {filtered_df.loc[filtered_df['District_Performance_Score'].idxmax(), 'District'] if 'District_Performance_Score' in filtered_df.columns else 'N/A'}"
    ])

    # Performance analysis
    if 'District_Performance_Score' in filtered_df.columns:
        high_performers = len(filtered_df[filtered_df['District_Performance_Score'] > filtered_df['District_Performance_Score'].mean()])
        insights['performance_analysis'].extend([
            f"🏅 {high_performers} districts performing above average",
            f"⚠️ {len(filtered_df) - high_performers} districts need improvement",
            f"📈 Performance variation: {filtered_df['District_Performance_Score'].std():.2f} points"
        ])

    # Trends
    covishield_pct = (filtered_df['Total_Covishield_Vaccination'].sum() / total_vacc * 100) if total_vacc > 0 else 0
    insights['trends_identified'].extend([
        f"💉 Covishield preference: {covishield_pct:.1f}% of total vaccinations",
        f"🎯 {'Strong' if avg_efficiency > 75 else 'Moderate' if avg_efficiency > 60 else 'Weak'} completion rates observed",
        f"🏥 Priority groups show {'good' if filtered_df['Total_HCW_Vaccination'].sum() > total_vacc * 0.1 else 'variable'} coverage"
    ])

    # Recommendations
    insights['recommendations'].extend([
        "🎯 Focus on second-dose completion in low-performing districts",
        "💉 Optimize vaccine distribution for better balance",
        "🏥 Strengthen rural healthcare infrastructure",
        "📊 Implement real-time monitoring systems",
        "🎓 Provide targeted training for healthcare workers"
    ])

    return insights

if __name__ == "__main__":
    main()