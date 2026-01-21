import numpy as np
import plotly.graph_objects as go
import scipy.stats as stats



def plot_qq_residuals(residuals: list[float], title: str = "Q-Q Plot"):
    (osm, osr), (slope, intercept, _) = stats.probplot(residuals, dist="norm")
    line_x = np.array([osm.min(), osm.max()])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=osm,
            y=osr,
            mode="markers",
            marker={
                "size": 6, "color": "black", "opacity": 0.6, "line": {"width": 0}
            },
            name="Residuals",
            showlegend=False
        )
    )

    fig.add_trace(
        go.Scatter(
            x=line_x,
            y=(slope * line_x + intercept),
            mode="lines",
            line={"color": "red", "width": 2, "dash": "solid"},
            name="Theoretical",
            showlegend=False
        )
    )

    font = {"family": "Times New Roman", "color": "black"}
    axis_layout = {
        "title_font": {"size": 12, **font},
        "tickfont": {"size": 11, **font},
        "showline": True,
        "linewidth": 1,
        "linecolor": "black",
        "mirror": True,
        "showgrid": False,
        "zeroline": False,
    }
    fig.update_layout(
        title={
            "text": title,
            "font": {"size": 14, **font},
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis={"title": "Theoretical Quantiles", **axis_layout},
        yaxis={"title": "Sample Quantiles", **axis_layout},
        plot_bgcolor="white",
        paper_bgcolor="white",
        width=600,
        height=500,
        margin={"l": 80, "r": 40, "t": 60, "b": 80},
    )

    return fig
