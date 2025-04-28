def create_ref_attributes(reference_source,  year_attr):
        
        
        if reference_source == "LUCAS":
                
                ref_glb_attributes = {'ref_2018':{'acknowledgement': 'European Commission, Joint Research Centre (JRC) (2018)',
                                        'PID': 'http://data.europa.eu/89h/cfe66a0c-bdee-4074-96e1-a2f7030b9515',
                                        'How to cite': 'European Commission, Joint Research Centre (JRC) (2018): LUCAS Copernicus 2018. European Commission, Joint Research Centre (JRC) [Dataset] PID: http://data.europa.eu/89h/cfe66a0c-bdee-4074-96e1-a2f7030b9515',
                                        'Download_link':'https://data.jrc.ec.europa.eu/dataset/cfe66a0c-bdee-4074-96e1-a2f7030b9515#dataaccess',
                                        'Detailed_description':'https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/LUCAS/LUCAS_harmonised/3_supporting/LUCAS2018-C1-Instructions.pdf'},
                                        
                                        'ref_2022':{'acknowledgement': 'European Commission, Joint Research Centre (JRC) (2023)',
                                        'PID': 'http://data.europa.eu/89h/e3fe3cd0-44db-470e-8769-172a8b9e8874',
                                        'How to cite': 'European Commission, Joint Research Centre (JRC) (2023): LUCAS Copernicus 2022. European Commission, Joint Research Centre (JRC) [Dataset] PID: http://data.europa.eu/89h/e3fe3cd0-44db-470e-8769-172a8b9e8874',
                                        'Download_link':'https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/LUCAS/LUCAS_2022_Copernicus/l2022_survey_cop_radpoly_attr.gpkg',
                                        'Detailed_description':'https://ec.europa.eu/eurostat/documents/205002/13686460/C1-LUCAS-2022.pdf'}}
        
                ref_perm_attr = {'point_id':{'long_name':'Point Identification',
                                                'description':'ID of the LUCAS theoretical point',
                                                'value_origin':'This field is defined by LUCAS',
                                                'original_name':'point_id'}}


        
        if reference_source == "CONAB":

                ref_glb_attributes = {f'ref_{year_attr}':{'acknowledgement': 'A Companhia Nacional de Abastecimento (CONAB)',
                          'PID': 'https://www.conab.gov.br/',
                          'How to cite': 'CONAB Companhia Nacional de Abastecimento. Portal de Informações Agropecuárias, Mapeamentos, Available online: https://portaldeinformacoes.conab.gov.br/mapeamentos-agricolas-downloads.html',
                          'Download_link':'https://portaldeinformacoes.conab.gov.br/mapeamentos-agricolas-downloads.html',
                          'Detailed_description':'None available'}
                          }

        
                ref_perm_attr = {
                        'point_id':{'long_name':'Point Identification',
                        'description':'ID of the CONAB shapefile',
                        'value_origin':'This field is defined by CONAB',
                        'original_name':'point_id'}
                        }
                
        if reference_source == "LEM":

                ref_glb_attributes = {f'ref_{year_attr}': {'acknowledgement': 'LEM Benchmark Database (2018)',
                'PID': 'https://doi.org/10.5194/isprs-archives-XLII-1-387-2018, 2018',
                'How to cite': 'Sanches, I. D., Feitosa, R. Q., Achanccaray, P., Montibeller, B., Luiz, A. J. B., Soares, M. D., Prudente, V. H. R., Vieira, D. C., and Maurano, L. E. P.: LEM BENCHMARK DATABASE FOR TROPICAL AGRICULTURAL REMOTE SENSING APPLICATION, Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci., XLII-1, 387–392, https://doi.org/10.5194/isprs-archives-XLII-1-387-2018, 2018.',
                'Download_link': 'https://github.com/lem-project',
                'Detailed_description': 'https://doi.org/10.5194/isprs-archives-XLII-1-387-2018, 2018.'}
                }
                
                ref_perm_attr = {
                        'point_id': {'long_name': 'Point Identification',
                        'description': 'ID of the LEM field',
                        'value_origin': 'This field is defined by LEM',
                        'original_name': 'point_id'}
                        }
        
        if reference_source == "LEMplus":

                ref_glb_attributes = {
                        f'ref_{year_attr}': {
                        'acknowledgement': 'LEM+ dataset (2020)',
                        'PID': 'https://doi.org/10.1016/j.dib.2020.106553',
                        'How to cite': 'Oldoni, L.V., Sanches, I.D.A., Picoli, M.C.A., Covre, R.M. and Fronza, J.G., 2020. LEM+ dataset: For agricultural remote sensing applications. Data in Brief, 33, p.106553.',
                        'Download_link': 'http://dx.doi.org/10.17632/vz6d7tw87f.1',
                        'Detailed_description': 'Oldoni, L.V., Sanches, I.D.A., Picoli, M.C.A., Covre, R.M. and Fronza, J.G., 2020. LEM+ dataset: For agricultural remote sensing applications. Data in Brief, 33, p.106553.'
                        }
                }

                ref_perm_attr = {
                        'point_id': {
                        'long_name': 'Point Identification',
                        'description': 'ID of the LEM+ field',
                        'value_origin': 'This field is defined by LEM+',
                        'original_name': 'point_id'
                        }
                }    


        if reference_source == "MapBiomasDirect":

                ref_glb_attributes = {
                        f'ref_{year_attr}': {
                                'acknowledgement': 'MapBiomas Brazil',
                                'PID': 'https://brasil.mapbiomas.org/',
                                'How to cite': 'MapBiomas Project - Collection 9 of the Annual Land Use Land Cover Maps of Brazil, accessed on 19-11-2024 through the link: https://brasil.mapbiomas.org/',
                                'Download_link': 'https://brasil.mapbiomas.org/',
                                'Detailed_description': 'https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2025/02/ATBD-Collection-9-versao2-v2.pdf'
                                }
                        }

                ref_perm_attr = {
                        'point_id': {
                        'long_name': 'Point Identification',
                        'description': 'ID of the MapBiomas field',
                        'value_origin': 'This field is defined by MapBiomas',
                        'original_name': 'point_id'
                        }
                }

        if reference_source == "TerraClass":

                ref_glb_attributes = {
                        f'ref_{year_attr}': {
                        'acknowledgement': 'TerraClass',
                        'PID': 'https://www.terraclass.gov.br/',
                        'How to cite': 'INPE, 2023. TerraClass Land Use and Land Cover Data, 2018, 2020, 2022. National Institute for Space Research. Available at: https://terrclass.gov.br (Accessed: 25 February 2025).',
                        'Download_link': 'https://www.terraclass.gov.br',
                        'Detailed_description': 'None available'
                        }
                }

                ref_perm_attr = {
                        'point_id': {
                        'long_name': 'Point Identification',
                        'description': 'ID of the TerraClass field',
                        'value_origin': 'This field is defined by TerraClass',
                        'original_name': 'point_id'
                        }
                }                


        # if croptype in ('Soybean', 'Coffee', 'Soybean-maize', 'Rice', 'Cotton'):
                
        #         # CONAB
        #         ref_glb_attributes = {f'lcs_{year_overlap}':{'acknowledgement': 'A Companhia Nacional de Abastecimento (CONAB)',
        #                   'PID': 'https://www.conab.gov.br/',
        #                   'How to cite': 'CONAB Companhia Nacional de Abastecimento. Portal de Informações Agropecuárias, Mapeamentos, Available online: https://portaldeinformacoes.conab.gov.br/mapeamentos-agricolas-downloads.html',
        #                   'Download_link':'https://portaldeinformacoes.conab.gov.br/mapeamentos-agricolas-downloads.html',
        #                   'Detailed_description':'None available'}}
                          
        #         ref_perm_attr = {'point_id':{'long_name':'Point Identification',
        #                                         'description':'ID of the CONAB field',
        #                                         'value_origin':'This field is defined by CONAB',
        #                                         'original_name':'point_id'}}

        # if croptype in ('Fruit_and_nut', 'Oil_palm'):

        #         ref_glb_attributes = {f'lcs_{year_overlap}':{'acknowledgement': 'MapBiomas Brazil',
        #                   'PID': 'https://brasil.mapbiomas.org/',
        #                   'How to cite': 'MapBiomas Project - Collection 9 of the Annual Land Use Land Cover Maps of Brazil, accessed on 19-11-2024 through the link: https://brasil.mapbiomas.org/',
        #                   'Download_link':'https://brasil.mapbiomas.org/',
        #                   'Detailed_description':'https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2025/02/ATBD-Collection-9-versao2-v2.pdf'}}
                          
        #         ref_perm_attr = {'point_id':{'long_name':'Point Identification',
        #                                         'description':'ID of the MapBiomas field',
        #                                         'value_origin':'This field is defined by MapBiomas',
        #                                         'original_name':'point_id'}}

        # Core attribute dictionary
        ref_core_dict = {
                'point_id': {}

        }

        perm_list = ['point_id']


        # Update permanent attributes
        for attr in perm_list:
                try:
                        ref_core_dict[attr] = ref_perm_attr[attr].copy()
                        ref_core_dict[attr].update(ref_glb_attributes[f'ref_{year_attr}'])
                except KeyError:
                        pass
        return ref_core_dict