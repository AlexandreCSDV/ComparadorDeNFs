import streamlit as st
import PyPDF2
import pandas as pd
import io

def extrair_nfs_pdf(pdf_file):
    """Extrai as NFs do PDF."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    texto_pdf = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    
    linhas = texto_pdf.split("\n")
    nfs_extraidas = set()
    encontrou_nota = False
    
    for linha in linhas:
        # Procura pelo cabeçalho "Nota"
        if "Nota" in linha:
            encontrou_nota = True
            continue
            
        if encontrou_nota:
            # Tenta encontrar números que parecem NFs (1-9 dígitos)
            palavras = linha.split()
            for palavra in palavras:
                # Filtra apenas números com 1-9 dígitos
                if palavra.isdigit() and 1 <= len(palavra) <= 9:
                    nfs_extraidas.add(palavra)
    
    return nfs_extraidas, len(pdf_reader.pages)

def carregar_nfs_excel(excel_file):
    """Carrega a lista de NFs do arquivo Excel."""
    df = pd.read_excel(excel_file, usecols=[0], dtype=str)
    return set(df.iloc[:, 0].dropna().astype(str))

def main():
    st.set_page_config(page_title="Verificador de NFs", layout="wide")
    st.title("Verificador de Notas Fiscais")
    st.write("Faça upload dos arquivos PDF e Excel para verificar as NFs.")

    # File uploaders
    col1, col2 = st.columns(2)
    with col1:
        pdf_file = st.file_uploader("Selecione o arquivo PDF", type=['pdf'])
    with col2:
        excel_file = st.file_uploader("Selecione o arquivo Excel", type=['xlsx', 'xls'])

    if pdf_file and excel_file:
        try:
            # Process files
            nfs_pdf, total_pages = extrair_nfs_pdf(pdf_file)
            nfs_excel = carregar_nfs_excel(excel_file)
            
            # Find matches and differences
            nfs_presentes = nfs_excel.intersection(nfs_pdf)
            nfs_ausentes = nfs_excel - nfs_pdf
            
            # Display statistics
            st.subheader("Estatísticas")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total de Páginas no PDF", total_pages)
            with col2:
                st.metric("Total de NFs no Excel", len(nfs_excel))
            with col3:
                st.metric("NFs encontradas no PDF", len(nfs_presentes))
            with col4:
                st.metric("NFs ausentes", len(nfs_ausentes))
            
            # Display results in tabs
            tab1, tab2, tab3 = st.tabs(["NFs Encontradas", "NFs Ausentes", "Lista Completa"])
            
            with tab1:
                st.write("NFs encontradas no PDF:")
                if nfs_presentes:
                    st.write(sorted(list(nfs_presentes)))
                else:
                    st.write("Nenhuma NF encontrada no PDF")
            
            with tab2:
                st.write("NFs ausentes no PDF:")
                if nfs_ausentes:
                    st.write(sorted(list(nfs_ausentes)))
                else:
                    st.write("Todas as NFs estão presentes no PDF")
            
            with tab3:
                st.write("Lista completa de NFs no PDF:")
                if nfs_pdf:
                    st.write(sorted(list(nfs_pdf)))
                else:
                    st.write("Nenhuma NF encontrada no PDF")
            
            # Download buttons
            st.subheader("Exportar Resultados")
            col1, col2 = st.columns(2)
            
            with col1:
                if nfs_presentes:
                    df_presentes = pd.DataFrame(sorted(list(nfs_presentes)), columns=['NFs Encontradas'])
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df_presentes.to_excel(writer, index=False)
                    excel_buffer.seek(0)
                    st.download_button(
                        label="Download NFs Encontradas (Excel)",
                        data=excel_buffer,
                        file_name="nfs_encontradas.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            with col2:
                if nfs_ausentes:
                    df_ausentes = pd.DataFrame(sorted(list(nfs_ausentes)), columns=['NFs Ausentes'])
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df_ausentes.to_excel(writer, index=False)
                    excel_buffer.seek(0)
                    st.download_button(
                        label="Download NFs Ausentes (Excel)",
                        data=excel_buffer,
                        file_name="nfs_ausentes.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar os arquivos: {str(e)}")

if __name__ == "__main__":
    main()
