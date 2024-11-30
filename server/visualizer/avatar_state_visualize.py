import os
import json
from datetime import datetime

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go


st.set_page_config(
    page_title="Event Timeline",
    page_icon="📅",
    layout='wide'
)


LOG_DIR = '../logs'

ENVENT_MAPPING = {
    'GetNews': '刷新闻',
    'GetGeekNewsHotList': '刷稀土掘金',
    'ChooseOneGeekNews': '查看详细稀土掘金内容',
    'GoTo': '前往某个地点',
    'GetLeetCodeList': '查看 LeetCode 目录',
    'ChooseOneLeetCodeQuestion': '刷一道 LeetCode',
    'AddMemory': '添加记忆',
    'GetBooks': '看书',
    'Cooking': '做饭',
    'PostWeibo': '发微博',
    'CheckWeiBoComments': '查看微博评论',
    'ReplyWeiboComment': '回复微博评论',
    'Search': '搜索'
}

EVENTS_NEED_TO_MONITOR = [
    'GoTo',
    'ChooseOneLeetCodeQuestion',
    'Cooking'
]


def visualize_avatar_state(activities_dict):
    df_dict = {
        'Task': [],
        'Start': [],
        'Finish': [],
        'Description': []
    }
    
    # 将数据转换为DataFrame格式
    times = sorted(list(activities_dict.keys()))
    for i in range(len(times)):
        start_time = datetime.strptime(times[i], '%Y-%m-%d %H:%M:%S,%f')
        end_time = (datetime.strptime(times[i+1], '%Y-%m-%d %H:%M:%S,%f') 
                   if i < len(times)-1 
                   else start_time + pd.Timedelta(minutes=1))
        
        activity = activities_dict[times[i]]
        task_name = activity.split('.')[0]  # 提取活动名称
        
        df_dict['Task'].append(task_name)
        df_dict['Start'].append(start_time)
        df_dict['Finish'].append(end_time)
        df_dict['Description'].append(activity)

    df = pd.DataFrame(df_dict)
    
    unique_tasks = df['Description'].unique()
    
    colors = {}
    color_sequence = px.colors.qualitative.Set3
    for i, task in enumerate(unique_tasks):
        colors[task] = color_sequence[i % len(color_sequence)]

    fig = ff.create_gantt(df, 
                         colors=colors,
                         index_col='Description',
                         show_colorbar=True,
                         group_tasks=True,
                         showgrid_x=True,
                         showgrid_y=True)

    fig.update_layout(
        title='活动时间轴',
        xaxis_title='时间',
        height=400,
        font=dict(size=10)
    )

    st.plotly_chart(fig, use_container_width=True)


def parse_event_from_log(log_path):
    """
    从日志中解析出 avatar 的事件。
    """
    event_dict, monitor_events = {}, {}
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            if 'INFO - llm_result=' in line:
                date = line.split('- INFO -')[0].strip()
                cur_e_dict_str = line.split('INFO - llm_result=')[1].strip().strip("'")
                
                try:
                    cur_e_dict_str = cur_e_dict_str.replace("\\'", "§§§")
                    cur_e_dict_str = cur_e_dict_str.replace("'", '"')
                    cur_e_dict_str = cur_e_dict_str.replace("§§§", "'")    
                    cur_e_dict = json.loads(cur_e_dict_str)
                except Exception as e:
                    print(f"Error parsing JSON: {cur_e_dict_str}")
                    continue

                event = cur_e_dict['execute'].split('.')[0]
                event_dict[date] = ENVENT_MAPPING[event] if event in ENVENT_MAPPING else event

                if event in EVENTS_NEED_TO_MONITOR:
                    event_name = ENVENT_MAPPING[event] if event in ENVENT_MAPPING else event
                    if event_name not in monitor_events:
                        monitor_events[event_name] = []
                    value = cur_e_dict['execute'].split('.call(')[-1].replace('self', '').replace(',', '').replace(')', '').replace("'", '').strip()
                    monitor_events[event_name].append(value)
                
    return event_dict, monitor_events


def main():
    st.markdown(
        "<h1 style='text-align: center;'>📅 Event Timeline</h1>", 
        unsafe_allow_html=True
    )

    with st.expander('选择日志文件', expanded=True):
        log_name = st.selectbox(
            '选择日志文件',
            os.listdir(LOG_DIR),
            label_visibility='collapsed'
        )   

    with st.spinner('解析日志中...'):
        event_dict, monitor_events = parse_event_from_log(
            os.path.join(LOG_DIR, log_name)
        )
    # print(json.dumps(event_dict, indent=4, ensure_ascii=False))

    with st.container(border=False):
        visualize_avatar_state(event_dict)

    cols = 3
    col_list = st.columns(cols)
    for i, (event, values) in enumerate(monitor_events.items()):
        with col_list[i % cols]:
            with st.container(border=False):
                value_counts = {}
                for value in values:
                    value_counts[value] = value_counts.get(value, 0) + 1
                    
                colors = px.colors.qualitative.Set3
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(value_counts.keys()),
                        y=list(value_counts.values()),
                        marker_color=colors[:len(value_counts)],
                        showlegend=False
                    )
                ])
                
                fig.update_layout(
                    title=event,
                    yaxis_title="出现次数",
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    main()
