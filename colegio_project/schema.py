import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Count
from colegio.models import Area, Oficina, SalonClase, Persona

# Tipos GraphQL para cada modelo
class AreaType(DjangoObjectType):
    class Meta:
        model = Area
        fields = "__all__"
    
    num_empleados = graphene.Int()
    
    def resolve_num_empleados(self, info):
        return self.empleados.count()

class OficinaType(DjangoObjectType):
    class Meta:
        model = Oficina
        fields = "__all__"

class SalonClaseType(DjangoObjectType):
    class Meta:
        model = SalonClase
        fields = "__all__"

class PersonaType(DjangoObjectType):
    class Meta:
        model = Persona
        fields = "__all__"

# Query principal
class Query(graphene.ObjectType):
    # Consultas para listas
    areas = graphene.List(AreaType)
    oficinas = graphene.List(OficinaType)
    salones = graphene.List(SalonClaseType)
    personas = graphene.List(PersonaType)
    
    # Consultas para obtener por ID
    area = graphene.Field(AreaType, id=graphene.Int())
    oficina = graphene.Field(OficinaType, id=graphene.Int())
    salon = graphene.Field(SalonClaseType, id=graphene.Int())
    persona = graphene.Field(PersonaType, id=graphene.Int())
    
    # Consultas para reportes
    reporte_areas = graphene.List(AreaType)
    resumen_estadisticas = graphene.JSONString()
    
    # Resolvers para listas
    def resolve_areas(self, info):
        return Area.objects.all()
    
    def resolve_oficinas(self, info):
        return Oficina.objects.all()
    
    def resolve_salones(self, info):
        return SalonClase.objects.all()
    
    def resolve_personas(self, info):
        return Persona.objects.all()
    
    # Resolvers para obtener por ID
    def resolve_area(self, info, id):
        try:
            return Area.objects.get(pk=id)
        except Area.DoesNotExist:
            return None
    
    def resolve_oficina(self, info, id):
        try:
            return Oficina.objects.get(pk=id)
        except Oficina.DoesNotExist:
            return None
    
    def resolve_salon(self, info, id):
        try:
            return SalonClase.objects.get(pk=id)
        except SalonClase.DoesNotExist:
            return None
    
    def resolve_persona(self, info, id):
        try:
            return Persona.objects.get(pk=id)
        except Persona.DoesNotExist:
            return None
    
    # Resolvers para reportes
    def resolve_reporte_areas(self, info):
        return Area.objects.annotate(num_empleados=Count('empleados'))
    
    def resolve_resumen_estadisticas(self, info):
        total_areas = Area.objects.count()
        total_oficinas = Oficina.objects.count()
        total_salones = SalonClase.objects.count()
        total_personas = Persona.objects.count()
        total_profesores = Persona.objects.filter(tipo='profesor').count()
        total_administrativos = Persona.objects.filter(tipo='administrativo').count()
        
        return {
            'total_areas': total_areas,
            'total_oficinas': total_oficinas,
            'total_salones': total_salones,
            'total_personas': total_personas,
            'total_profesores': total_profesores,
            'total_administrativos': total_administrativos,
        }

# Mutaciones para crear
class CreateAreaMutation(graphene.Mutation):
    class Arguments:
        nombre = graphene.String(required=True)
    
    area = graphene.Field(AreaType)
    
    def mutate(self, info, nombre):
        area = Area(nombre=nombre)
        area.save()
        return CreateAreaMutation(area=area)

class CreateOficinaMutation(graphene.Mutation):
    class Arguments:
        codigo = graphene.String(required=True)
        area_id = graphene.Int(required=True)
    
    oficina = graphene.Field(OficinaType)
    
    def mutate(self, info, codigo, area_id):
        area = Area.objects.get(pk=area_id)
        oficina = Oficina(codigo=codigo, area=area)
        oficina.save()
        return CreateOficinaMutation(oficina=oficina)

class CreateSalonMutation(graphene.Mutation):
    class Arguments:
        codigo = graphene.String(required=True)
    
    salon = graphene.Field(SalonClaseType)
    
    def mutate(self, info, codigo):
        salon = SalonClase(codigo=codigo)
        salon.save()
        return CreateSalonMutation(salon=salon)

