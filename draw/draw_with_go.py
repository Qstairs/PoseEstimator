import numpy as np
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

RIGHT_INDX = [1,2,3,7,9,11,13,15,17,19,21,23,25,27,29,31]

def enable_plotly_in_cell():
    import IPython
    from plotly.offline import init_notebook_mode
    display(IPython.core.display.HTML('''
            <script src="/static/components/requirejs/require.js"></script>
    '''))
    init_notebook_mode( connected=False )

def make_surface_graph( dict_ruin ,risk_rate_range ,graph_title ) :

    sliders = [dict(
          steps = [dict( method = 'animate'
                       , args = [ [ f'{ risk_rate :.0%}' ]
                                , dict( mode = 'immediate'
                                      , frame = dict( duration=100 ,redraw=False )
                                      , transition = dict( duration=0 ) ) ]
                       , label=f'{ risk_rate :.0%}' ) for risk_rate in risk_rate_range ]
        , transition = dict( duration = 0 )
        , x = 0
        , y = 0
        , currentvalue = dict( font = dict(size=12)
                             , prefix = ''
                             , visible = True
                             , xanchor = 'center' )
        , len=1.0 )]

    updatemenus = [dict(
          type = 'buttons'
        , showactive = False
        , y = 1
        , x = -0.05
        , xanchor = 'right'
        , yanchor = 'top'
        , pad = dict( t=0, r=10 )
        , buttons = [dict(
              label = 'Play'
            , method = 'animate'
            , args = [ None
                     , dict( frame = dict( duration=100 , redraw=True )
                           , transition = dict( duration=0 )
                           , fromcurrent = True
                           , mode = 'immediate' )] )] )]

    layout = go.Layout( title         = graph_title
                      , autosize      = False
                      , paper_bgcolor = "#000"
                      , width         = 1000
                      , height        = 800
                      , scene = dict(
                            aspectmode = "manual"
                          , aspectratio = dict(x=1 ,y=1 ,z=0.5)
                          , xaxis = dict(color="#fff" ,linecolor="#fff" ,gridcolor="#eee" ,title="リスクリワード比率")
                          , yaxis = dict(color="#fff" ,linecolor="#fff" ,gridcolor="#eee" ,title="勝率（％）")
                          , zaxis = dict(color="#fff" ,linecolor="#fff" ,gridcolor="#eee" ,range=[-1,101] ,title="破産の確率（％）")
                          , camera = dict(eye=dict(x=1.5 ,y=.9 ,z=.7)) )
                      , font = dict(color="#fff")
                      , updatemenus = updatemenus
                      , sliders = sliders )

    z1 = dict_ruin
    # data = [ go.Surface( z = z1[ 0.02 ]
    #                    , y = z1['columns']
    #                    , x = z1['index']
    #                    , cmin=0 ,cmax=100
    #                    , colorscale = "Jet"
    #                    , colorbar   = dict(lenmode='fraction' ,len=0.5 ,x=1 ,y=0.3 )
    #                    , contours   = dict(x=dict(color="#fff") ,y=dict(color="#fff") ,z=dict(color="#fff")) ) ]

    # frames = []
    # for risk_rate in risk_rate_range :
    #     frames.append( dict( data = [ go.Surface( z = z1[ risk_rate ]
    #                                             , y = z1['columns']
    #                                             , x = z1['index'] ) ]
    #                        , name = f'{ risk_rate :.0%}' ) )
    # data = [ go.Scatter3d( z = z1["x"]
    #                    , y = z1["y"]
    #                    , x = z1["z"]
    #                    , cmin=0 ,cmax=100
    #                    , colorscale = "Jet"
    #                    , colorbar   = dict(lenmode='fraction' ,len=0.5 ,x=1 ,y=0.3 )
    #                    , contours   = dict(x=dict(color="#fff") ,y=dict(color="#fff") ,z=dict(color="#fff")) ) ]

    # frames = []
    # for risk_rate in range(100) :
    #     frames.append( dict( data = [ go.Surface( z = z1["x"][risk_rate]
    #                                             , y = z1["y"][risk_rate]
    #                                             , x = z1["z"][risk_rate] ) ]
    #                        , name = f'{ risk_rate :.0%}' ) )

    # enable_plotly_in_cell()
    # fig = dict( data=data ,layout=layout ,frames=frames )

    fig = go.Figure(data=[go.Scatter3d(z = z1["x"]
                       , y = z1["y"]
                       , x = z1["z"],mode='markers',marker=dict(
        size=5
        ,color = z1["x"]
        ,colorscale = 'Viridis'
        ,symbol= [ 'circle' for _ in z1["x"] ]
    ))])
    # plotly.offline.iplot( fig )
    pio.write_html(fig, f"{graph_title}.html",)
    pio.write_image(fig, f"{graph_title}.png")

