from django.db import migrations

# ==========================================================
# MOTIVOS PRINCIPALES DE INTERNACIÓN
# ==========================================================

INTERSTICIALES = [
    ("SIN", "Sin motivo intersticial", 1),
    ("EPD_EXAC", "Exacerbación de EPD", 2),
    ("EPD_DIAG", "Diagnóstico inicial de EPD", 3),
    ("EPD_IR", "Insuficiencia respiratoria por EPD", 4),
    ("EPD_INF", "Infección sobre EPD", 5),
    ("EPD_TRAT", "Complicación del tratamiento de EPD", 6),
    ("OTRA_EPD", "Otra causa relacionada con EPD", 7),
]


def cargar(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")
    Catalogo = apps.get_model("pacientes", "Catalogo")

    def cargar_items(codigo_tipo, items):
        tipo = TipoCatalogo.objects.get(codigo=codigo_tipo)

        for codigo, descripcion, orden in items:
            Catalogo.objects.get_or_create(
                tipo=tipo,
                codigo=codigo,
                defaults={
                    "descripcion": descripcion,
                    "orden": orden,
                },
            )

    cargar_items("MOTIVO_INTERSTICIAL", INTERSTICIALES)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    codigos = [codigo for codigo, _, _ in INTERSTICIALES]

    Catalogo.objects.filter(
        tipo__codigo="MOTIVO_INTERSTICIAL",
        codigo__in=codigos,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0016_cargar_motivos_Obstructivos"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]
    
    
