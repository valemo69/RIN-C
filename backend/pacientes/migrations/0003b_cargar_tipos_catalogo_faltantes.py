from django.db import migrations

# ==========================================================
# POR QUÉ EXISTE ESTA MIGRACIÓN
# ==========================================================
#
# La migración 0004_cargar_catalogos_basicos carga ítems de
# Catálogo (por ejemplo "DNI" o "Activo") para los tipos
# TIPO_DOCUMENTO y ESTADO_VITAL. El problema es que esos DOS
# TIPOS DE CATÁLOGO nunca se crean: la migración 0003 sólo crea
# PROCEDENCIA, DESTINO_EGRESO, SECTOR, COMORBILIDAD, etc, pero
# no TIPO_DOCUMENTO ni ESTADO_VITAL. Tampoco crea SEXO ni
# COBERTURA, que hacen falta para que el formulario de Paciente
# tenga opciones para elegir.
#
# Por eso, al correr "migrate" en una base de datos nueva, la
# migración 0004 explota con:
#   TipoCatalogo.DoesNotExist: TipoCatalogo matching query does not exist.
#
# Esta migración se inserta ENTRE 0003 y 0004 (mirá el campo
# "dependencies" de 0004_cargar_catalogos_basicos.py, que ahora
# depende de esta) para crear esos 4 tipos de catálogo que
# faltaban, antes de que 0004 intente usarlos.


def cargar_tipos_catalogo_faltantes(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")

    tipos = [
        (10, "TIPO_DOCUMENTO", "Tipo de documento", True),
        (20, "SEXO", "Sexo", True),
        (30, "COBERTURA", "Cobertura", False),
        (40, "ESTADO_VITAL", "Estado vital", True),
        (50, "MOTIVO_INFECCIOSO", "Motivo infeccioso", False),
        (60, "MOTIVO_OBSTRUCTIVO", "Motivo obstructivo", False),
        (70, "MOTIVO_INTERSTICIAL", "Motivo intersticial", False),
        (80, "MOTIVO_PLEURAL", "Motivo pleural", False),
        (90, "MOTIVO_VASCULAR", "Motivo vascular", False),
        (100, "MOTIVO_ONCOLOGICO", "Motivo oncológico", False),
        (110, "MOTIVO_OTROS", "Otros motivos", False),
    ]

    for orden, codigo, nombre, protegido in tipos:
        TipoCatalogo.objects.get_or_create(
            codigo=codigo,
            defaults={
                "nombre": nombre,
                "descripcion": "",
                "orden": orden,
                "protegido": protegido,
                "activo": True,
            },
        )


def deshacer(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")

    TipoCatalogo.objects.filter(
        codigo__in=[
            "TIPO_DOCUMENTO",
            "SEXO",
            "COBERTURA",
            "ESTADO_VITAL",
            "MOTIVO_INFECCIOSO",
            "MOTIVO_OBSTRUCTIVO",
            "MOTIVO_INTERSTICIAL",
            "MOTIVO_PLEURAL",
            "MOTIVO_VASCULAR",
            "MOTIVO_ONCOLOGICO",
            "MOTIVO_OTROS",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0003_cargar_tipos_catalogo"),
    ]

    operations = [
        migrations.RunPython(
            cargar_tipos_catalogo_faltantes,
            deshacer,
        ),
    ]
