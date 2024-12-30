import streamlit as st
import sqlite3

st.set_page_config(layout="wide")

# Connexion à la base de données SQLite
DB_PATH = "produits.db"

def init_db():
    """Initialise la base de données et crée la table si elle n'existe pas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produit TEXT NOT NULL,
            taille500ml INTEGER DEFAULT 0,
            taille1L INTEGER DEFAULT 0,
            taille4L INTEGER DEFAULT 0,
            taille10L INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_product(produit, taille500ml, taille1L, taille4L, taille10L):
    """Ajoute un produit dans la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produits (produit, taille500ml, taille1L, taille4L, taille10L)
        VALUES (?, ?, ?, ?, ?)
    """, (produit, taille500ml, taille1L, taille4L, taille10L))
    conn.commit()
    conn.close()

def get_products(order_by="id", order="ASC"):
    """Récupère tous les produits avec un tri."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM produits ORDER BY {order_by} {order}")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_product(product_id, produit, taille500ml, taille1L, taille4L, taille10L):
    """Met à jour un produit existant."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produits
        SET produit = ?, taille500ml = ?, taille1L = ?, taille4L = ?, taille10L = ?
        WHERE id = ?
    """, (produit, taille500ml, taille1L, taille4L, taille10L, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    """Supprime un produit."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produits WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# Initialisation de la base de données
init_db()

# Splash screen avec mot de passe
def show_login_screen():
    """Fonction pour afficher le splash screen avec mot de passe."""
    st.title("Page de Connexion")

    # Boîte de message pour le mot de passe
    password_input = st.empty()  # Espace vide pour afficher le champ de mot de passe

    # Champ de mot de passe
    password = password_input.text_input("Entrez le mot de passe", type="password")

    # Vérification du mot de passe
    if password == "cdc987654":  # Remplacer "votre_mot_de_passe" par le mot de passe réel
        password_input.empty()  # Masquer le champ de mot de passe après succès
        st.session_state.logged_in = True
        st.session_state.password_input = ""  # Effacer le mot de passe dans la session
        st.success("Connexion réussie!")
        return True
    elif password:
        password_input.text_input("Mot de passe incorrect. Essayez à nouveau.", type="password", key="incorrect_password")
        
    return False

# Vérification si l'utilisateur est connecté
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    if not show_login_screen():
        st.stop()  # Arrêter l'exécution si la connexion n'est pas réussie

# Interface principale (cachée avant la connexion)
if st.session_state.logged_in:
    # Interface principale après connexion
    st.title("Gestion des Produits")

    # Ajout d'un produit
    with st.form("add_product_form", clear_on_submit=True):
        st.subheader("Ajouter un produit")

        # Utilisation de st.columns pour organiser les champs sur la même ligne
        col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 2])

        produit = col1.text_input("Nom du produit", max_chars=100)
        taille500ml = col2.number_input("Quantité 500ml", min_value=0, step=1, value=0)
        taille1L = col3.number_input("Quantité 1L 2L", min_value=0, step=1, value=0)
        taille4L = col4.number_input("Quantité 4L", min_value=0, step=1, value=0)
        taille10L = col5.number_input("Quantité 10L", min_value=0, step=1, value=0)

        submitted = st.form_submit_button("Ajouter")
        if submitted and produit:
            add_product(produit, taille500ml, taille1L, taille4L, taille10L)
            st.success("Produit ajouté avec succès !")

    # Affichage des produits sous forme de tableau
    st.subheader("Liste des produits")

    # Récupérer les produits triés par défaut (par id, ASC)
    products = get_products(order_by="id", order="ASC")

    if products:
        for product in products:
            # Créer une ligne dans le tableau avec les champs modifiables et les boutons
            col1, col2, col3, col4, col5, col6, col7 = st.columns([18, 13, 13, 13, 13, 10, 10])

            # Champs modifiables dans le tableau
            produit = col1.text_input("Nom du produit", value=product[1], key=f"produit_{product[0]}")
            taille500ml = col2.number_input("Quantité 500ml", min_value=0, step=1, value=product[2], key=f"taille500ml_{product[0]}")
            taille1L = col3.number_input("Quantité 1L 2L", min_value=0, step=1, value=product[3], key=f"taille1L_{product[0]}")
            taille4L = col4.number_input("Quantité 4L", min_value=0, step=1, value=product[4], key=f"taille4L_{product[0]}")
            taille10L = col5.number_input("Quantité 10L", min_value=0, step=1, value=product[5], key=f"taille10L_{product[0]}")

            # Boutons de mise à jour et de suppression sur la même ligne
            update = col6.button("Mettre à jour", key=f"update_{product[0]}")
            delete = col7.button("Supprimer", key=f"delete_{product[0]}")

            if update:
                update_product(product[0], produit, taille500ml, taille1L, taille4L, taille10L)
                st.success(f"Produit {product[0]} mis à jour avec succès !")
            if delete:
                delete_product(product[0])
                st.warning(f"Produit {product[0]} supprimé !")

    else:
        st.info("Aucun produit trouvé.")

