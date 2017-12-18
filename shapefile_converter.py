import pandas as pd
import pyproj
import shapefile

class get_shape_file():
    def __init__(self, file_path):
        self.file_path = file_path

    def get_shapes_coord(self):
        """Returns shape x and y coordinates from shapefile"""
        """works with any shapefile type"""
        sf = shapefile.Reader(self.file_path)
        xpts = [[x[0] for x in a.__geo_interface__['coordinates'][0]] 
                 for a in sf.iterShapes()]
        ypts = [[x[1] for x in a.__geo_interface__['coordinates'][0]] 
                 for a in sf.iterShapes()]
        self.xpts = xpts
        self.ypts = ypts

    def xy_to_latlon(self):
        """Converts polygon xy coordinates to latitude longitude"""
        NYSP1983 = pyproj.Proj(init="ESRI:102718", preserve_units=True)
        all_poly_lats = [[(NYSP1983(x[0],x[1], inverse=True))[1] 
                          for x in zip(a[0],a[1])] 
                          for a in zip(self.xpts, self.ypts)]
        all_poly_lons = [[(NYSP1983(x[0],x[1], inverse=True))[0] 
                          for x in zip(a[0],a[1])] 
                          for a in zip(self.xpts, self.ypts)]
        self.ypts = all_poly_lats
        self.xpts = all_poly_lons

    def latlon_to_xy(self):
        """Converts polygon latitude and longitude to xy coordinates"""
        NYSP1983 = pyproj.Proj(init="ESRI:102718", preserve_units=True)
        all_poly_ypts = [[(NYSP1983(x[0],x[1]))[1]
                          for x in zip(a[0],a[1])]
                          for a in zip(self.xpts, self.ypts)]
        all_poly_xpts = [[(NYSP1983(x[0],x[1]))[0]
                          for x in zip(a[0],a[1])]
                          for a in zip(self.xpts, self.ypts)]
        self.ypts = all_poly_ypts
        self.xpts = all_poly_xpts
        
    def create_block_df(self):
        """Creates dataframe with block, borough and x and y coordinates"""
        sf = shapefile.Reader(self.file_path)
        blocks = [a[1] for a in sf.iterRecords()]
        boro = [a[0] for a in sf.iterRecords()]
        #xpts, ypts = get_shapes_coord(file_path)
        #xpts, ypts = xy_to_latlon(xpts, ypts) #make optional for if want to convert to latlon
        df = pd.DataFrame({'block':blocks, 
                           'boro':boro, 
                           'xpts':self.xpts, 
                           'ypts':self.ypts})
        self.df = df