class CreatePersonaMutation(graphene.Mutation):
    class Arguments:
        documento = graphene.String(required=True)
        nombre = graphene.String(required=True)
        tipo = graphene.String(required=True)
        tipo_profesor = graphene.String(required=False)
        area_id = graphene.Int(required=True)
        oficina_id = graphene.Int(required=True)
    
    persona = graphene.Field(PersonaType)
    
    def mutate(self, info, documento, nombre, tipo, tipo_profesor, area_id, oficina_id):
        area = Area.objects.get(pk=area_id)
        oficina = Oficina.objects.get(pk=oficina_id)
        persona = Persona(
            documento=documento,
            nombre=nombre,
            tipo=tipo,
            tipo_profesor=tipo_profesor,
            area=area,
            oficina=oficina
        )
        persona.save()
        return CreatePersonaMutation(persona=persona)

# Mutaciones para actualizar
class UpdateAreaMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        nombre = graphene.String(required=True)
    
    area = graphene.Field(AreaType)
    
    def mutate(self, info, id, nombre):
        area = Area.objects.get(pk=id)
        area.nombre = nombre
        area.save()
        return UpdateAreaMutation(area=area)

class UpdateOficinaMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        codigo = graphene.String(required=True)
        area_id = graphene.Int(required=True)
    
    oficina = graphene.Field(OficinaType)
    
    def mutate(self, info, id, codigo, area_id):
        oficina = Oficina.objects.get(pk=id)
        area = Area.objects.get(pk=area_id)
        oficina.codigo = codigo
        oficina.area = area
        oficina.save()
        return UpdateOficinaMutation(oficina=oficina)

class UpdateSalonMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        codigo = graphene.String(required=True)
    
    salon = graphene.Field(SalonClaseType)
    
    def mutate(self, info, id, codigo):
        salon = SalonClase.objects.get(pk=id)
        salon.codigo = codigo
        salon.save()
        return UpdateSalonMutation(salon=salon)

class UpdatePersonaMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        documento = graphene.String(required=True)
        nombre = graphene.String(required=True)
        tipo = graphene.String(required=True)
        tipo_profesor = graphene.String(required=False)
        area_id = graphene.Int(required=True)
        oficina_id = graphene.Int(required=True)
    
    persona = graphene.Field(PersonaType)
    
    def mutate(self, info, id, documento, nombre, tipo, tipo_profesor, area_id, oficina_id):
        persona = Persona.objects.get(pk=id)
        area = Area.objects.get(pk=area_id)
        oficina = Oficina.objects.get(pk=oficina_id)
        
        persona.documento = documento
        persona.nombre = nombre
        persona.tipo = tipo
        persona.tipo_profesor = tipo_profesor
        persona.area = area
        persona.oficina = oficina
        
        persona.save()
        return UpdatePersonaMutation(persona=persona)

# Mutaciones para eliminar
class DeleteAreaMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    area = graphene.Field(AreaType)
    
    def mutate(self, info, id):
        area = Area.objects.get(pk=id)
        area.delete()
        return DeleteAreaMutation(area=area)

class DeleteOficinaMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    oficina = graphene.Field(OficinaType)
    
    def mutate(self, info, id):
        oficina = Oficina.objects.get(pk=id)
        oficina.delete()
        return DeleteOficinaMutation(oficina=oficina)

class DeleteSalonMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    salon = graphene.Field(SalonClaseType)
    
    def mutate(self, info, id):
        salon = SalonClase.objects.get(pk=id)
        salon.delete()
        return DeleteSalonMutation(salon=salon)

class DeletePersonaMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    persona = graphene.Field(PersonaType)
    
    def mutate(self, info, id):
        persona = Persona.objects.get(pk=id)
        persona.delete()
        return DeletePersonaMutation(persona=persona)

# Mutación principal
class Mutation(graphene.ObjectType):
    # Mutaciones para Áreas
    create_area = CreateAreaMutation.Field()
    update_area = UpdateAreaMutation.Field()
    delete_area = DeleteAreaMutation.Field()
    
    # Mutaciones para Oficinas
    create_oficina = CreateOficinaMutation.Field()
    update_oficina = UpdateOficinaMutation.Field()
    delete_oficina = DeleteOficinaMutation.Field()
    
    # Mutaciones para Salones
    create_salon = CreateSalonMutation.Field()
    update_salon = UpdateSalonMutation.Field()
    delete_salon = DeleteSalonMutation.Field()
    
    # Mutaciones para Personas
    create_persona = CreatePersonaMutation.Field()
    update_persona = UpdatePersonaMutation.Field()
    delete_persona = DeletePersonaMutation.Field()

# Esquema completo
schema = graphene.Schema(query=Query, mutation=Mutation)