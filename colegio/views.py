from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from datetime import datetime
import json
from graphql import graphql_sync

# Importar modelos y formularios
from .models import Area, Oficina, SalonClase, Persona
from .forms import AreaForm, OficinaForm, SalonClaseForm, PersonaForm
from colegio_project.schema import schema

# Vistas para Area
class AreaListView(ListView):
    model = Area
    template_name = 'colegio/area_list.html'
    context_object_name = 'areas'

class AreaCreateView(CreateView):
    model = Area
    form_class = AreaForm
    template_name = 'colegio/area_form.html'
    success_url = reverse_lazy('area-list')

class AreaUpdateView(UpdateView):
    model = Area
    form_class = AreaForm
    template_name = 'colegio/area_form.html'
    success_url = reverse_lazy('area-list')

class AreaDeleteView(DeleteView):
    model = Area
    template_name = 'colegio/area_confirm_delete.html'
    success_url = reverse_lazy('area-list')

# Vistas para Oficina
class OficinaListView(ListView):
    model = Oficina
    template_name = 'colegio/oficina_list.html'
    context_object_name = 'oficinas'

class OficinaCreateView(CreateView):
    model = Oficina
    form_class = OficinaForm
    template_name = 'colegio/oficina_form.html'
    success_url = reverse_lazy('oficina-list')

class OficinaUpdateView(UpdateView):
    model = Oficina
    form_class = OficinaForm
    template_name = 'colegio/oficina_form.html'
    success_url = reverse_lazy('oficina-list')

class OficinaDeleteView(DeleteView):
    model = Oficina
    template_name = 'colegio/oficina_confirm_delete.html'
    success_url = reverse_lazy('oficina-list')

# Vistas para SalonClase
class SalonClaseListView(ListView):
    model = SalonClase
    template_name = 'colegio/salonclase_list.html'
    context_object_name = 'salones'

class SalonClaseCreateView(CreateView):
    model = SalonClase
    form_class = SalonClaseForm
    template_name = 'colegio/salonclase_form.html'
    success_url = reverse_lazy('salonclase-list')

class SalonClaseUpdateView(UpdateView):
    model = SalonClase
    form_class = SalonClaseForm
    template_name = 'colegio/salonclase_form.html'
    success_url = reverse_lazy('salonclase-list')

class SalonClaseDeleteView(DeleteView):
    model = SalonClase
    template_name = 'colegio/salonclase_confirm_delete.html'
    success_url = reverse_lazy('salonclase-list')

# Vistas para Persona
class PersonaListView(ListView):
    model = Persona
    template_name = 'colegio/persona_list.html'
    context_object_name = 'personas'

