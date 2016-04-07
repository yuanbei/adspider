# coding:utf8


import io
import sys

from pylib import db
from sql_constants import *

reload(sys)
sys.setdefaultencoding('utf8')


class AdsAnalyser(object):

    def __init__(self,
                 dbspec,
                 ads_refer_group_count_threshod,
                 ads_refer_count_threshod,
                 ads_refer_sum_threshod):
        self.conn = None
        self.dbspec = dbspec
        self.ads_refer_group_count_threshod = ads_refer_group_count_threshod
        self.ads_refer_count_threshod = ads_refer_count_threshod
        self.ads_refer_sum_threshod = ads_refer_sum_threshod

    def initialize(self):
        self.conn = db.Connect(self.dbspec)
        assert self.conn is not None

    def finalize(self):
        if self.conn is not None:
            self.conn.Close()
            self.conn = None

    def get_all_ads_target_domains(self):
        assert self.conn is not None
        results = None
        simple_rows_list = []
        if self.conn is not None:
            try:
                results = self.conn.Execute(SQL_GET_ALL_ADS_TARGET_DOMAIN)
            except InconsistentResponses:
                pass
        if results is not None and isinstance(results, db.VirtualTable):
            rows_list = results.GetRows()
            for rows in rows_list:
                simple_rows_list.append(rows[0])
        return simple_rows_list

    def update_all_ads_refer_group(self, ads_target_domain_list):
        ads_refer_group_list = []
        for domain in ads_target_domain_list:
            self.update_ads_refer_group(domain)

    def update_ads_refer_group(self, domain):
        assert self.conn is not None
        self.reset_ads_refer_group(domain)
        try:
            results = self.conn.Execute(SQL_GET_ADS_TARGET_BY_DOMAIN_AND_REFER_COUNT,
                                        {
                                            'domain': domain,
                                            'count': self.ads_refer_count_threshod
                                        })
            ads_refer_sum = len(results.GetRows())
            if ads_refer_sum >= self.ads_refer_group_count_threshod:
                for row in results.GetRows():
                    self.set_ads_refer_record_is_ads(row[0], 1)
        except db.InconsistentResponses:
            pass

    def reset_ads_refer_group(self, domain):
        assert self.conn is not None
        try:
            results = self.conn.Execute(SQL_GET_ADS_TARGET_BY_DOMAIN,
                                        {
                                            'domain': domain
                                        })
            for row in results.GetRows():
                self.set_ads_refer_record_is_ads(row[0], 0)
        except db.InconsistentResponses:
            pass

    def set_ads_refer_record_is_ads(self, record_id, is_ads):
        assert self.conn is not None
        try:
            results = self.conn.Execute(SQL_SET_ADS_REFER_IS_ADS,
                                        {
                                            'id': record_id,
                                            'is_ads': is_ads
                                        })
        except db.InconsistentResponses:
            pass

    def get_all_ads_refers(self):
        ads_refer_rows = []
        assert self.conn is not None
        try:
            results = self.conn.Execute(SQL_GET_ALL_ADS_REFERS)
            ads_refer_rows = results.GetRows()
        except db.InconsistentResponses:
            pass
        return ads_refer_rows

    def generate_ads_refer_graph_dot_file(self):
        ads_refer_rows = []
        sql_str = "select * from AdsReferGraph where is_ads = 1"
        dot_data = "digraph AdsReferGraph{ \n"
        dot_data += "%node_defines%"
        node_label_map = {}
        assert self.conn is not None
        if self.conn is not None:
            try:
                results = self.conn.Execute(sql_str)
                ads_refer_rows = results.GetRows()
            except InconsistentResponses:
                pass
        if ads_refer_rows is not None and len(ads_refer_rows) > 0:
            for ads_refer_row in ads_refer_rows:
                edge_str = self.generate_ads_refer_edge(ads_refer_row[1],
                                                        ads_refer_row[2],
                                                        ads_refer_row[3],
                                                        node_label_map)
                print edge_str
                dot_data += edge_str
                dot_data += "\n"
        dot_data += " }"
        node_defines_str = ""
        for key, value in node_label_map.items():
            node_define_str = value
            node_define_str += '[label="'
            node_define_str += key
            node_define_str += '"]'
            node_define_str += '\n'
            node_defines_str += node_define_str
        dot_data = dot_data.replace("%node_defines%", node_defines_str)
        with io.open("ads_refer_graph.dot", 'w') as file_handle:
            file_handle.write(unicode(dot_data))

    def generate_ads_refer_edge(self,
                                ads_host,
                                ads_target,
                                refer_count,
                                node_label_map):
        if ads_host not in node_label_map.keys():
            node_label_map[ads_host] = "node%s" % len(node_label_map.keys())
        if ads_target not in node_label_map.keys():
            node_label_map[ads_target] = "node%s" % len(node_label_map.keys())

        edge_str = node_label_map[ads_host]
        edge_str += "->"
        edge_str += node_label_map[ads_target]
        edge_str += "[label = "
        edge_str += str(refer_count)
        edge_str += "];"
        return edge_str


def main():
    dbspec = 'localhost:adspider:123456:adspider'
    ads_analyser = AdsAnalyser(dbspec, 20, 2, 2)
    ads_analyser.initialize()
    domain_list = ads_analyser.get_all_ads_target_domains()
    domain_list.sort()
    print domain_list
    ads_analyser.update_all_ads_refer_group(domain_list)
    ads_refer_list = ads_analyser.get_all_ads_refers()
    ads_analyser.generate_ads_refer_graph_dot_file()
    ads_analyser.finalize()


if __name__ == '__main__':
    main()
