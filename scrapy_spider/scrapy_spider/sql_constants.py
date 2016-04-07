# -*- coding: utf-8 -*-

# SQL constants for piplines.py

INSERT_ITEM_SQLITE = '''INSERT INTO AdsProfile
                     (ads_target_url,
                      ads_content_url,
                      ads_present_mode,
                      ads_host,
                      ads_target_domain,
                      ads_host_domain) VALUES(?,?,?,?,?,?)'''
INSERT_ITEM_MYSQL = '''INSERT INTO AdsProfile
                           (ads_target_url,
                            ads_content_url,
                            ads_present_mode,
                            ads_host,
                            ads_target_domain,
                            ads_host_domain)
                            VALUES(%(ads_target_url)s,
                                   %(ads_content_url)s,
                                   %(ads_present_mode)s,
                                   %(ads_host)s,
                                   %(ads_target_domain)s,
                                   %(ads_host_domain)s)'''
CREATE_ADS_PROFILE_TABLE_SQLITE = '''CREATE TABLE IF NOT EXISTS AdsProfile (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  ads_target_url TEXT,
                                  ads_content_url TEXT,
                                  ads_present_mode TEXT,
                                  ads_host TEXT,
                                  ads_target_domain TEXT,
                                  ads_host_domain TEXT)
                                  '''
CREATE_ADS_PROFILE_TABLE_MYSQL = '''create table if not exists AdsProfile (
                                  id int(16) not null primary key auto_increment,
                                  ads_target_url text,
                                  ads_content_url text,
                                  ads_present_mode text,
                                  ads_host text,
                                  ads_target_domain text,
                                  ads_host_domain text)
                                  default charset utf8 collate utf8_unicode_ci
                                  '''
CREATE_ADS_REFER_GRAPH_MYSQL = '''create table if not exists AdsReferGraph (
                                  id int(16) not null primary key auto_increment,
                                  ads_host_domain text,
                                  ads_target_domain text,
                                  refer_count int(16),
                                  is_ads tinyint)
                                  default charset utf8 collate utf8_unicode_ci
                                  '''
CREATE_TRIGGER_MYSQL = '''
                          drop trigger if exists update_adsrefergraph;
                          create trigger update_adsrefergraph after insert
                          on AdsProfile
                          FOR EACH ROW
                          begin
                          set @count = (select count(*) from AdsReferGraph where ads_target_domain = new.ads_target_domain and ads_host_domain = new.ads_host_domain);
                          if @count = 0 then
                          insert into AdsReferGraph(ads_host_domain,ads_target_domain,refer_count, is_ads) values(new.ads_host_domain,new.ads_target_domain,1,0);
                          elseif @count>0 then
                          update AdsReferGraph set refer_count = refer_count+1 where ads_target_domain = new.ads_target_domain and ads_host_domain = new.ads_host_domain;
                          end if;
                          end
                          '''
