from flask import Flask, render_template, request
import os
import json
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

# 基本文件夹路径
base_folder = "static/result/"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/plot', methods=['POST'])
def plot():
    dataset_name = request.form.get('dataset')
    folder_name = request.form.get('algorithm')
    selected_metric = request.form.get('metric')  # 获取用户选择的指标

    # 使用 os.path.join() 组合基本路径和用户输入的文件夹名称
    folder_path = os.path.join(base_folder, dataset_name, folder_name)

    print(folder_path)
    data_list = []

    # 逐个读取 JSON 文件
    json_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if
                  filename.endswith('.json')]

    for file_name in json_files:
        with open(file_name, 'r') as json_file:
            data = json.load(json_file)
            data_list.append(data)

    # 设置颜色
    colors = plt.cm.viridis(np.linspace(0, 1, len(data_list)))
    methods = [entry['subDataset'] for entry in data_list]
    print(selected_metric)

    # recall_values = [entry['result'][0]['recall'] if "recall" in entry['result'][0] else 0 for entry in data_list]
    # 根据用户选择的指标生成相应的数据
    if selected_metric == 'precision':
        metric_values = [entry['result'][0]['precision'] if "precision" in entry['result'][0] else 0 for entry in
                         data_list]
        ylabel = 'Precision'
    elif selected_metric == 'recall':
        metric_values = [entry['result'][0]['recall'] if "recall" in entry['result'][0] else 0 for entry in data_list]
        ylabel = 'Recall'
    elif selected_metric == 'pf':
        metric_values = [entry['result'][0]['pf'] if (
                    "pf" in entry['result'][0] and isinstance(entry['result'][0]['pf'], (int, float))) else 0 for entry
                         in data_list]
        ylabel = 'False Positive Rate (PF)'
    elif selected_metric == 'F-measure':
        metric_values = [entry['result'][0]['F-measure'] if "F-measure" in entry['result'][0] else 0 for entry in
                         data_list]
        ylabel = 'F-Measure'
    elif selected_metric == 'accuracy':
        metric_values = [entry['result'][0]['accuracy'] if "accuracy" in entry['result'][0] else 0 for entry in
                         data_list]
        ylabel = 'Accuracy'
    elif selected_metric == 'AUC':
        metric_values = [entry['result'][0]['AUC'] if (
                    "AUC" in entry['result'][0] and isinstance(entry['result'][0]['AUC'], (int, float))) else 0 for
                         entry in data_list]
        ylabel = 'AUC (Area Under the Curve)'
    else:
        metric_values = []  # 处理其他情况
        ylabel = 'Unknown'

    print(metric_values)
    # 创建柱状图
    plt.bar(methods, metric_values, color=colors)
    plt.xlabel(f'SubDataset({dataset_name})')
    plt.ylabel(selected_metric)
    plt.title(f'{selected_metric} for Different SubDataset using {folder_name}')
    for i, value in enumerate(metric_values):
        plt.text(i, value, f'{value:.2f}', ha='center', va='bottom')

    # 保存图表为图片
    plot_filename = f'static/image/{dataset_name}_{folder_name}_plot.png'
    plt.savefig(plot_filename)
    plt.clf()  # 清空图表

    print(selected_metric)
    return render_template('index.html', plot_filename=plot_filename)


if __name__ == '__main__':
    app.run(debug=True)
