
# -*- coding: utf-8 -*-

# SQL constants for ads_analyser.py


SQL_GET_ALL_ADS_TARGET_DOMAIN = '''
                                select distinct ads_target_domain from AdsReferGraph
                                '''
SQL_GET_ADS_TARGET_BY_DOMAIN = '''
                                select *
                                from AdsReferGraph
                                where ads_target_domain =%(domain)s
                                '''
SQL_GET_ADS_TARGET_BY_DOMAIN_AND_REFER_COUNT = '''
                                select *
                                from AdsReferGraph
                                where ads_target_domain =%(domain)s and refer_count > %(count)s
                                '''
SQL_SET_ADS_REFER_IS_ADS = '''
                           update AdsReferGraph
                           set is_ads = %(is_ads)s
                           where id = %(id)s
                           '''
SQL_GET_ALL_ADS_REFERS = '''
                           select ads_host, ads_target_url, ads_content_url
                           from AdsProfile
                           where (ads_host_domain, ads_target_domain)
                           in
                           (select ads_host_domain, ads_target_domain
                            from AdsReferGraph
                            where is_ads = 1)
                         '''
