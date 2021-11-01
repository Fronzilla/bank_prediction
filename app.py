import streamlit as st

import scr.session_state as session
from scr.data import load_data
from scr.download import csv_download_link
from scr.model import load_model

st.set_page_config(page_title='Domain classification', layout='wide')


def main():
    session_state = session.get(df_data=None, domain_column=None, encoder=None, model=None)
    st.header(""" Сервис классификации банков""")

    st.sidebar.subheader('FAQ')

    with st.sidebar.beta_expander('Как использовать?'):
        st.write("""
                1. Загрузите файл следующих форматов:
                    - 'csv' 
        """)

    with st.sidebar.beta_expander('Какие колонки должны быть в .csv файле '):
        st.write(""" 
        
        .csv файл должен содержать следующие данные для каждого банка 
        
                    {'Портфель', 'Возраст', 'Пол', 'Регион выдачи паспорта',
                    'Регион регистрации (стандартизировано)', 'Город выдачи',
                    'Место работы', 'Должность', 'Тип займа',
                    'Дата договора стандартизированная',
                    'Сумма договора стандартизированная', 'Отношение осз к сумме договора',
                    'Возраст ИД', 'количество кредитов с просрочкой по бки', 'odv',
                    'HasEDO', 'Город ФМЖ', 'Город регистрации', 'Статус'}
        
        """)

    with st.sidebar.beta_expander('Какие банки классифицируются?'):
        st.write(""" 

        Классификатор умеет работать со следующими банками

                    (0004) Азиатско-Тихоокеанский Банк (ПАО)	
                    (0117) АО Банк Русский Стандарт	
                    (0227) АО Райффайзенбанк	
                    (0275) АО ЮниКредит Банк	
                    (0414) КБ Ренессанс Кредит (ООО)	
                    (0434) КИВИ Банк (АО)	0.500000	
                    (0706) ПАО Банк Санкт-Петербург
                    (0729) ПАО КБ УБРиР	0.000000	
                    (0737) ПАО МОСКОВСКИЙ КРЕДИТНЫЙ БАНК	
                    (0748) ПАО Промсвязьбанк
                    
        """)

    with st.spinner('Загрузка метаданных...'):
        load_data(session_state)  # загрузка данных в сессию
        load_model(session_state)  # загрузка модели в сессию

    if session_state.df_data is not None:
        df = session_state.df_data
        st.write(df.dtypes)

        with st.spinner('Классификация банков...'):
            result = session_state.model.predict(df)

        df['bank'] = result

        st.write('Ссылка на скачивание')
        csv_download_link(df)


if __name__ == '__main__':
    main()
