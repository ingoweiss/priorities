import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import plotly.io as pio
import plotly.subplots as sp
pio.templates.default = "plotly_white"

from data import Data
# from config import Config

class Graphs:

    @classmethod
    def timeline(cls):

        epics = Data.priorities()
        changes = Data.changes()

        fig = go.Figure()

        for index, change in changes.iterrows():

            if change.at['Category'] in ['Initial', 'Added']:
                marker_sizes = [4, 10]    
            elif (change.at['Category'] == 'Removed'):
                marker_sizes = [10, 4]
            elif (change.at['Date'] == changes['Date'].max()):
                marker_sizes = [4, 10]
            else:
                marker_sizes = [4, 2]

            fig.add_trace(go.Scatter(
                name=change['Epic'],
                x=[change['Previous Date'], change['Date']],
                y=[change['Previous Priority'], change['Current Priority']],
                mode='lines+markers',
                line=dict(
                    color='steelblue',
                    width=0.5+change.at['Impact Score']*0.05
                ),
                marker=dict(
                    size=marker_sizes,
                    opacity=1,
                    line=dict(width=0)
                ),
                customdata=[[change.at['Epic'], change.at['Previous Priority']], [change.at['Epic'], change.at['Current Priority']]],
                hovertemplate="<b>%{customdata[1]}</b>. %{customdata[0]}<extra></extra>",
                showlegend=False
            ))
            if change.at['Category'] in ['Initial', 'Added']:
                fig.add_annotation(
                    x=change.at['Date'],
                    y=change.at['Current Priority'],
                    xanchor="right",
                    yanchor='middle',
                    text="{epic} {priority:02.0f}".format(epic=change.at['Epic'], priority=change.at['Current Priority']),
                    showarrow=False,
                    xshift=-7,
                    yshift=0
                )
            if (change.at['Date'] == changes['Date'].max()) & (change.at['Current Priority'] >= 1):
                fig.add_annotation(
                    x=change.at['Date'],
                    y=change.at['Current Priority'],
                    xanchor="left",
                    yanchor='middle',
                    text="{priority:02.0f} {epic}".format(epic=change.at['Epic'], priority=change.at['Current Priority']),
                    showarrow=False,
                    xshift=7,
                    yshift=0)
        fig.update_yaxes(
            autorange='reversed',
            showgrid=False,
            showticklabels=False,
            zeroline=False
       )
        fig.update_xaxes(
            tickmode = 'array',
            tickvals = epics.index,
            tickformat = '%b %y'
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=0
            ),
            height=600
        )

        graph = dcc.Graph(
            id='timeline',
            figure=fig,
            config=dict(displayModeBar=False)
        )
        return graph
