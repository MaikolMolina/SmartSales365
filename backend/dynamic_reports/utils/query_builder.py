from django.db import connection
from datetime import datetime
from backend.commercial.models import Venta, Producto, Cliente

class QueryBuilder:
    
    def build_query(self, parsed_command):
        report_type = parsed_command['report_type']
        
        if report_type == 'ventas':
            return self._build_sales_query(parsed_command)
        elif report_type == 'productos':
            return self._build_products_query(parsed_command)
        elif report_type == 'clientes':
            return self._build_clients_query(parsed_command)
        return self._build_sales_query(parsed_command)
    
    def _build_sales_query(self, parsed_command):
        date_range = parsed_command['date_range']
        group_by = parsed_command['group_by']

        where_conditions = []
        if date_range:
            if len(date_range) >= 1:
                start = date_range[0]
                if isinstance(start, datetime):
                    start = start.strftime('%Y-%m-%d')
                where_conditions.append(f"v.fecha_venta >= '{start}'")
            if len(date_range) >= 2:
                end = date_range[1]
                if isinstance(end, datetime):
                    end = end.strftime('%Y-%m-%d')
                where_conditions.append(f"v.fecha_venta <= '{end}'")
        
        # Query base
        query = """
        SELECT 
            v.id,
            v.fecha_venta as fecha,
            c.nombre as cliente_nombre,
            p.nombre as producto_nombre,
            v.cantidad,
            v.precio_unitario,
            v.total as monto_total
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN productos p ON v.producto_id = p.id
        """
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)

        # Agrupamientos
        if group_by == 'producto':
            query = f"""
            SELECT 
                p.nombre as producto_nombre,
                COUNT(v.id) as total_ventas,
                SUM(v.cantidad) as total_unidades,
                SUM(v.total) as monto_total
            FROM ventas v
            JOIN productos p ON v.producto_id = p.id
            """
            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)
            query += " GROUP BY p.id, p.nombre"
        
        elif group_by == 'cliente':
            query = f"""
            SELECT 
                c.nombre as cliente_nombre,
                COUNT(v.id) as total_compras,
                SUM(v.total) as monto_total
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.id
            """
            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)
            query += " GROUP BY c.id, c.nombre"
        
        elif group_by == 'mes':
            query = f"""
            SELECT 
                DATE_TRUNC('month', v.fecha_venta) as mes,
                COUNT(v.id) as total_ventas,
                SUM(v.cantidad) as total_unidades,
                SUM(v.total) as monto_total
            FROM ventas v
            """
            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)
            query += " GROUP BY mes ORDER BY mes"

        return query
    
    def _build_products_query(self, parsed_command):
        return """
        SELECT 
            p.nombre,
            cat.nombre as categoria,
            p.precio,
            p.stock,
            COUNT(v.id) as total_ventas,
            COALESCE(SUM(v.cantidad), 0) as unidades_vendidas
        FROM productos p
        LEFT JOIN categorias cat ON p.categoria_id = cat.id
        LEFT JOIN ventas v ON p.id = v.producto_id
        GROUP BY p.id, p.nombre, cat.nombre, p.precio, p.stock
        """
    
    def _build_clients_query(self, parsed_command):
        return """
        SELECT 
            c.nombre,
            c.email,
            c.telefono,
            COUNT(v.id) as total_compras,
            COALESCE(SUM(v.total), 0) as monto_total
        FROM clientes c
        LEFT JOIN ventas v ON c.id = v.cliente_id
        GROUP BY c.id, c.nombre, c.email, c.telefono
        """
    
    def execute_query(self, query):
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            results = []
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                # Convertir Decimal a float
                for key, value in row_dict.items():
                    if hasattr(value, '__class__') and value.__class__.__name__ == 'Decimal':
                        row_dict[key] = float(value)
                results.append(row_dict)
            return results
