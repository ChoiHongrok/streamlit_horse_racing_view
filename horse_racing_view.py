import joblib
import pandas as pd
import streamlit as st


st.title('Horse racing Record')
df_path = './data/racing_df_2017_20230514.csv'
df = pd.read_csv(df_path, encoding='cp949')

# string colums
int2str_cols = ['rcDate', 'birthday']
df[int2str_cols] = df[int2str_cols].astype(str)

# change column order
horse = ['hrName', 'chulNo', 'hrNo', 'hrTool', 'age', 'birthday', 'sex', 'rating', ]
game_info = ['weather', 'meet', 'rcDate', 'rcDay', 'ilsu', 'rcDist', 'rcName', 'rcNo', 
             'ageCond', 'prizeCond', 'rank', 'budam', 'track' ]
time_info = ['rcTime', 'rcTimeG1f', 'rcTimeG2f', 'rcTimeG3f', 'rcTime_1c', 'rcTime_2c', 'rcTime_3c', 'rcTime_400',
             'rcTime_4c', 'rcTimeS1f', 'diffUnit', ]
weight = ['wgBudam', 'wgBudamBigo', 'wgHr', 'wgJk']
rank_info = ['ordBigo', 'ord', 'ordG1f', 'g2f', 'g3f_4c', 'g4f_3c', 'ordS1f', 'g6f_2c', 'g8f_1c']
prize = ['chaksun1', 'chaksun2', 'chaksun3', 'chaksun4', 'chaksun5', 'buga1', 'buga2', 'buga3',]
rider_trainer = ['jkName', 'jkNo', 'trName', 'trNo']
odds = ['plcOdds', 'winOdds',]
etc = ['name', 'owName', 'owNo', 'rankRise', ]

col_types = {'말':horse, '게임정보':game_info, '기록':time_info, '중량':weight, 
             '순위':rank_info, '상금':prize, '기수_조교사':rider_trainer, '배당':odds, '기타':etc}
col_all = horse + game_info + weight + rank_info + time_info + rider_trainer + prize + odds + etc
df = df[col_all]

col2name = joblib.load('./data/racing_record_col2name.dict')


n_cols = len(df.columns)
with st.expander('경주성적표 용어해설'):
    st.text('''
    펄롱타임 : 1펄롱(200m)을 주파한 기록

    통과거리 : 말이 달린 거리

    통과타임

    - 선두마가 통과거리를 지날 때의 주파기록
    - 1F 간격으로 역산하며 마지막 기록은 그 경주의 1위마의 우승기록
    구간별 통과순위 : 각 말의 주행을 검토하는 기초자료로 각 코너 통과시의 말 위치

    - S1F : 출발지점에서 200m 지점
    - 1C : 1코너로 결승선 전 1,680m지점
    - 2C : 2코너로 결승선 전 1,400m지점
    - 3C : 3코너로 결승선 전 810m지점
    - G3F : 결승선 전 600m지점
    - 4C : 4코너로 결승선 전 530m지점
    - G1F : 결승선 전 200m지점
    - 표기방법
    * (1,2,3)은 1마신 미만의 마군표시. ( )내의 내측의 마필부터 표시
    * (1,^2,3)중 ^표시 마번은 선두집단의 표시
    * 1,2,3은 선행마로부터 1마신이상 2마신미만의 차이 표시
    * 1-2-3은 선행마로부터 2마신이상 5마신미만의 차이 표시
    * 1=2=3은 선행마로부터 5마신이상 10마신미만의 차이 표시
    * 1≡2≡3은 선행마로부터 10마신아상 대차
    * 3은 주행중시 표시
    통과 누적기록 : 각 코너 통과시의 선두말 통과 누적기록

    - S1F지점 : 출발지점에서 200m 지점까지의 통과 기록
    - 1코너(1C)지점 : 출발지점에서 1코너(결승선 전 1,680m지점)까지의 통과 누적기록
    - 2코너(2C)지점 : 출발지점에서 2코너(결승선 전 1,400m지점)까지의 통과 누적기록
    - 3코너(3C)지점 : 출발지점에서 3코너(결승선 전 810m지점)까지의 통과 누적기록
    - G3F지점 : 결승선 전 600m지점으로, 출발지점에서 결승선 전 600m지점까지의 통과 누적기록
    - 4코너(4C)지점 : 결승선 전 530m지점으로, 출발지점에서 결승선 전 530m지점까지의 통과 누적기록
    - G1F지점 : 결승선 전 200m지점으로, 출발지점에서 결승선 전 200m지점까지의 통과 누적기록
    펄롱타임 : 결승선 전 마지막 주파기록

    - 3F-G : 결승선 전 600m지점부터 결승선까지의 기록
    - 1F-G : 결승선 전 200m지점부터 결승선까지의 기록
    
    - budam변수 별정?
    상금많은 말은 부중을 더 주는게 별정A형, 
    상금적은말은 부중을 덜어주는게 별정B형, 
    상금많은 말은 부중을 올리고 상금적은 말은 부중을 내려주는게 별정C형. 
    대부분 별정B형으로 가고 능력마들게임은 별정A형으로 가는 경향이 있습니다....부중을 더 주는 것은 좀 그렇죠...능력마가 많지 않기 때문...
    ''')

