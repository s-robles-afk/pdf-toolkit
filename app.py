import streamlit as st
from pypdf import PdfReader

# Configuración de la página
st.set_page_config(page_title="PDF Toolkit", page_icon="📄")

st.title("📄 PDF Toolkit")
st.write("Una herramienta simple para leer, combinar y crear archivos PDF.")

# --- SECCIÓN 1: Leer y extraer texto de un PDF ---
st.header("1. Leer texto de un PDF")

archivo_subido = st.file_uploader("Sube un archivo PDF", type="pdf")

if archivo_subido is not None:
    lector = PdfReader(archivo_subido)
    texto_completo = ""

    for pagina in lector.pages:
        texto_completo += pagina.extract_text()

    st.subheader("Texto extraído:")
    st.text_area("Contenido del PDF", texto_completo, height=300)

# --- SECCIÓN 2: Combinar varios PDFs ---
st.header("2. Combinar varios PDFs en uno")

archivos_a_combinar = st.file_uploader(
    "Sube dos o más PDFs para combinar",
    type="pdf",
    accept_multiple_files=True,
    key="combinar")

if archivos_a_combinar and len(archivos_a_combinar) >= 2:
    from pypdf import PdfWriter

    escritor = PdfWriter()

    for archivo in archivos_a_combinar:
        lector_temp = PdfReader(archivo)
        for pagina in lector_temp.pages:
            escritor.add_page(pagina)

    # Guardamos el PDF combinado en memoria
    import io
    buffer_salida = io.BytesIO()
    escritor.write(buffer_salida)
    buffer_salida.seek(0)

    st.success(f"¡{len(archivos_a_combinar)} PDFs combinados exitosamente!")

    st.download_button(
        label="Descargar PDF combinado",
        data=buffer_salida,
        file_name="pdf_combinado.pdf",
        mime="application/pdf")    

    # --- SECCIÓN 3: Crear un PDF desde texto ---
st.header("3. Crear un PDF desde texto")

texto_usuario = st.text_area("Escribe el contenido de tu PDF aquí:", height=200, key="crear_texto")
nombre_archivo = st.text_input("Nombre del archivo (sin .pdf):", value="mi_documento")

if st.button("Generar PDF"):
    if texto_usuario.strip() == "":
        st.warning("Escribe algo de texto antes de generar el PDF.")
    else:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import io

        buffer_pdf = io.BytesIO()
        c = canvas.Canvas(buffer_pdf, pagesize=letter)

        ancho, alto = letter
        y = alto - 50  # margen superior
        margen_izquierdo = 50
        max_ancho_linea = 90  # caracteres aprox por línea

        # Dividimos el texto en líneas para que no se salga de la página
        lineas = []
        for parrafo in texto_usuario.split("\n"):
            while len(parrafo) > max_ancho_linea:
                lineas.append(parrafo[:max_ancho_linea])
                parrafo = parrafo[max_ancho_linea:]
            lineas.append(parrafo)

        for linea in lineas:
            if y < 50:  # si se acaba la página, crea una nueva
                c.showPage()
                y = alto - 50
            c.drawString(margen_izquierdo, y, linea)
            y -= 15

        c.save()
        buffer_pdf.seek(0)

        st.success("¡PDF generado exitosamente!")

        st.download_button(
            label="Descargar PDF",
            data=buffer_pdf,
            file_name=f"{nombre_archivo}.pdf",
            mime="application/pdf"
    )