import streamlit as st
import sqlite3
import pandas as pd
import datetime as dt
import streamlit.components.v1 as components
import os


st.title("일일 체크 _ver1.0")
only_date = dt.datetime.now().date()
# Connect to the database
sidebar = st.sidebar


with sqlite3.connect('test.db') as conn:
    cursor = conn.cursor()

    # Create the table if it does not exist
    cursor.execute('''CREATE TABLE \
                if NOT EXISTS checkDay2 (
                        col1 integer, col2 integer,
                        col3 integer, col4 integer,
                        col5 integer, col6 integer,
                        col7 integer, col8 integer,
                        col9 integer, col10 integer,
                        date_time text DEFAULT (datetime(date('now'),'localtime'))
                    )''')

    # Define a function to check if the current date already exists in the table
    def date_exists():
        cursor.execute('''SELECT *
                    FROM checkDay2
                    WHERE date_time
                    LIKE ?''',
                       (f'%{only_date}%',))
        rows = cursor.fetchall()
        return len(rows) > 0

    # Create a form to input values for each button
    buttons = ["인입", "신규", "동의서", "데이터", "유효성",
               "테스트", "실이전", "도메인", "안정화", "취소"]
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(
        10)
    cols = [col1, col2, col3, col4, col5, col6, col7, col8, col9, col10]

    # DB 에서 불러온 값 저장
    def get_saved_values():

        # print(only_date)
        cursor.execute('''SELECT * \
                    FROM checkDay2 \
                    WHERE date_time \
                    LIKE ? \
                    ORDER BY date_time \
                    ASC limit 1''',
                       (f'%{only_date}%',))
        return cursor.fetchone()

    # print("테스트+ ", get_saved_values())
    saved_values = get_saved_values()

    if saved_values is None:
        # cursor.execute('''INSERT INTO checkDay2 (col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, date_time)
        #                     VALUES (?,?,?,?,?,?,?,?,?,?, \
        #                     datetime('now','localtime'))''',
        #                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

        # Save the changes to the database
        # conn.commit()
        saved_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # 튜플형태 임으로 list로 변환

    # 저장된 값이 없을 경우 0으로 초기화합니다.

    for i in range(len(buttons)):

        with cols[i]:

            number = st.number_input(
                f'Insert a number{i}', step=1, value=saved_values[i], label_visibility='hidden', min_value=0)

            if number != 0:

                saved_values = list(saved_values)
                saved_values[i] = number

            st.write(buttons[i])
            st.write(f' {saved_values[i]}')

    # db 숫자 불러오기
    # for i in (range(10)):
    #     with cols[i]:
    #         st.write(saved_values[i])

    # Save the form inputs to the database

    if st.button('Save'):
        # Insert or update the data depending on whether the current date already exists
        if date_exists():
            # Update the data for the current date
            cursor.execute('''UPDATE checkDay2 \
                SET col1=?, col2=?, col3=?, col4=?, col5=?, col6=?, col7=?, col8=?, col9=?, col10=? \
                WHERE date_time \
                LIKE ?''',
                           (saved_values[0], saved_values[1], saved_values[2], saved_values[3], saved_values[4], saved_values[5], saved_values[6], saved_values[7], saved_values[8], saved_values[9], f'%{only_date}%'))
        else:
            # Insert a new row for the current date
            cursor.execute('''INSERT INTO checkDay2 (col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, date_time)
                            VALUES (?,?,?,?,?,?,?,?,?,?, \
                            datetime('now','localtime'))''',
                           (saved_values[0], saved_values[1], saved_values[2], saved_values[3], saved_values[4], saved_values[5], saved_values[6], saved_values[7], saved_values[8], saved_values[9]))

        # Save the changes to the database
        conn.commit()

        st.success('Data saved successfully!')
# 날짜만 표기 하기 위해 쿼리문에서 date(date_time) as '등록일' 추가
df2 = pd.read_sql_query(
    "SELECT col1 as '인입',\
    col2 as '신규',\
    col3 as '동의서',\
    col4 as '데이터',\
    col5 as '유효성',\
    col6 as '테스트',\
    col7 as '실이전',\
    col8 as '도메인',\
    col9 as '안정화',\
    col10 as '취소',\
    date(date_time) as '등록일'\
    FROM checkDay2 \
    WHERE date_time order by date_time DESC limit 1", conn)

# st.dataframe(df2)
df3 = df2.set_index('등록일')
st.write(df3)
conn.close()
# # 리셋 버튼추가를 위할시 해당 블럭 주석 해제
# if st.checkbox('리셋', False, key=1):

#     if not st.button('Reset'):

#         saved_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     # Insert or update the data depending on whether the current date already exists
#         if date_exists():
#             # Update the data for the current date
#             cursor.execute('''UPDATE checkDay2 \
#                     SET col1=?, col2=?, col3=?, col4=?, col5=?, col6=?, col7=?, col8=?, col9=?, col10=? \
#                     WHERE date_time \
#                     LIKE ?''',
#                            (saved_values[0], saved_values[1], saved_values[2], saved_values[3], saved_values[4], saved_values[5], saved_values[6], saved_values[7], saved_values[8], saved_values[9], f'%{only_date}%'))
#             st.success('Data saved successfully!')

#         else:
#             # Insert a new row for the current date
#             cursor.execute('''INSERT INTO checkDay2 (col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, date_time)
#                                 VALUES (?,?,?,?,?,?,?,?,?,?, \
#                                 datetime('now','localtime'))''',
#                            (saved_values[0], saved_values[1], saved_values[2], saved_values[3], saved_values[4], saved_values[5], saved_values[6], saved_values[7], saved_values[8], saved_values[9]))
#             st.success('Data saved successfully!')

#         # Save the changes to the database
#         conn.commit()
if sidebar.button("페이지2"):
    st.title("페이지2")
