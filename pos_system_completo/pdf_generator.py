"""
Módulo de generación de recibos y tickets en PDF
Utiliza ReportLab para diseñar documentos limpios optimizados para impresoras térmicas o carta.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from database import Sale, Business

def generate_sale_receipt_pdf(sale_id, output_dir="static/receipts"):
    """
    Genera un recibo de venta en PDF para una venta específica.
    Retorna la ruta del archivo generado.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sale = Sale.query.get(sale_id)
    if not sale:
        return None

    business = Business.query.get(sale.business_id)
    business_name = business.name if business else "Sistema POS"

    filename = f"recibo_venta_{sale.id}.pdf"
    filepath = os.path.join(output_dir, filename)

    # Configuración del documento (tamaño carta con márgenes estrechos estilo ticket)
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightWidth=30,
        leftWidth=30,
        topMargin=30,
        bottomMargin=30
    )

    story = []
    styles = getSampleStyleSheet()

    # Estilos personalizados
    title_style = ParagraphStyle(
        'ReceiptTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=1, # Centrado
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'ReceiptSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=12
    )

    body_style = ParagraphStyle(
        'ReceiptBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    bold_body_style = ParagraphStyle(
        'ReceiptBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    # Encabezado del Negocio
    story.append(Paragraph(business_name, title_style))
    story.append(Paragraph("Comprobante de Venta / Ticket", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))

    # Información general de la venta
    story.append(Paragraph(f"<b>Folio de Venta:</b> #{sale.id}", body_style))
    story.append(Paragraph(f"<b>Fecha y Hora:</b> {sale.sale_date.strftime('%d/%m/%Y %H:%M:%S')}", body_style))
    story.append(Paragraph(f"<b>Método de Pago:</b> {sale.payment_method.capitalize()}", body_style))
    story.append(Spacer(1, 10))

    # Tabla de productos
    table_data = [["Cant.", "Descripción", "P. Unit", "Subtotal"]]

    for item in sale.items:
        product_name = item.product.name if item.product else "Producto"
        table_data.append([
            str(item.quantity),
            product_name,
            f"${item.unit_price:.2f}",
            f"${item.subtotal:.2f}"
        ])

    t = Table(table_data, colWidths=[40, 240, 70, 70])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#cbd5e1')),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.HexColor('#cbd5e1')),
    ]))

    story.append(t)
    story.append(Spacer(1, 10))

    # Totales
    story.append(Paragraph(f"<b>Total a Pagar:</b> ${sale.total_amount:.2f}", bold_body_style))
    
    if sale.payment_method == 'efectivo' and sale.cash_received:
        story.append(Paragraph(f"<b>Efectivo Recibido:</b> ${sale.cash_received:.2f}", body_style))
        story.append(Paragraph(f"<b>Cambio Entregado:</b> ${sale.change:.2f}", body_style))

    story.append(Spacer(1, 20))
    story.append(Paragraph("¡Gracias por su compra!", ParagraphStyle('Footer', parent=subtitle_style, fontSize=11, fontName='Helvetica-Bold')))

    doc.build(story)
    return filepath
