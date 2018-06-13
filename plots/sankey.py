import plotly
from plots.data import get_data, get_interval_data


def plot(interval): # -1 = end to end plot

    data = get_data() if interval == -1 else get_interval_data(interval)

    data_trace = dict(
        type='sankey',
        domain = dict(
            x =  [0,1],
            y =  [0,1]
        ),
        orientation = "h",
        valueformat = ".0f",
        node = dict(
            pad = 10,
            thickness = 30,
            line = dict(
                color = "black",
                width = 0.5
            ),
            label = data['node']['label'],
            color = data['node']['color']
        ),
        link = dict(
            source = data['link']['source'],
            target = data['link']['target'],
            value = data['link']['value']
        )
    )

    layout =  dict(
        title = "",
        height = 772,
        width = 950,
        plot_bgcolor = 'rgb(245,245,245)',
        paper_bgcolor = 'rgb(245,245,245)',
        font = dict(
            size = 10
        ),    
    )


    fig = dict(data=[data_trace], layout=layout)

    config = {
        'displayModeBar': False,
        'showLink': False
    }

    return plotly.offline.plot(fig, validate=False, config=config, include_plotlyjs=False, output_type='div')
