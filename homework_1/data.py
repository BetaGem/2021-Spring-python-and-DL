# get data from website

import requests
import json
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin

# packages used for plotting
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO
import base64

AppKey = "5j1znBVAsnSf5xQyNQyq"
choices = {'0':'aqi','1':'pm2_5','2':'pm10','3':'co','4':'no2','5':'o3','7':'so2'}
Title = {'0':'AQI','1':'PM2.5','2':'PM10','3':'CO','4':'NO_2','5':'O_3','7':'SO_2'}
# color range, reference: Ambient air quality standards GB 3095-2012
clim = [[0,150],[0,100],[0,200],[0,2],[0,80],[0,150],[0,0],[0,40]]

class PlotFromURL:
    
    def __init__(self,url):
        self.url = url
    
    def update_local_file(self):
        '''download latest json file from www.pm25.in'''
        
        flag = 1
        count = 0
        session = requests.Session()
        while(flag and count < 100):
            # try 100 times until succeed
            r = session.get(self.url+"api/querys/aqi_ranking.json?token="+AppKey)
            hjson = json.loads(r.text)
            try:
                temp = hjson[0]
                flag = 0    # success!
                a = json.dumps(hjson)
                # avoid json file being overwritten
                with open("data.json",'w') as f:
                    f.write(a)
            
            except KeyError:
                print('failed',end=' ')
                count += 1     
        return 'Update failed'
    
    def local_data(self,city,pollutant):
        '''get air quality data from local file'''
        
        # hanzi to pinyin
        with open("data.json",'r+') as f:
            content = f.read()
            js = json.loads(content)
            
            if all(alpha not in js[0]['area'] for alpha in ['a','e','i','o','u']):      
                for i in range(len(js)):
                    pinyin = lazy_pinyin(js[i]['area'])
                    st=''
                    for j in range(len(pinyin)):
                        st += pinyin[j]
                    js[i]['area'] = st
                    
                a = json.dumps(js)
                f.seek(0)
                f.truncate()
                f.write(a)
                
        # Read data from data.json
        with open("data.json",'r') as f:
            for i in range(len(js)):
                if js[i]['area'] == city:
                    print(str(i),end=' ')
                    return js[i][choices[pollutant]], js[i]['time_point']
                
            print("failed:",city)
            return None,None
            
    def plotmap(self,latitude,longitude,value,size,pollutant,
                #boundary_x,boundary_y
               ):
        '''plot air quality map to html'''
        
        # Set unit
        if pollutant == '3':
            unit = "(mg/m^3)"
        elif pollutant == '0':
            unit = ''
        else:
            unit = "(\mu g/m^3)"
               
        fig = Figure()
        ax = fig.add_subplot(1,1,1)
        sc = ax.scatter(longitude,latitude,
                        c=value,s=size,
                        cmap='jet',alpha=0.7,
                        vmin=clim[int(pollutant)][0],vmax=clim[int(pollutant)][1])
        # add boundary
        # ax.plot(boundary_x,boundary_y)
        
        # Some additional features
        fig.colorbar(sc)
        fig.set_size_inches(8,5)
        fig.tight_layout(pad=2)
        ax.set_title(r"$"+Title[pollutant]+"\ map\ of\ major\ Chinese\ cities\ "+unit+"$")
        ax.grid(True)
        ax.set_xlim([70,136]) 
        ax.set_ylim([19,54])
        ax.set_xlabel(r"$longitude(\degree E)$")
        ax.set_ylabel(r"$latitude(\degree N)$")
        ax.text(x=71,y=20,s="*Smaller dots represent data > 1 day ago",
                fontdict=dict(fontsize=8))
        
        # Convert plot to PNG image
        pngImage = BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
        return pngImageB64String