import streamlit as st
import PyPDF2
import pandas as pd
import io

// ... existing code ...

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
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total de Páginas no PDF", total_pages)
            with col2:
                st.metric("Total de NFs no PDF", len(nfs_pdf))
            with col3:
                st.metric("Total de NFs no Excel", len(nfs_excel))
            with col4:
                st.metric("NFs encontradas no PDF", len(nfs_presentes))
            with col5:
                st.metric("NFs ausentes", len(nfs_ausentes))

// ... rest of the existing code ...
