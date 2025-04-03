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
    for linha in linhas:
        colunas = linha.split()
        if len(colunas) > 1:
            nfs_extraidas.add(colunas[1])
    return nfs_extraidas

def carregar_nfs_excel(excel_file):
    """Carrega a lista de NFs do arquivo Excel."""
    df = pd.read_excel(excel_file, usecols=[0], dtype=str)
    return set(df.iloc[:, 0].dropna().astype(str))

def main():
    st.title("Verificador de Notas Fiscais")
    st.write("Faça upload dos arquivos PDF e Excel para verificar as NFs.")

    # File uploaders
    pdf_file = st.file_uploader("Selecione o arquivo PDF", type=['pdf'])
    excel_file = st.file_uploader("Selecione o arquivo Excel", type=['xlsx', 'xls'])

    if pdf_file and excel_file:
        try:
            # Process files
            nfs_pdf = extrair_nfs_pdf(pdf_file)
            nfs_excel = carregar_nfs_excel(excel_file)
            
            # Find matches and differences
            nfs_presentes = nfs_excel.intersection(nfs_pdf)
            nfs_ausentes = nfs_excel - nfs_pdf
            
            # Display results
            st.subheader("Resultados")
            
            # Present NFs
            st.write("NFs encontradas no PDF:")
            if nfs_presentes:
                st.write(sorted(list(nfs_presentes)))
            else:
                st.write("Nenhuma NF encontrada no PDF")
            
            # Missing NFs
            st.write("NFs ausentes no PDF:")
            if nfs_ausentes:
                st.write(sorted(list(nfs_ausentes)))
            else:
                st.write("Todas as NFs estão presentes no PDF")
            
            # Statistics
            st.subheader("Estatísticas")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de NFs no Excel", len(nfs_excel))
            with col2:
                st.metric("NFs encontradas no PDF", len(nfs_presentes))
            with col3:
                st.metric("NFs ausentes", len(nfs_ausentes))
                
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar os arquivos: {str(e)}")

if __name__ == "__main__":
    main() 
