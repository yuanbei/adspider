
# -*- coding: utf-8 -*-

# SQL constants for ads_analyser.py


SQL_GET_ALL_ADS_TARGET_DOMAIN = '''
                                select distinct ads_target_domain from AdsReferGraph
                                '''
SQL_GET_SUM_OF_ADS_TARGET_BY_DOMAIN = '''
                                select count(*)
                                from AdsReferGraph
                                where ads_target_domain =%(domain)s
                                '''
SQL_GET_SUM_OF_ADS_TARGET_BY_DOMAIN_AND_REFER_COUNT = '''
                                select count(*)
                                from AdsReferGraph
                                where ads_target_domain =%(domain)s and refer_count > %(count)s
                                '''
SQL_GET_ALL_ADS_HOST = '''
                                select distinct ads_host from AdsProfile
                       '''
SQL_GET_DS_PROFILE_GROUP = '''
                                select *
                                from AdsProfile
                                where ads_host = %(ads_host)s and ads_target_domain = %(ads_target_domain)s
                       '''
