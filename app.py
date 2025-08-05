import pandas as pd
import streamlit as st
import joblib
from datetime import datetime, date
import numpy as np

st.set_page_config(initial_sidebar_state='expanded',page_title='Prédicteur la campagne marketing - Youssouf',page_icon='🏦',layout='wide')

# source
@st.cache_resource
def charger_model():
    try:
        model = joblib.load('modelGBT.pkl')
        features = joblib.load('features.pkl')
        return model,features
    except FileNotFoundError as e:
        st.error(f'Erreur: Fichier manquant - {e}')
        st.stop()
    except Exception as e:
        st.error(f'Erreur lors de chargement :{e}')
        st.stop()
        
model,features = charger_model()

# en tete
st.markdown('''
            <style>
            .main-header{
               background: linear-gradient(135deg, #91BDF2 0%, #91BDF2 100%);
               padding:2.2rem;
               border-radius:50px;
               margin-bottom:2rem;
               text-align:center;
               border-shadow: 0 20px 50px rgba(0,0,0,0.1);
                }
            </style>
            ''',unsafe_allow_html=True)
st.markdown('''
            <div class='main-header'>
            <h1>🏦 Prédicteur la campagne de marketing</h1>
            <p style='font-size:20px;'>Développé par - <strong>Youssouf</strong> Assistant Intelligent</p>
            </div>
            
            ''',unsafe_allow_html=True)
# sidbar
st.markdown('''
            <style>
            .friendly-info {
                background: #e3f2fd;
                padding: 2rem;
                border-radius: 15px;
                border-left: 5px solid #2196F3;
                margin: 1.5rem 0;
            }
            .encouragement {
            background: linear-gradient(135deg, #fff3e0, #ffecb3);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 5px solid #ff9800;
        }
            </style>
            ''',unsafe_allow_html=True)
