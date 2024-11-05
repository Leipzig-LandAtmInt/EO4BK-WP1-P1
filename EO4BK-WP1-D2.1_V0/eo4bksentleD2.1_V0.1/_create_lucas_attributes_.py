def create_lucas_attributes(variables):
        
        
        lcs_eo4bkdata = variables
        lcs_glb_attributes = {'lcs_2018':{'acknowledgement': 'European Commission, Joint Research Centre (JRC) (2018)',
                          'PID': 'http://data.europa.eu/89h/cfe66a0c-bdee-4074-96e1-a2f7030b9515',
                          'How to cite': 'European Commission, Joint Research Centre (JRC) (2018): LUCAS Copernicus 2018. European Commission, Joint Research Centre (JRC) [Dataset] PID: http://data.europa.eu/89h/cfe66a0c-bdee-4074-96e1-a2f7030b9515',
                          'Download_link':'https://data.jrc.ec.europa.eu/dataset/cfe66a0c-bdee-4074-96e1-a2f7030b9515#dataaccess',
                          'Detailed_description':'https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/LUCAS/LUCAS_harmonised/3_supporting/LUCAS2018-C1-Instructions.pdf'},
                        'lcs_2022':{'acknowledgement': 'European Commission, Joint Research Centre (JRC) (2023)',
                          'PID': 'http://data.europa.eu/89h/e3fe3cd0-44db-470e-8769-172a8b9e8874',
                          'How to cite': 'European Commission, Joint Research Centre (JRC) (2023): LUCAS Copernicus 2022. European Commission, Joint Research Centre (JRC) [Dataset] PID: http://data.europa.eu/89h/e3fe3cd0-44db-470e-8769-172a8b9e8874',
                          'Download_link':'https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/LUCAS/LUCAS_2022_Copernicus/l2022_survey_cop_radpoly_attr.gpkg',
                          'Detailed_description':'https://ec.europa.eu/eurostat/documents/205002/13686460/C1-LUCAS-2022.pdf'}}
        
        lcs_perm_attr = {'point_id':{'long_name':'Point Identification',
                                                'description':'ID of the LUCAS theoretical point',
                                                'value_origin':'This field is defined by LUCAS',
                                                'original_name':'point_id'}}

        # Core attribute dictionary
        lcs_core_dict = {
                'point_id': {}

        }

        perm_list = ['point_id']


        # Update permanent attributes
        for attr in perm_list:
                try:
                        lcs_core_dict[attr] = lcs_perm_attr[attr].copy()
                        lcs_core_dict[attr].update(lcs_glb_attributes['lcs_2018'])
                except KeyError:
                        pass
        return lcs_core_dict