main_cols = ['meet', 'rcDate', 'rcDay', 'rcDist', 'rcNo', 'weather', 'chulNo', 'age', 'sex', 'hrName']
sel_type = st.radio('choose your selection type', (1, 2), horizontal=True)
selected_cols = []

if sel_type == 1:
    # type 1
    for type_name, col_type in col_types.items():
        n_col_type = len(col_type)
        with st.expander(f'변수 선택: {type_name}({n_col_type}개)'):
            all_check = st.checkbox('전체선택', value=0, key=f'전체선택_{type_name}')
            n_st_cols = 5
            st_cols = st.columns(n_st_cols)
            
            selection = {}
            for i, col in enumerate(col_type):
                st_idx = i // (int(n_col_type/n_st_cols) + 1)# // round(63/5) = 13 // round(13/5) = 3 // round(8/5) = 2개 // round(5 / 5) = 1
                with st_cols[st_idx]:
                    init_value = 1 if col in main_cols else 0
                    init_value = 1 if all_check else init_value
                    selection[col] = st.checkbox(f'{col} ({col2name.get(col)})', value=init_value)
                    
        selected = [col for col, select in selection.items() if select == True]
        selected_cols.extend(selected)
    # with st.expander(f'변수 선택({n_cols}개)'):
    #     all_check = st.checkbox('전체선택', value=1)
    #     n_st_cols = 4
    #     st_cols = st.columns(n_st_cols)
        
    #     selection = {}
    #     for i, col in enumerate(df.columns):
    #         st_idx = i // round(n_cols/n_st_cols)# // round(63/5) = 13
    #         with st_cols[st_idx]:
    #             init_value = 1 if all_check else 0
    #             selection[col] = st.checkbox(f'{col} ({col2name.get(col)})', value=init_value)
                    
    #     selected = [col for col, select in selection.items() if select == True]

elif sel_type == 2:
    ## type 2
    for type_name, col_type in col_types.items():
        n_col_type = len(col_type)
        with st.expander(f'변수 선택: {type_name}({n_col_type}개)'):
            container = st.container()

            all = st.checkbox("Select all", value=0, key=f'전체선택_{type_name}')
        
            cols = [f'{col} ({col2name.get(col)})' for col in col_type]
            
            if all:
                selected = container.multiselect("Select one or more options:",
                    list(cols), list(cols))
            else:
                selected =  container.multiselect("Select one or more options:",
                    list(cols), [col for col in cols if col.split()[0] in main_cols])
            selected = [col.split()[0] for col in selected]
            selected_cols.extend(selected)

horse_name = st.text_input('horse name:')

col1, col2 = st.columns(2)
from_date = col1.text_input('Date(from):\n\n(format=yyyymmdd, yyyymm, yyyy)')
to_date = col2.text_input('Date(to):\n\n(format=yyyymmdd, yyyymm, yyyy) ')

df_selected = df[selected_cols]
if horse_name:
    df_selected = df_selected.query('hrName == @horse_name')
if from_date:
    df_selected = df_selected.query('rcDate >= @from_date')

if to_date:
    df_selected = df_selected.query('rcDate <= @to_date')
    
st.write('DataFrame')
st.dataframe(data=df_selected, width=90000)
