import pandas                  as pd
import numpy                   as np
import seaborn                 as sns
import statsmodels.api         as sm
import statsmodels.formula.api as smf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import folium
import geojsoncontour
import branca
from folium import plugins
from IPython.display import display
import scipy as sp
import scipy.ndimage
import warnings

warnings.filterwarnings('ignore')
# This statement allow to display plot without asking to 
#%matplotlib inline
# always make it pretty 
matplotlib.use('agg')
plt.style.use('ggplot')

def prepareData(dataPath,departamento,ciudad,sexo,edad,mes,dia,hora):
    weights = pd.read_csv('Data_Parms/'+dataPath+'.csv_Params.csv',sep=',')
    map_cat = pd.read_csv('Data_encoder/'+dataPath+'.csv_encoder_info.csv',sep=',')
    geo_loc = pd.read_csv('Data_por_barrio_V2/'+departamento+"-"+ciudad+' (CT)'+'.csv',sep=',')
    #Transformed variables
    x = map_to_vector(sexo,edad,mes,dia,hora,map_cat)
    #Compute probabilites
    prob = compute_prob(weights,x)
    df_plot = prob.merge(geo_loc,how='inner',on='Barrio')
    df_plot.dropna(subset=['long'],inplace=True)
    return df_plot


def compute_prob(weights,x):
    W = np.array(weights.iloc[:,1:])
    dot_exp = np.matmul(W,x)
    df_prob = pd.DataFrame(columns=['Barrio','Prob'])
    df_prob['Prob'] = 1/(1+np.exp(-dot_exp))
    df_prob['Barrio'] = weights['Barrio']
    return df_prob

def map_to_vector(sexo,edad,mes,dia,hora, map_cat):
    m_sexo = map_cat[map_cat['Sexo']==sexo]['Cod-Sexo'].iloc[0]
    x = np.array([edad,m_sexo,mes,dia,hora])
    return x

def plotDataHTML(df_plot,departamento,ciudad):
    minlat = np.min(df_plot['lat'])
    maxlat = np.max(df_plot['lat'])
    minlon = np.min(df_plot['long'])
    maxlon = np.max(df_plot['long'])

    lon = df_plot['long']
    lat = df_plot['lat']
    meanlon=np.mean(lon)
    meanlat=np.mean(lat)
    stdlon=np.std(lon)
    stdlat=np.std(lat)
    
    pro = df_plot['Prob']
    ngrid_lon = 200
    ngrid_lat = 200

    yi = np.linspace(minlat, maxlat, ngrid_lat)
    xi = np.linspace(minlon, maxlon, ngrid_lon)


    triang = tri.Triangulation(lon, lat)
    interpolator = tri.LinearTriInterpolator(triang, pro)
    Xi, Yi = np.meshgrid(xi, yi)
    zi = interpolator(Xi, Yi)
    vmin = np.min(pro)
    vmax = np.max(pro)

    sigma = [5, 5]
    z_mesh = sp.ndimage.filters.gaussian_filter(zi, sigma, mode='constant')

    colors = ['blue','royalblue', 'navy','pink',  'mediumpurple',  'darkorchid',  'plum',  'm', 'mediumvioletred', 'palevioletred', 'crimson',
            'magenta','pink','red','yellow','orange', 'brown','green', 'darkgreen']
    levels = len(colors)
    cm     = branca.colormap.LinearColormap(colors, vmin=vmin, vmax=vmax).to_step(levels)

    contf = plt.contourf(Xi, Yi, z_mesh, levels, alpha=0.5, colors=colors, linestyles='None', vmin=vmin, vmax=vmax) 

    geojson = geojsoncontour.contourf_to_geojson(
        contourf=contf,
        min_angle_deg=3.0,
        ndigits=5,
        stroke_width=1,
        fill_opacity=0.1)
    
    geomap = folium.Map(location=[np.mean(lat), np.mean(lon)],zoom_start=12,tiles="OpenStreetMap")

    folium.GeoJson(
        geojson,
        style_function=lambda x: {
            'color':     x['properties']['stroke'],
            'weight':    x['properties']['stroke-width'],
            'fillColor': x['properties']['fill'],
            'opacity':   0.5,
        }).add_to(geomap)

    folium.Circle(
        location=[minlat, minlon],
        radius=100,
        color='crimson',
        fill=True,
        fill_color='crimson').add_to(geomap)

    folium.Circle(
        location=[maxlat, maxlon],
        radius=100,
        color='crimson',
        fill=True,
        fill_color='crimson').add_to(geomap)
    cm.caption = 'Probability'
    geomap.add_child(cm)
    plugins.Fullscreen(position='topright', force_separate_button=True).add_to(geomap)
    geomap.save('Mapa'+departamento+'-'+ciudad+'.html')
    return('Mapa'+departamento+'-'+ciudad+'.html')


#plotDataHTML(prepareData(dataPath,departamento,ciudad,sexo,edad,mes,dia,hora))