def make_dict_ruin( win_range ,rr_range ,risk_rate_range ,funds ,ruin_line ,rate_amount='amount') :
    dict_ruin = { 'index' : rr_range
                , 'columns' : [ f'{ win * 100 }' for win in win_range] }
    for risk_rate in risk_rate_range :
        raw = pd.DataFrame()
        for win in win_range :
            for rr in rr_range :
                ruin_rate = rr
                # if rate_amount=='rate' :
                #     ruin_rate = 0.5
                # elif rate_amount=='amount' :
                #     ruin_rate = ruin_fixed_amount( win ,rr ,risk_rate ).calc()
                # raw.loc[ rr ,f'{ win :.0%}' ] = f'{ round( ruin_rate * 100 ,2 ) }'
                print(rr, win)
                raw.loc[ rr ,f'{ win :.0%}' ] = f'{win*100}'
        dict_ruin[ risk_rate ] = raw.T.values
    return dict_ruin

if __name__=="__main__" :
    win_range = np.arange(0.3 ,0.62 ,0.02)
    rr_range = np.arange(0.4 ,3.1 ,0.1)
    risk_rate_range = np.arange(0.02 ,0.08 ,0.02)
    funds = 1000000
    ruin_line = 200000

    dict_ruin = make_dict_ruin( win_range ,rr_range ,risk_rate_range ,funds ,ruin_line ,rate_amount='rate')
    print(dict_ruin)

    dict_ruin = {}
    # for i in range(100):
    #     dict_ruin[i] = {
    #         "x":i,
    #         "y":i,
    #         "z":i
    #     }
    
    dict_ruin = {
        "x":[i for i in range(100)],
        "y":[i for i in range(100)],
        "z":[i for i in range(100)]
    }
    make_surface_graph(dict_ruin, risk_rate_range, "graph_title")

# exit()

# def load_landmark_data(path):

#     data = {"x":[],"y":[],"z":[],"frame":[], "size":[], "right_left":[], "group":[]}
#     with open(path, "r") as f:
#         for line in f.readlines():
#             vals = line.rstrip().split(",")

#             frame_number = int(vals[0])

#             pose_cnt = 0
#             for idx, val in enumerate(vals[1:]):
#             # for idx, val in enumerate(vals[24*3+1:25*3+1]):
#                 if idx % 3 == 2:
#                     key = "x"
#                     val = -float(val)
#                     data["frame"].append(frame_number)
#                     data["size"].append(1)
#                     if pose_cnt in RIGHT_INDX:
#                         data["right_left"].append("right")
#                     else:
#                         data["right_left"].append("left")
                    
#                     # groups = []
#                     # for _idx, cmb in enumerate(POSE_CONNECTIONS):
#                     #     if pose_cnt in cmb:
#                     #         data["group"].append(_idx)
#                     #         break
#                     data["group"].append(idx)
#                     pose_cnt += 1


#                 elif idx % 3 == 0:
#                     key = "y"
#                     val = float(val)
#                 else:
#                     key = "z"
#                     val = -float(val)

#                 data[key].append(val)

#                 # if idx % 3 == 2:
#                 #     break

#     return data


# path = "./outputs/home3_world.csv"
# landmark_data = load_landmark_data(path)

# data = [
#     go.Scatter(
#         x=landmark_data["x"], y=landmark_data["y"], name="name",
#         mode='lines+markers')
# ]
# fig = go.Figure(data=data)
# # fig.show()
# def save(fig, config, save_name):
#     pio.orca.config.executable = '/Applications/orca.app/Contents/MacOS/orca'
#     pio.write_html(fig, f"{save_name}.html", config=config,)
#     pio.write_image(fig, f"{save_name}.png")
# save(fig=fig, config=None, save_name='all_plot')
