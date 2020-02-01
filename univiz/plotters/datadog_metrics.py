''' Plotter for Datadog custom metrics.
Input: CSV file with Datadog's 'Top 500' metrics from the administration account
Output: HTML Plotly plot with a chart with percentages for the usage
'''
import sys
import pandas as pd
from plotly import graph_objects as go
from plotly import offline
from pprint import pprint


class DDPlotter(object):
    component_glossary = {
        'appRestExecutionTime': 'App-Backend',
        'callbackExecutionTime': 'App-Backend',
        'cb': 'collaboration',
        'io': 'io.dropwizard.* (Suggestions + Linelinker)',
        'document': 'document.*',
        'messagecore': 'Message-Core',
        'EmailResource': 'Backend-Service',
        'ExternalEmailResource': 'Backend-Service',
        'AccesslistResource': 'Backend-Service',
        'ConversationResource': 'Backend-Service',
        'DynamicValidationResource': 'Backend-Service',
        'ExternalUserGroupResource': 'Backend-Service',
        'ExternalConnectionGroupResource': 'Backend-Service',
        'CreditNoteResource': 'Backend-Service',
        'DocumentFileResource': 'Backend-Service',
        'AssignmentResource': 'Backend-Service',
        'ExternalCompanyAccountResource': 'Backend-Service',
        'ExternalUserResource': 'Backend-Service',
        'ExternalNetworkResource': 'Backend-Service',
        'UserResource': 'Backend-Service',
        'DocumentResource': 'Backend-Service',
        'eagle_pod_container_resource_limits_cpu_cores': 'eagle_pod (Soren M.)',
        'eagle_pod_container_resource_limits_memory_bytes': 'eagle_pod (Soren M.)',
        'eagle_pod_container_resource_requests_cpu_cores': 'eagle_pod (Soren M.)',
        'eagle_pod_container_resource_requests_memory_bytes': 'eagle_pod (Soren M.)',
        'eagle_pod_container_resource_usage_cpu_cores': 'eagle_pod (Soren M.)',
        'eagle_pod_container_resource_usage_memory_bytes': 'eagle_pod (Soren M.)',
        'grpc_server_handled_total': 'grpc_server (Telegraf from truebn)',
        'grpc_server_handling_seconds': 'grpc_server (Telegraf from truebn)',
        'grpc_server_msg_received_total': 'grpc_server (Telegraf from truebn)',
        'grpc_server_msg_sent_total': 'grpc_server (Telegraf from truebn)',
        'grpc_server_started_total': 'grpc_server (Telegraf from truebn)',
        'supplier_management': 'Supplier Management',
        'tradeshift_go': 'TS Go',
        'cloudscan_service': 'Cloudscan'
    }
    component_metrics = {}

    def read_file(self, file_name):
        print("Reading file: %s" % file_name)
        with open(file_name) as fh:
            data = pd.read_csv(fh)
            data.set_axis(['metric', 'avg', 'max'], axis=1, inplace=True)
        return data

    def extract_metrics(self, raw_data):
        for index, row in raw_data.iterrows():
            component = row['metric'].split('.')[0]
            if component not in self.component_metrics:
                self.component_metrics[component] = []
            self.component_metrics[component].append(row)
        return self.component_metrics

    def sum_components(self, data, col):
        sum_data = {}
        for component in data:
            if component in self.component_glossary:
                key = self.component_glossary[component]
            else:
                key = component + ".*"
            if key in sum_data:
                sum_data[key] += sum([x[col] for x in data[component]])
            else:
                sum_data[key] = sum([x[col] for x in data[component]])
        return sum_data

    def plot_metrics(self, data, data_type):
        report_file = '../templates/results.html'
        if data_type == 'max':
            data = self.sum_components(data, 'avg')
            title = 'Average number of custom metrics per service'
            report_file = '../templates/results_average.html'
        elif data_type == 'avg':
            data = self.sum_components(data, 'max')
            title = 'Maximum number of custom metrics per service'
            report_file = '../templates/results_maximum.html'
        pprint(data)
        print("Total custom metrics: ", sum(list(data.values())))
        print("Total different components: ", len(data.keys()))
        chart = go.Pie(labels=list(data.keys()), values=list(data.values()), textinfo='label+text+value+percent')
        fig = go.Figure(chart)

        fig.update_layout(
            title=title,
            xaxis_title="x Axis Title",
            yaxis_title="y Axis Title",
        )

        offline.plot(fig, filename=report_file)

    def analyze(self, file_name):
        raw_data = self.read_file(file_name)
        data = self.extract_metrics(raw_data)
        self.plot_metrics(data, 'avg')
        self.plot_metrics(data, 'max')


def main():
    # DDPlotter().analyze('../../data/top_avg_metrics_extract_2019-08-13.csv')
    DDPlotter().analyze('../../data/top_avg_metrics_extract_2019-12-17 13_22_15.751858.csv')


if __name__ == '__main__':
    main()
