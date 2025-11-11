import re
from datetime import datetime, timedelta
import calendar

class ReportParser:
    """
    Parser para interpretar comandos de texto naturales y convertirlos en consultas
    """
    
    def __init__(self):
        self.keywords = {
            'ventas': ['venta', 'ventas', 'compras', 'transacciones'],
            'productos': ['producto', 'productos', 'artículos', 'items'],
            'clientes': ['cliente', 'clientes', 'compradores'],
            'periodos': ['mes', 'año', 'semana', 'día', 'periodo', 'fecha'],
            'agrupaciones': ['agrupar', 'por', 'agrupado', 'grupo'],
            'formatos': ['pdf', 'excel', 'json', 'pantalla']
        }
    
    def parse_command(self, command):
        command_lower = command.lower()
        
        report_type = self._extract_report_type(command_lower)
        date_range = self._extract_dates(command_lower)
        group_by = self._extract_group_by(command_lower)
        output_format = self._extract_format(command_lower)
        fields = self._extract_fields(command_lower)
        
        return {
            'report_type': report_type,
            'date_range': date_range,
            'group_by': group_by,
            'output_format': output_format,
            'fields': fields,
            'original_command': command
        }
    
    def _extract_report_type(self, command):
        if any(word in command for word in self.keywords['ventas']):
            return 'ventas'
        elif any(word in command for word in self.keywords['productos']):
            return 'productos'
        elif any(word in command for word in self.keywords['clientes']):
            return 'clientes'
        return 'ventas'
    
    def _extract_dates(self, command):
        dates = []

        # DD/MM/YYYY
        matches = re.findall(r'(\d{1,2})/(\d{1,2})/(\d{4})', command)
        for d, m, y in matches:
            try:
                dates.append(datetime(int(y), int(m), int(d)))
            except:
                pass

        # YYYY-MM-DD
        matches = re.findall(r'(\d{4})-(\d{1,2})-(\d{1,2})', command)
        for y, m, d in matches:
            try:
                dates.append(datetime(int(y), int(m), int(d)))
            except:
                pass

        # Mes de septiembre
        matches = re.findall(r'mes de (\w+)', command)
        for month_name in matches:
            try:
                month = list(calendar.month_name).index(month_name.capitalize())
                start = datetime(datetime.now().year, month, 1)
                last_day = calendar.monthrange(datetime.now().year, month)[1]
                end = datetime(datetime.now().year, month, last_day)
                dates.extend([start, end])
            except:
                pass

        # 15 de septiembre
        matches = re.findall(r'(\d{1,2}) de (\w+)', command)
        for day_str, month_name in matches:
            try:
                day = int(day_str)
                month = list(calendar.month_name).index(month_name.capitalize())
                date_obj = datetime(datetime.now().year, month, day)
                dates.append(date_obj)
            except:
                pass

        # Fechas relativas
        if not dates:
            if 'ayer' in command:
                dates.append(datetime.now() - timedelta(days=1))
            elif 'hoy' in command:
                dates.append(datetime.now())
            elif 'semana' in command:
                dates.extend([datetime.now() - timedelta(days=7), datetime.now()])
            elif 'mes' in command and 'este' in command:
                start = datetime.now().replace(day=1)
                end = datetime.now()
                dates.extend([start, end])
            elif 'año' in command and 'este' in command:
                start = datetime.now().replace(month=1, day=1)
                end = datetime.now()
                dates.extend([start, end])

        return dates[:2]
    
    def _extract_group_by(self, command):
        if 'agrupar por producto' in command or 'agrupado por producto' in command:
            return 'producto'
        elif 'agrupar por cliente' in command or 'agrupado por cliente' in command:
            return 'cliente'
        elif 'agrupar por mes' in command or 'agrupado por mes' in command:
            return 'mes'
        elif 'agrupar por categoría' in command or 'agrupado por categoría' in command:
            return 'categoria'
        return None
    
    def _extract_format(self, command):
        if 'pdf' in command:
            return 'PDF'
        elif 'excel' in command:
            return 'EXCEL'
        return 'JSON'
    
    def _extract_fields(self, command):
        fields = []
        if 'nombre' in command and 'cliente' in command:
            fields.append('cliente_nombre')
        if 'monto' in command or 'total' in command:
            fields.append('monto_total')
        if 'cantidad' in command:
            fields.append('cantidad')
        if 'fecha' in command:
            fields.append('fecha')
        return fields if fields else ['*']
