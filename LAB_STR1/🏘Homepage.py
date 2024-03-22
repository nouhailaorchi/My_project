import streamlit as st

# Définir la configuration de la page
st.set_page_config(
    page_title="Simulation des Algorithmes d'Ordonnancement",
    page_icon="📊",
    layout="wide"
)



# Titre principal
st.title("Bienvenue dans notre projet de simulation des algorithmes d'ordonnancement")

# Sous-titre ou description
st.markdown(
    """
    Ce projet propose une simulation visuelle de différents algorithmes d'ordonnancement tels que FCFS , SJF ,  Rate Monotonic (RM),
    Deadline Monotonic (DM) et Least Laxity First (LLF). Vous pouvez configurer les paramètres des processus, exécuter
    l'algorithme sélectionné et visualiser le diagramme de Gantt résultant.
    """
)

# Séparation pour une meilleure lisibilité
st.markdown("---")



# Pied de page ou crédits
st.write(
    """
    Projet réalisé par ORCHI NOUHAILA  - BELHAJ SOUKAINA  - GUIDALI WIDAD 
    -----------ENSAJ_2023---------------
    """
)
