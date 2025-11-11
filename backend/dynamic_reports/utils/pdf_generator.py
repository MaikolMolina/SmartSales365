from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.http import HttpResponse
import json
from datetime import datetime

class PDFGenerator:
    """
    Genera reportes en formato PDF
    """
    
    def generate_pdf(self, data, parsed_command, query_results):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            textColor=colors.darkblue
        )
        
        elements = []
        
        # Título
        title = Paragraph(f"Reporte de {parsed_command['report_type'].title()}", title_style)
        elements.append(title)
        
        # Información del reporte
        info_style = styles['Normal']
        elements.append(Paragraph(f"<b>Comando:</b> {parsed_command['original_command']}", info_style))
        elements.append(Paragraph(f"<b>Generado:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", info_style))
        elements.append(Spacer(1, 20))
        
        # Tabla de datos
        if query_results:
            table_data = self._prepare_table_data(query_results)
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
        else:
            elements.append(Paragraph("No se encontraron datos para el reporte", info_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def _prepare_table_data(self, query_results):
        if not query_results:
            return [['No hay datos']]
        
        # Encabezados
        headers = list(query_results[0].keys())
        table_data = [headers]
        
        # Datos
        for row in query_results:
            table_data.append([str(row[header]) for header in headers])
        
        return table_data
    
    def create_pdf_response(self, data, parsed_command, query_results, filename=None):
        pdf_buffer = self.generate_pdf(data, parsed_command, query_results)
        
        if not filename:
            filename = f"reporte_{parsed_command['report_type']}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response