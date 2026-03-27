"""Plotting utilities for shadow price analysis"""

import plotly.graph_objects as go
import pandas as pd


def shadowPlot(df, y_column):
    """
    Create a Plotly plot grouped by TSO.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe containing 'tso', 'dateTimeUtc' and the y_column
    y_column : str
        Column name to plot on y axis
    
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

    fig.show()
