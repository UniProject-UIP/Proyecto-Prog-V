import streamlit as st # type: ignore
import requests # type: ignore

st.set_page_config(page_title="Asistente Vocacional de la UIP", layout="centered")
st.title("Asistente Vocacional UIP")
st.write("Ingresa tus intereses, habilidades y metas para obtener una recomendación de carrera universitaria.")

with st.form("career_form"):
    interests = st.text_area("Intereses", placeholder="¿Qué te interesa?")
    skills = st.text_area("Habilidades", placeholder="¿En qué eres bueno?")
    goals = st.text_area("Metas", placeholder="¿Qué te gustaría lograr a futuro?")
    submitted = st.form_submit_button("Obtener recomendación")

if submitted:
    if not (interests and skills and goals):
        st.warning("Por favor completa todos los campos.")
    else:
        with st.spinner("Analizando tus respuestas..."):
            try:
                response = requests.post(
                    "https://your-api-gateway-url/career-advice",
                    json={"interests": interests, "skills": skills, "goals": goals},
                )
                data = response.json()

                if response.status_code == 200:
                    st.success("¡Aquí tienes tu recomendación")
                    st.markdown(f"**Carrera sugerida:** {data.get('career', 'N/A')}")
                    st.markdown(f"**Descripción:** {data.get('description', 'N/A')}")
                    st.markdown(f"**Razón de la recomendación:** {data.get('reason', 'N/A')}")
                else:
                    st.error(f"Error del servidor: {data.get('detail', 'Intenta más tarde.')}")

            except Exception as e:
                st.error("Ocurrió un error al conectarse con el servidor.")
                st.exception(e)
