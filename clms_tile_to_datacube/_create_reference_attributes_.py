def create_ref_attributes(croptype, variables, year_overlap):
        
        


        lcs_eo4bkdata = variables
        
        
        if croptype in ('Soybean', 'Coffee', 'Soybean-maize', 'Rice', 'Cotton'):
                
                # CONAB
                ref_glb_attributes = {f'lcs_{year_overlap}':{'acknowledgement': 'A Companhia Nacional de Abastecimento (CONAB)',
                          'PID': 'https://www.conab.gov.br/',
                          'How to cite': 'CONAB Companhia Nacional de Abastecimento. Portal de Informações Agropecuárias, Mapeamentos, Available online: https://portaldeinformacoes.conab.gov.br/mapeamentos-agricolas-downloads.html',
                          'Download_link':'https://portaldeinformacoes.conab.gov.br/mapeamentos-agricolas-downloads.html',
                          'Detailed_description':'None available'}}
                          
                ref_perm_attr = {'point_id':{'long_name':'Point Identification',
                                                'description':'ID of the CONAB field',
                                                'value_origin':'This field is defined by CONAB',
                                                'original_name':'point_id'}}

        if croptype in ('Fruit_and_nut', 'Oil_palm'):

                ref_glb_attributes = {f'lcs_{year_overlap}':{'acknowledgement': 'MapBiomas Brazil',
                          'PID': 'https://brasil.mapbiomas.org/',
                          'How to cite': 'MapBiomas Project - Collection 9 of the Annual Land Use Land Cover Maps of Brazil, accessed on 19-11-2024 through the link: https://brasil.mapbiomas.org/',
                          'Download_link':'https://brasil.mapbiomas.org/',
                          'Detailed_description':'https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2025/02/ATBD-Collection-9-versao2-v2.pdf'}}
                          
                ref_perm_attr = {'point_id':{'long_name':'Point Identification',
                                                'description':'ID of the MapBiomas field',
                                                'value_origin':'This field is defined by MapBiomas',
                                                'original_name':'point_id'}}

        # Core attribute dictionary
        ref_core_dict = {
                'point_id': {}

        }

        perm_list = ['point_id']


        # Update permanent attributes
        for attr in perm_list:
                try:
                        ref_core_dict[attr] = ref_perm_attr[attr].copy()
                        ref_core_dict[attr].update(ref_glb_attributes[f'lcs_{year_overlap}'])
                except KeyError:
                        pass
        return ref_core_dict