with st.sidebar:
    st.markdown("## 🤖 À propos de votre assistant")
    st.markdown("""
    <div class="friendly-info">
        <h4>Comment je fonctionne ?</h4>
        <p>• J'utilise un modèle d'IA entraîné sur des milliers de cas</p>
        <p>• Ma précision est d'environ 92%</p>
        <p>• Je respecte votre vie privée</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 💡 Rappel important")
    st.markdown("""
    <div class="encouragement">
        <p><strong>Gardez en tête :</strong></p>
        <p>✨ Je suis un outil d'aide, pas un agent de la campagne de marketing</p>
    </div>
    """, unsafe_allow_html=True)

# formulaire
st.markdown('''
            <h2 style='color:#343a40;text-align:center;margin-bottom:25px'> 📋 Informations du clients</h2>
            
            ''',unsafe_allow_html=True)
# --- Formulaire client ---
with st.form(key='formulaire_client'):
    # 🧍 Informations personnelles
    st.header("🧍 Informations personnelles")
    nom_client = st.text_input(
        '📝 Votre nom complet du client', 
        placeholder="Ex: Youssouf Mohamed ",
        help="Saisissez le nom complet du client"
    ).strip()
    Age = st.slider('🎂 Âge du client', 18, 100, 40)
    Income = st.slider('💰 Revenu annuel (en $)', 0, 200000, 50000, step=1000)
    Education = st.selectbox('🎓 Niveau d\'éducation', ['Education_base', 'Licence', 'Doctorat', 'Master', 'cycle_2'])
    Marital_Status = st.selectbox('💑 Statut marital', ['Celibataire', 'En_couple', 'Marie', 'Divorce', 'Veuf', 'Autre'])

    # 👶 Famille
    st.header("👶 Enfants")
    Kidhome = st.number_input('👶 Nombre d\'enfants à la maison', 0, 5, 0)
    Teenhome = st.number_input('🧒 Nombre d\'ados à la maison', 0, 5, 0)

    # 📅 Date d’enregistrement
    st.header("📅 Date d'enregistrement client")
    Dt_Customer = st.date_input("Date d'inscription", min_value=date(2000,1,1), value=date(2014,1,1))
    Day_Customer = Dt_Customer.day
    Month_Customer = Dt_Customer.month
    Year_Customer = Dt_Customer.year

    # 🛍️ Dépenses
    st.header("🛍️ Dépenses produits")
    MntWines = st.slider("🍷 Vin", 0, 1500, 300)
    MntFruits = st.slider("🍎 Fruits", 0, 300, 50)
    MntMeatProducts = st.slider("🍖 Viande", 0, 1500, 250)
    MntFishProducts = st.slider("🐟 Poisson", 0, 500, 100)
    MntSweetProducts = st.slider("🍬 Sucreries", 0, 300, 50)
    MntGoldProds = st.slider("🏅 Produits en or", 0, 500, 100)

    # 📦 Comportement d'achat
    st.header("📦 Comportement d'achat")
    NumDealsPurchases = st.slider("💼 Offres utilisées", 0, 15, 3)
    NumWebPurchases = st.slider("🛒 Achats en ligne", 0, 15, 5)
    NumCatalogPurchases = st.slider("📚 Achats catalogue", 0, 15, 2)
    NumStorePurchases = st.slider("🏪 Achats en magasin", 0, 15, 6)
    NumWebVisitsMonth = st.slider("🌐 Visites du site par mois", 0, 20, 4)

    # 📢 Campagnes marketing
    st.header("📢 Réponse aux campagnes précédentes")
    AcceptedCmp1 = st.checkbox("✔️ Campagne 1 acceptée")
    AcceptedCmp2 = st.checkbox("✔️ Campagne 2 acceptée")
    AcceptedCmp3 = st.checkbox("✔️ Campagne 3 acceptée")
    AcceptedCmp4 = st.checkbox("✔️ Campagne 4 acceptée")
    AcceptedCmp5 = st.checkbox("✔️ Campagne 5 acceptée")

    # ❗ Réclamations
    st.header("📞 Réclamations")
    Complain = st.radio("Client a-t-il porté plainte ?", [0, 1])

    # 📉 Récence (nombre de jours depuis dernier achat)
    st.header("📆 Récence")
    Recency = st.slider("⏳ Nombre de jours depuis dernier achat", 0, 100, 30)
    st.markdown('---')
    col_center = st.columns([1,2,1])
    with col_center[1]:
        submit = st.form_submit_button(
            'Prédire la probabilité de souscription', 
            type="primary", 
            use_container_width=True
        )
if submit:
    if not nom_client:
        st.warning('Veuillez renseigner le nom complet du client !')
    else:
        donnees_client = {colonne: 0 for colonne in features}
       # donnee numerique
        donnees_client['Income'] = Income
        donnees_client['Kidhome'] = Kidhome
        donnees_client['Teenhome'] = Teenhome
        donnees_client['Recency'] = Recency
        donnees_client['MntWines'] = MntWines
        donnees_client['MntFruits'] = MntFruits
        donnees_client['MntMeatProducts'] = MntMeatProducts
        donnees_client['MntFishProducts'] = MntFishProducts
        donnees_client['MntSweetProducts'] = MntSweetProducts
        donnees_client['MntGoldProds'] = MntGoldProds
        donnees_client['NumDealsPurchases'] = NumDealsPurchases
        donnees_client['NumWebPurchases'] = NumWebPurchases
        donnees_client['NumCatalogPurchases'] = NumCatalogPurchases
        donnees_client['NumStorePurchases'] = NumStorePurchases
        donnees_client['NumWebVisitsMonth'] = NumWebVisitsMonth
        donnees_client['AcceptedCmp3'] = AcceptedCmp3
        donnees_client['AcceptedCmp4'] = AcceptedCmp4
        donnees_client['AcceptedCmp5'] = AcceptedCmp5
        donnees_client['AcceptedCmp1'] = AcceptedCmp1
        donnees_client['AcceptedCmp2'] = AcceptedCmp2
        donnees_client['Complain'] = Complain
        donnees_client['Day_Customer'] = Day_Customer
        donnees_client['Month_Customer'] = Month_Customer
        donnees_client['Year_Customer'] = Year_Customer
        donnees_client['Age'] = Age
        # encodage
        Education_prof = f'Education_{Education}'
        if Education_prof in donnees_client:
            donnees_client[Education_prof] = 1
            
        colonne_Marital_Status = f'Marital_Status_{Marital_Status}'
        if colonne_Marital_Status in donnees_client:
            donnees_client[colonne_Marital_Status] = 1
            
        # creation data
        nouvelle_donnee = pd.DataFrame([
            [donnees_client[col] for col in features]
            ],columns=features)    
        try:
            prediction = model.predict(nouvelle_donnee)[0]
            proba = model.predict_proba(nouvelle_donnee)[0][1]
            st.markdown('---')
            st.markdown(f"""
            <div class="friendly-info">
                <h2>Résultat de l\'analyse pour {nom_client}</h2>
            </div>
            """, unsafe_allow_html=True)
            if prediction == 1:
                st.success(f'✅ **Prédiction positive** :{nom_client} a de forte chances de accempte la campagne ! ')
                conseil = '**Recommadation** : Contactez ce client rapidement , il présente un profil trés  favorable'
            else:
                st.warning(f'❌ **Prédiction Négative** :{nom_client} a peu  de chances de accempte la campagne  ! ')
                conseil = '**Recommadation** : ce client ne néccesite un approche commercial adapté ou cible'
            col_prob1,col_prob2 = st.columns([1,2])
            with col_prob1:
                delta_val = float(round(proba - 0.5,2))
                st.metric(
                    label='🎯 Probabilité de accepte',
                    value =f'{proba:.1%}',
                    delta=delta_val
                    )
                st.caption('Différence par rapport à une moyenne de 50 %')
            with col_prob2:
                couleur_barre = "#28a745" if proba > 0.5 else "#dc3545"
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px;">
                    <h5 style="margin-bottom: 10px; color: #495057;">Niveau de confiance</h5>
                    <div style="background-color: #e9ecef; border-radius: 25px; height: 20px; overflow: hidden;">
                        <div style="width: {proba*100}%; height: 100%; background-color: {couleur_barre}; 
                                   border-radius: 25px; transition: width 0.3s ease;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.info(conseil)
        except Exception as e:
             st.error(f"❌ Erreur lors de la prédiction : {str(e)}")
             st.info("💡 Veuillez vérifier que tous les champs sont correctement remplis.")     
         
# Message de conclusion plus chaleureux
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2.5rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 20px; margin-top: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <h4 style="color: #495057; margin-bottom: 1rem;">🏦' Votre Assistant Intelligente</h4>
    <p style="font-size: 1em; color: #6c757d; margin-bottom: 0.5rem;">
        Créé avec passion par <strong>Youssouf</strong> pour vous accompagner dans votre parcours santé
    </p>
    <p style="font-size: 0.9em; color: #6c757d; margin-bottom: 1rem;">
        Version 2024 - Mis à jour régulièrement pour votre bien-être
    </p>
    <div style="border-top: 1px solid #dee2e6; padding-top: 1rem;">
        <p style="font-size: 0.85em; color: #6c757d; font-style: italic;">
            ⚠️ Rappel important : Cet outil d'aide à la décision complète mais ne remplace jamais 
            l'expertise de votre agent
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

















    