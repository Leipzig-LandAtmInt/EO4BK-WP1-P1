import geopandas as gpd

centroid_dict = {}
def create_centroid_list(crop, gpkg_dict):
    centroid_dict[crop] = {}
    centroid_dict[crop]['Centroid'] = gpkg_dict[crop].centroid
    centroid_dict[crop]['Index'] = gpkg_dict[crop]['point_id']
    centroid_dict[crop]['Centroid'] = centroid_dict[crop]['Centroid'].to_crs(4326)    
    return centroid_dict
