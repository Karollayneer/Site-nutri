import os  
from reportlab.pdfgen import canvas  # Importe a biblioteca reportlab  

def gerar_pdf_relatorio(paciente, pdf_path):  
    """Gera um relatório em PDF para o paciente."""  
    c = canvas.Canvas(pdf_path)  
    c.drawString(100, 750, f"Relatório do Paciente: {paciente['nome']}")  
    c.drawString(100, 730, f"Idade: {paciente['idade']}")  
    c.drawString(100, 710, f"Peso: {paciente['peso']} kg")  
    c.drawString(100, 690, f"Altura: {paciente['altura']} m")  
    c.save()  
    print(f"Relatório em PDF gerado para {paciente['nome']} em {pdf_path}")  

if __name__ == '__main__':  
    # Exemplo de uso da função  
    paciente_exemplo = {  
        'nome': 'Paciente Teste',  
        'idade': 30,  
        'peso': 75.5,  
        'altura': 1.75  
    }  
    pdf_path = 'relatorio_paciente_teste.pdf'  
    gerar_pdf_relatorio(paciente_exemplo, pdf_path)  