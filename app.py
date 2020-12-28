import streamlit as st
import pandas as pd
from classifier import Classifier

st.set_page_config(page_title='player salary', layout='wide')
st.title('Ice hockey player salary estimator')



# @app.route("/", methods = ["POST", "GET"])
# def index_page(player_id=66):
#     predicted_salary = 0
#     if request.method == "POST":
#         try:
#             player_id = int(request.form['player_id'])
#             predicted_salary = classifier.predict_salary(player_id)
#         except:
#             pass

#     return render_template(
#         'index.html',
#         predicted_salary=predicted_salary
#     )

def main():

    # st.image('cut2.jpg')

    data_load_state = st.text('Loading data...')
    classifier = Classifier()
    data_load_state.text('Loading data...done!')

    st.sidebar.write('Select player parameters and chose player from drop down list or the central part of the screen')

    position = st.sidebar.radio("Position", ['Any', 'C', 'RW', 'LW', 'D'])

    hand = st.sidebar.radio("Hand", ['Any', 'L', 'R'])

    min_value=int(classifier.train.G.min())
    max_value=int(classifier.train.G.max())
    goals = st.sidebar.slider(
        "Goals:", min_value=min_value, 
        max_value=max_value,
        value=(min_value, max_value),
        step=1,
    )

    country_list = classifier.train.Cntry.unique()
    if len(country_list) > 0:
        country_list.sort()
        country_list = ['Any'] + list(country_list)
    country = st.sidebar.multiselect("Country", country_list, default = 'Any')

    team_list = list(classifier.train.Team.unique())
    if len(team_list) > 0:
        team_list.sort()
        team_list = ['Any team'] + team_list
    team = st.sidebar.multiselect('Team', team_list, default='Any team')
    
    st.subheader('Players data')

    df = classifier.train
    
    if position != 'Any':
        df = df.loc[lambda x: (x.Position.str.contains(position))]

    if hand != 'Any':
        df = df.loc[lambda x: (x.Hand == hand)]

    if 'Any' not in country:
        df = df.loc[lambda x: (x.Cntry.isin(country))]
        
    if 'Any team' not in team:
        df =  df.loc[lambda x: (x.Team.isin(team))]

    df = df.loc[lambda x: (goals[0] <= x.G) & (x.G <= goals[1])]

    display_columns = ['Team', 'Last Name', 'First Name', 'Born', 'Cntry', 'City', 'Position', 'Hand']

    other_columns = ['GP',
 'G',
 'A',
 'A1',
 'A2',
 'PTS',
 '+/-',
 'E+/-',
 'PIM',
 'Shifts',
 'TOI',
 'TOIX',
 'TOI/GP',
 'TOI/GP.1',
 'TOI%',
 'IPP%',
 'SH%',
 'SV%',
 'PDO',
 'F/60',
 'A/60',
 'Pct%',
 'Diff',
 'Diff/60',
 'iCF',
 'iCF.1',
 'iFF',
 'iSF',
 'iSF.1',
 'iSF.2',
 'ixG',
 'iSCF',
 'iRB',
 'iRS',
 'iDS',
 'sDist',
 'sDist.1',
 'Pass',
 'iHF',
 'iHF.1',
 'iHA',
 'iHDf',
 'iMiss',
 'iGVA',
 'iTKA',
 'iBLK',
 'iGVA.1',
 'iTKA.1',
 'iBLK.1',
 'BLK%',
 'iFOW',
 'iFOL',
 'iFOW.1',
 'iFOL.1',
 'FO%',
 '%FOT',
 'dzFOW',
 'dzFOL',
 'nzFOW',
 'nzFOL',
 'ozFOW',
 'ozFOL',
 'FOW.Up',
 'FOL.Up',
 'FOW.Down',
 'FOL.Down',
 'FOW.Close',
 'FOL.Close',
 'OTG',
 '1G',
 'GWG',
 'ENG',
 'PSG',
 'PSA',
 'G.Bkhd',
 'G.Dflct',
 'G.Slap',
 'G.Snap',
 'G.Tip',
 'G.Wrap',
 'G.Wrst',
 'CBar ',
 'Post',
 'Over',
 'Wide',
 'S.Bkhd',
 'S.Dflct',
 'S.Slap',
 'S.Snap',
 'S.Tip',
 'S.Wrap',
 'S.Wrst',
 'iPenT',
 'iPenD',
 'iPENT',
 'iPEND',
 'iPenDf',
 'NPD',
 'Min',
 'Maj',
 'Match',
 'Misc',
 'Game',
 'CF',
 'CA',
 'FF',
 'FA',
 'SF',
 'SA',
 'xGF',
 'xGA',
 'SCF',
 'SCA',
 'GF',
 'GA',
 'RBF',
 'RBA',
 'RSF',
 'RSA',
 'DSF',
 'DSA',
 'FOW',
 'FOL',
 'HF',
 'HA',
 'GVA',
 'TKA',
 'PENT',
 'PEND',
 'OPS',
 'DPS',
 'PS',
 'OTOI',
 'Grit',
 'DAP',
 'Pace',
 'GS',
 'GS/G']

    df_display = df[display_columns + other_columns]

    st.dataframe(df_display)

    try:
        selected_player = st.selectbox('Select player:', df_display['Last Name'], index=0)
    except:
        selected_player = st.selectbox('Select player:', classifier.train['Last Name'], index=0)

    if st.button('Predict salary'):
        try:
            with st.spinner('Start predicting...'):
                player_id = classifier.train.loc[lambda x: x['Last Name'] == selected_player].index[0]
                # st.write(player_id)
                predicted_salary = classifier.predict_salary(player_id)
                st.markdown(f"Predicted salary: ** {predicted_salary:.2f}$**")
        except:
            st.write('Could not predict')
    # st.subheader('Map of all pickups')
    # clubs = pd.read_csv('clubs_geo.csv')
    # st.map(clubs)

if __name__ == "__main__":
    main()