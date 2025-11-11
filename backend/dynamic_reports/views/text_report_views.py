from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import time
from ..utils.report_parser import ReportParser
from ..utils.query_builder import QueryBuilder
from ..utils.pdf_generator import PDFGenerator
from ..utils.excel_generator import ExcelGenerator
from backend.commercial.models import ReporteGenerado

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_text_report(request):
    """
    CU6 - Generar Reporte Dinámico por Texto
    """
    try:
        prompt = request.data.get('prompt')
        formato = request.data.get('formato', 'JSON')
        
        if not prompt:
            return Response(
                {'error': 'El prompt es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        start_time = time.time()
        
        # Parsear el comando
        parser = ReportParser()
        parsed_command = parser.parse_command(prompt)
        
        # Construir y ejecutar la consulta
        query_builder = QueryBuilder()
        query = query_builder.build_query(parsed_command)
        results = query_builder.execute_query(query)
        
        execution_time = time.time() - start_time
        
        # Guardar en base de datos
        reporte = ReporteGenerado.objects.create(
            usuario=request.user,
            prompt=prompt,
            formato_solicitado=formato,
            consulta_sql=query,
            resultado=results,
            tiempo_ejecucion=execution_time
        )
        
        # Generar respuesta según el formato
        if formato == 'PDF':
            pdf_generator = PDFGenerator()
            return pdf_generator.create_pdf_response(
                results, parsed_command, results,
                filename=f"reporte_{reporte.id}.pdf"
            )
        
        elif formato == 'EXCEL':
            excel_generator = ExcelGenerator()
            return excel_generator.create_excel_response(
                results, parsed_command, results,
                filename=f"reporte_{reporte.id}.xlsx"
            )
        
        else:  # JSON para vista en pantalla
            return Response({
                'message': 'Reporte generado exitosamente',
                'reporte_id': reporte.id,
                'datos': results,
                'consulta': query,
                'tiempo_ejecucion': execution_time,
                'comando_interpretado': parsed_command
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response(
            {'error': f'Error generando reporte: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_report_history(request):
    """
    Obtener historial de reportes del usuario
    """
    try:
        reportes = ReporteGenerado.objects.filter(usuario=request.user).order_by('-fecha_creacion')[:50]
        
        data = []
        for reporte in reportes:
            data.append({
                'id': reporte.id,
                'prompt': reporte.prompt,
                'formato': reporte.formato_solicitado,
                'fecha_creacion': reporte.fecha_creacion,
                'tiempo_ejecucion': reporte.tiempo_ejecucion,
                'cantidad_resultados': len(reporte.resultado) if reporte.resultado else 0
            })
        
        return Response({'reportes': data}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Error obteniendo historial: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )