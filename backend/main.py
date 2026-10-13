from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fpdf import FPDF
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Production mein ise frontend URL se replace karna
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DocumentData(BaseModel):
    party_a: str
    party_b: str
    date: str
    amount: str

@app.post("/generate-nda")
def generate_nda(data: DocumentData):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Template Text
    text = f"""
    NON-DISCLOSURE AGREEMENT
    
    This Agreement is made on {data.date} between:
    1. {data.party_a} (Disclosing Party)
    2. {data.party_b} (Receiving Party)
    
    The parties agree to keep the project details and the agreed 
    amount of ${data.amount} strictly confidential.
    
    Signatures: _______________________
    """
    
    pdf.multi_cell(0, 10, txt=text)
    
    # Save to memory and return as file
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=nda_contract.pdf"})