import streamlit as st
import requests
import pandas as pd

API = "http://localhost:8000"

st.set_page_config(
    page_title="E-commerce",
    layout="wide"
)

# =============================
# STATE
# =============================
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"


# =============================
# LOGIN
# =============================
def login_page():

    st.title("Login")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        response = requests.post(
            f"{API}/login",
            json={
                "email": email,
                "senha": senha
            }
        )

        user = response.json()

        if "error" not in user:
            st.session_state.user = user
            st.session_state.page = "app"
            st.rerun()
        else:
            st.error("Login inválido")

    if st.button("Cadastro"):
        st.session_state.page = "cadastro"
        st.rerun()


# =============================
# CADASTRO
# =============================
def cadastro_page():

    st.title("Cadastro")

    nome = st.text_input("Nome")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Criar conta"):

        requests.post(
            f"{API}/usuarios",
            json={
                "nome": nome,
                "email": email,
                "senha": senha
            }
        )

        st.success("Conta criada")
        st.session_state.page = "login"
        st.rerun()

    if st.button("Login"):
        st.session_state.page = "login"
        st.rerun()


# =============================
# APP
# =============================
def app():

    user = st.session_state.user

    pedidos = requests.get(
        f"{API}/pedidos/{user['id']}"
    ).json()

    st.sidebar.markdown(f"### 👤 {user['nome']}")
    st.sidebar.markdown(f"📦 Pedidos: {len(pedidos)}")
    st.sidebar.divider()

    if st.sidebar.button("Sair"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()

    menu = st.sidebar.selectbox(
        "Menu",
        ["Produtos", "Comprar", "Pedidos"] +
        (["Admin"] if user["role"] == "admin" else [])
    )

    # =============================
    # PRODUTOS
    # =============================
    if menu == "Produtos":

        st.title("Produtos")

        produtos = requests.get(f"{API}/produtos").json()

        df = pd.DataFrame(produtos)

        st.dataframe(df, use_container_width=True)


    # =============================
    # COMPRAR
    # =============================
    elif menu == "Comprar":

        st.title("Comprar")

        produtos = requests.get(f"{API}/produtos").json()

        produto_map = {
            f"{p['nome']} - R$ {p['preco']}": p["id"]
            for p in produtos
        }

        with st.form("buy"):

            item = st.selectbox("Produto", list(produto_map.keys()))
            qtd = st.number_input("Quantidade", min_value=1)

            if st.form_submit_button("Comprar"):

                response = requests.post(
                    f"{API}/pedidos",
                    json={
                        "uid": user["id"],
                        "pid": produto_map[item],
                        "qtd": qtd
                    }
                )

                if response.json().get("success"):
                    st.success("🛒 Compra realizada com sucesso!")
                    st.toast("Pedido confirmado", icon="✅")
                else:
                    st.error("Erro na compra")


    # =============================
    # PEDIDOS
    # =============================
    elif menu == "Pedidos":

        st.title("Meus pedidos")

        pedidos = requests.get(
            f"{API}/pedidos/{user['id']}"
        ).json()

        if not pedidos:
            st.info("Nenhum pedido")
        else:
            df = pd.DataFrame(pedidos)
            if "data" in df.columns:
                df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.strftime("%d/%m/%Y %H:%M:%S")
            st.dataframe(df, use_container_width=True, hide_index=True)
            total_gasto = sum([p["total"] for p in pedidos])
            st.markdown("---")
            st.metric("Total gasto", f"R$ {total_gasto:.2f}", delta=None)


    # =============================
    # ADMIN
    # =============================
    elif menu == "Admin":

        st.title("Admin")

        tab1, tab2, tab3 = st.tabs([
            "📦 Produtos",
            "📁 Categorias",
            "✏️ Editar"
        ])

        # -------------------------
        # PRODUTOS
        # -------------------------
        with tab1:

            st.subheader("➕ Criar Produto")

            categorias = requests.get(f"{API}/categorias").json()

            if not categorias:
                st.warning("Crie categorias primeiro!")
            else:

                cat_map = {c["nome"]: c["id"] for c in categorias}

                with st.form("create", clear_on_submit=True):

                    nome = st.text_input("Nome")
                    desc = st.text_area("Descrição")
                    preco = st.number_input("Preço", min_value=0.0)
                    estoque = st.number_input("Estoque", min_value=0)
                    cat = st.selectbox("Categoria", list(cat_map.keys()))

                    if st.form_submit_button("Criar Produto"):

                        requests.post(
                            f"{API}/produtos",
                            json={
                                "nome": nome,
                                "descricao": desc,
                                "preco": preco,
                                "estoque": estoque,
                                "categoria_id": cat_map[cat]
                            }
                        )

                        st.success("Produto criado!")
                        st.rerun()

                st.divider()

                st.subheader("Lista de Produtos")

                produtos = requests.get(f"{API}/produtos").json()

                df = pd.DataFrame(produtos)

                st.dataframe(df, use_container_width=True)


            # -------------------------
            # CATEGORIAS
            # -------------------------
            with tab2:

                st.subheader("Criar Categoria")

                col1, col2 = st.columns([3, 1])

                with col1:
                    nome = st.text_input("Nome da categoria", key="cat_input")

                with col2:
                    if st.button("➕ Criar", key="btn_cat"):
                        if nome.strip():
                            try:
                                response = requests.post(
                                    f"{API}/categorias",
                                    json={"nome": nome},
                                    timeout=5
                                )
                                if response.status_code in [200, 201]:
                                    st.success("✅ Categoria criada!")
                                    st.rerun()
                                else:
                                    st.error(f"Erro ao criar: {response.text}")
                            except Exception as e:
                                st.error(f"Erro de conexão: {e}")
                        else:
                            st.warning("Nome não pode ser vazio")

                st.divider()

                st.subheader("Lista de Categorias")

                try:
                    categorias = requests.get(f"{API}/categorias", timeout=5).json()
                    
                    if not categorias:
                        st.info("📭 Nenhuma categoria criada ainda")
                    else:
                        df = pd.DataFrame(categorias)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        st.caption(f"Total: {len(categorias)} categoria(s)")
                except Exception as e:
                    st.error(f"❌ Erro ao carregar categorias: {e}")


        # -------------------------
        # EDITAR
        # -------------------------
        with tab3:

            st.subheader("Editar Produtos")

            produtos = requests.get(f"{API}/produtos").json()

            if not produtos:
                st.info("Nenhum produto cadastrado")
            else:

                df = pd.DataFrame(produtos)

                st.dataframe(df, use_container_width=True)

                ids = [p["id"] for p in produtos]

                pid = st.selectbox("Produto", ids)

                prod = next(p for p in produtos if p["id"] == pid)

                categorias = requests.get(f"{API}/categorias").json()
                cat_map = {c["nome"]: c["id"] for c in categorias}

                with st.form("edit"):

                    nome = st.text_input("Nome", value=prod["nome"])
                    preco = st.number_input("Preço", value=float(prod["preco"]))
                    estoque = st.number_input("Estoque", value=int(prod["estoque"]))
                    cat = st.selectbox("Categoria", list(cat_map.keys()))

                    if st.form_submit_button("Salvar"):

                        requests.put(
                            f"{API}/produtos/{pid}",
                            json={
                                "nome": nome,
                                "descricao": "",
                                "preco": preco,
                                "estoque": estoque,
                                "categoria_id": cat_map[cat]
                            }
                        )

                        st.success("Atualizado!")
                        st.rerun()


# =============================
# ROUTER
# =============================
if st.session_state.page == "login":
    login_page()

elif st.session_state.page == "cadastro":
    cadastro_page()

elif st.session_state.page == "app":
    app()