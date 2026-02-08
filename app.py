import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import PyPDF2

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(
    page_title="Invoice AI",
    layout="centered"
)

# ----------------------
# TITLE
# ----------------------
st.title("📄 Invoice AI")
st.write("Upload a scanned PDF invoice, read it, and download a printable version.")

# ----------------------
# FILE UPLOAD
# ----------------------
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# ----------------------
# READ PDF TEXT
# ----------------------
def read_pdf_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# ----------------------
# CREATE PRINTABLE PDF
# ----------------------
def create_printable_pdf(text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x = 40
    y = height - 40

    for line in text.split("\n"):
        if y < 40:
            c.showPage()
            y = height - 40
        c.drawString(x, y, line[:100])
        y -= 14

    c.save()
    buffer.seek(0)
    return buffer

# ----------------------
# MAIN LOGIC
# ----------------------
if uploaded_file:
    st.success("PDF selected")

    if st.button("Read invoice"):
        with st.spinner("Reading invoice..."):
            text = read_pdf_text(uploaded_file)

        st.subheader("📄 Extracted text")
        st.text(text[:4000])

        printable_pdf = create_printable_pdf(text)
 
        st.download_button(
            label="⬇️ Download & Print PDF",
            data=printable_pdf,
            file_name="invoice_printable.pdf",
            mime="application/pdf"
        )