class PersonaCreateView(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'colegio/persona_form.html'
    success_url = reverse_lazy('persona-list')

class PersonaUpdateView(UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'colegio/persona_form.html'
    success_url = reverse_lazy('persona-list')

class PersonaDeleteView(DeleteView):
    model = Persona
    template_name = 'colegio/persona_confirm_delete.html'
    success_url = reverse_lazy('persona-list')

# Vista para la página principal
def home_view(request):
    # Obtener estadísticas para mostrar en la página principal
    total_areas = Area.objects.count()
    total_oficinas = Oficina.objects.count()
    total_salones = SalonClase.objects.count()
    total_personas = Persona.objects.count()
    total_profesores = Persona.objects.filter(tipo='profesor').count()
    total_administrativos = Persona.objects.filter(tipo='administrativo').count()
    
    context = {
        'total_areas': total_areas,
        'total_oficinas': total_oficinas,
        'total_salones': total_salones,
        'total_personas': total_personas,
        'total_profesores': total_profesores,
        'total_administrativos': total_administrativos,
    }
    
    return render(request, 'colegio/home.html', context)

# Vista para el reporte de áreas
class ReporteAreaView(ListView):
    model = Area
    template_name = 'colegio/reporte_area.html'
    context_object_name = 'areas'
    
    def get_queryset(self):
        # Obtener todas las áreas con el conteo de empleados
        queryset = Area.objects.annotate(num_empleados=Count('empleados'))
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir información adicional al contexto
        total_profesores = Persona.objects.filter(tipo='profesor').count()
        total_administrativos = Persona.objects.filter(tipo='administrativo').count()
        total_empleados = Persona.objects.count()
        
        context.update({
            'total_profesores': total_profesores,
            'total_administrativos': total_administrativos,
            'total_empleados': total_empleados,
        })
        return context

# Vista para exportar reporte a PDF
def exportar_reporte_pdf(request):
    # Crear el objeto HttpResponse con el encabezado PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_areas.pdf"'
    
    # Crear el objeto PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Definir colores
    header_color = HexColor('#3498db')
    section_color = HexColor('#f2f2f2')
    
    # Función para encabezado de página
    def header_footer(canvas, doc):
        # Guardar el estado
        canvas.saveState()
        
        # Encabezado
        canvas.setFont('Helvetica-Bold', 16)
        canvas.setFillColor(header_color)
        canvas.drawString(inch, height - inch, "Reporte de Áreas y Empleados")
        
        # Fecha
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        canvas.setFont('Helvetica', 10)
        canvas.setFillColorRGB(0, 0, 0)
        canvas.drawString(width - 2.5*inch, height - inch, f"Fecha: {fecha}")
        
        # Línea separadora
        canvas.setStrokeColorRGB(0.8, 0.8, 0.8)
        canvas.line(inch, height - 1.2*inch, width - inch, height - 1.2*inch)
        
        # Pie de página
        canvas.setFont('Helvetica', 9)
        canvas.drawString(inch, 0.75*inch, "Colegio Cambridge - Sistema de Gestión")
        canvas.drawRightString(width - inch, 0.75*inch, f"Página {canvas.getPageNumber()}")
        
        # Restaurar el estado
        canvas.restoreState()
    
    # Dibujar encabezado y pie de página en la primera página
    header_footer(p, None)
    
    # Obtener datos
    areas = Area.objects.annotate(num_empleados=Count('empleados'))
    total_profesores = Persona.objects.filter(tipo='profesor').count()
    total_administrativos = Persona.objects.filter(tipo='administrativo').count()
    total_empleados = Persona.objects.count()
    
    # Posición inicial para el contenido
    y_position = height - 1.5*inch
    
    # Resumen general
    p.setFont('Helvetica-Bold', 12)
    p.setFillColor(header_color)
    p.drawString(inch, y_position, "Resumen General")
    y_position -= 0.3*inch
    
    # Tabla de resumen
    p.setFillColorRGB(0, 0, 0)
    p.setFont('Helvetica', 10)
    
    # Dibujar tabla de resumen
    resumen_data = [
        ["Total de Áreas", str(areas.count())],
        ["Total de Empleados", str(total_empleados)],
        ["Total de Profesores", str(total_profesores)],
        ["Total de Administrativos", str(total_administrativos)]
    ]
    
    # Configuración de la tabla
    table_width = 4*inch
    table_height = 0.25*inch
    col1_width = 2.5*inch
    col2_width = 1.5*inch
    
    # Dibujar encabezados de tabla
    p.setFillColor(section_color)
    p.rect(inch, y_position, table_width, table_height, fill=1)
    p.setFillColorRGB(0, 0, 0)
    p.setFont('Helvetica-Bold', 10)
    p.drawString(inch + 0.1*inch, y_position + 0.1*inch, "Concepto")
    p.drawString(inch + col1_width + 0.1*inch, y_position + 0.1*inch, "Cantidad")
    
    y_position -= table_height
    
    # Dibujar filas de datos
    p.setFont('Helvetica', 10)
    for row in resumen_data:
        p.rect(inch, y_position, table_width, table_height, fill=0)
        p.drawString(inch + 0.1*inch, y_position + 0.1*inch, row[0])
        p.drawString(inch + col1_width + 0.1*inch, y_position + 0.1*inch, row[1])
        y_position -= table_height
    
    y_position -= 0.3*inch
    
    # Detalle por área
    for area in areas:
        # Verificar si necesitamos una nueva página
        if y_position < 2*inch:
            p.showPage()
            header_footer(p, None)
            y_position = height - 1.5*inch
        
        # Encabezado de área
        p.setFont('Helvetica-Bold', 12)
        p.setFillColor(header_color)
        p.drawString(inch, y_position, f"{area.nombre} ({area.num_empleados} empleado{'s' if area.num_empleados != 1 else ''})")
        y_position -= 0.2*inch
        
        # Tabla de empleados
        empleados = area.empleados.all()
        
        if empleados:
            # Configuración de la tabla de empleados
            table_width = 6.5*inch
            table_height = 0.25*inch
            col_widths = [1.2*inch, 2*inch, 1.5*inch, 1.8*inch]
            
            # Encabezados de tabla
            headers = ["Documento", "Nombre", "Tipo", "Oficina"]
            
            p.setFillColor(section_color)
            p.rect(inch, y_position, table_width, table_height, fill=1)
            p.setFillColorRGB(0, 0, 0)
            p.setFont('Helvetica-Bold', 9)
            
            x_position = inch + 0.1*inch
            for i, header in enumerate(headers):
                p.drawString(x_position, y_position + 0.1*inch, header)
                x_position += col_widths[i]
            
            y_position -= table_height
            
            # Filas de datos
            p.setFont('Helvetica', 9)
            for empleado in empleados:
                # Verificar si necesitamos una nueva página
                if y_position < 1*inch:
                    p.showPage()
                    header_footer(p, None)
                    y_position = height - 1.5*inch
                    
                    # Re-dibujar encabezado de área
                    p.setFont('Helvetica-Bold', 12)
                    p.setFillColor(header_color)
                    p.drawString(inch, y_position, f"{area.nombre} (continuación)")
                    y_position -= 0.2*inch
                    
                    # Re-dibujar encabezados de tabla
                    p.setFillColor(section_color)
                    p.rect(inch, y_position, table_width, table_height, fill=1)
                    p.setFillColorRGB(0, 0, 0)
                    p.setFont('Helvetica-Bold', 9)
                    
                    x_position = inch + 0.1*inch
                    for i, header in enumerate(headers):
                        p.drawString(x_position, y_position + 0.1*inch, header)
                        x_position += col_widths[i]
                    
                    y_position -= table_height
                    p.setFont('Helvetica', 9)
                
                # Dibujar fila
                p.rect(inch, y_position, table_width, table_height, fill=0)
                
                x_position = inch + 0.1*inch
                p.drawString(x_position, y_position + 0.1*inch, empleado.documento)
                x_position += col_widths[0]
                
                p.drawString(x_position, y_position + 0.1*inch, empleado.nombre)
                x_position += col_widths[1]
                
                tipo_text = empleado.get_tipo_display()
                if empleado.tipo == 'profesor':
                    tipo_text += f" ({empleado.get_tipo_profesor_display()})"
                p.drawString(x_position, y_position + 0.1*inch, tipo_text)
                x_position += col_widths[2]
                
                p.drawString(x_position, y_position + 0.1*inch, empleado.oficina.codigo)
                
                y_position -= table_height
        else:
            p.setFont('Helvetica', 10)
            p.setFillColorRGB(0.5, 0.5, 0.5)
            p.drawString(inch, y_position, "No hay empleados asignados a esta área.")
            p.setFillColorRGB(0, 0, 0)
            y_position -= 0.2*inch
        
        y_position -= 0.2*inch
    
    # Cerrar el objeto PDF
    p.showPage()
    p.save()
    
    return response

# Vistas para GraphQL
def debug_schema(request):
    try:
        # Intentar obtener el esquema
        schema_str = str(schema)
        return JsonResponse({
            'status': 'ok',
            'schema': schema_str[:500] + '...' if len(schema_str) > 500 else schema_str
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)

def graphiql_interface(request):
    return render(request, 'graphene/graphiql.html')

@csrf_exempt
@require_http_methods(["POST"])
def graphql_endpoint(request):
    try:
        data = json.loads(request.body)
        query = data.get('query')
        variables = data.get('variables')
        
        result = graphql_sync(schema, query, variable_values=variables)
        
        response_data = {
            'data': result.data
        }
        
        if result.errors:
            response_data['errors'] = [str(error) for error in result.errors]
        
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({
            'errors': [str(e)]
        }, status=400)

def graphiql_online(request):
    return render(request, 'graphene/graphiql_online.html')