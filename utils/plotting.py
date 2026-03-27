"""Plotting utilities for shadow price analysis"""

import plotly.graph_objects as go
import pandas as pd
import os
import subprocess


def shadowPlot(df, y_column, save=False, auto_commit=False):
    """
    Create a Plotly plot grouped by TSO.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe containing 'tso', 'dateTimeUtc' and the y_column
    y_column : str
        Column name to plot on y axis. Also used as the filename for saving.
    save : bool, optional
        If True, save the plot as an HTML file with the column name (default: False)
    auto_commit : bool, optional
        If True, automatically commit and push the saved plot to git repo (default: False)
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive Plotly figure
    """
    # Convert index (dateTimeUtc) to CET
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    df['dateTimeCET'] = df.index.tz_convert('CET')
    
    # Create figure
    fig = go.Figure()
    
    # Group by TSO and add traces
    for tso in df['tso'].unique():
        tso_data = df[df['tso'] == tso].sort_values('dateTimeCET')
        fig.add_trace(go.Scatter(
            x=tso_data['dateTimeCET'],
            y=tso_data[y_column],
            mode='markers',
            name=str(tso),
            hovertemplate='<b>%{fullData.name}</b><br>Time: %{x}<br>' + y_column + ': %{y}<extra></extra>'
        ))
    
    # Update layout
    fig.update_layout(
        title=f'{y_column} by TSO',
        xaxis_title='Time (CET)',
        yaxis_title=y_column,
        hovermode='x unified',
        template='plotly_white',
        height=600
    )

    # Save plot with filename based on y_column if save flag is True
    if save:
        save_filename = f'{y_column}.html'
        fig.write_html(save_filename)
        print(f"Plot saved to: {save_filename}")
        
        # Auto commit and push if requested
        if auto_commit:
            try:
                subprocess.run(['git', 'add', save_filename], check=True, capture_output=True)
                subprocess.run(['git', 'commit', '-m', f'Automated commit: Add plot {save_filename}'], 
                             check=True, capture_output=True)
                subprocess.run(['git', 'push'], check=True, capture_output=True)
                print(f"Committed and pushed {save_filename} to repository")
            except subprocess.CalledProcessError as e:
                print(f"Git operation failed: {e}")
    
    fig.show()
