""" see ~/work/w51/alma/singledish/ """ 
from astroquery.eso import Eso

rslt = Eso.query_apex_quicklooks(project_id='098.C-0421(A)', cache=False)
print(rslt)

Eso.cache_location='/Volumes/passport/w51-apex/raw/'
Eso.retrieve_data(rslt['Product ID'])
