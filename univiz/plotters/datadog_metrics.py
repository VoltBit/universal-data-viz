''' Plotter for Datadog custom metrics.
Input: CSV file with Datadog's 'Top 500' metrics from the administration account
Output: HTML Plotly plot with a chart with percentages for the usage
'''
import sys
import pandas as pd
from plotly import graph_objects as go
from pprint import pprint


class DDPlotter(object):
    component_glossary = {
        'appRestExecutionTime': 'app-backend',
        'callbackExecutionTime': 'app-backend',
        'cb': 'collaboration',
        'io': 'io.dropwizard.jetty (Suggestions + Linelinker)',
        'messagecore': 'message-core',
        'EmailResource': 'backend-service',
        'ExternalEmailResource': 'backend-service',
        'AccesslistResource': 'backend-service',
        'ConversationResource': 'backend-service',
        'DynamicValidationResource': 'backend-service',
        'ExternalUserGroupResource': 'backend-service',
        'ExternalConnectionGroupResource': 'backend-service',
        'CreditNoteResource': 'backend-service',
        'DocumentFileResource': 'backend-service',
        'AssignmentResource': 'backend-service',
        'ExternalCompanyAccountResource': 'backend-service',
        'ExternalUserResource': 'backend-service',
        'ExternalNetworkResource': 'backend-service',
        'UserResource': 'backend-service',
        'DocumentResource': 'backend-service',
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

    def sum_components(self, data):
        sum_data = {}
        for component in data:
            if component in self.component_glossary:
                key = self.component_glossary[component]
            else:
                key = component
            if key in sum_data:
                sum_data[key] += sum([x['avg'] for x in data[component]])
            else:
                sum_data[key] = sum([x['avg'] for x in data[component]])
        return sum_data

    def plot_metrics(self, data):
        data = self.sum_components(data)
        pprint(data)
        print("Total custom metrics: ", sum(list(data.values())))
        print("Total different components: ", len(data.keys()))
        chart = go.Pie(labels=list(data.keys()), values=list(data.values()), textinfo='label+text+value+percent')
        go.Figure(chart).show()

    def analyze(self, file_name):
        raw_data = self.read_file(file_name)
        data = self.extract_metrics(raw_data)
        self.plot_metrics(data)


def main():
    DDPlotter().analyze('../../data/top_avg_metrics_extract_2019-08-13.csv')


if __name__ == '__main__':
    main()
