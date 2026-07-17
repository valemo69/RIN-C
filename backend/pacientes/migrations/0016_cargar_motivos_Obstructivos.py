from django.db import migrations

# ==========================================================
# MOTIVOS PRINCIPALES DE INTERNACIÓN
# ==========================================================

OBSTRUCTIVAS = [
    ("SIN", "Sin motivo obstructivo", 1),
    ("EPOC_AE", "Exacerbación de EPOC", 2),
    ("ASMA_AE", "Exacerbación de asma", 3),
    ("BRONQUIECTASIAS", "Exacerbación de bronquiectasias", 4),
    ("FQ", "Exacerbación de fibrosis quística", 5),
    ("POVA", "Patología obstructiva de la vía aérea", 6),
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

    cargar_items("MOTIVO_OBSTRUCTIVO", OBSTRUCTIVAS)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    codigos = [codigo for codigo, _, _ in OBSTRUCTIVAS]

    Catalogo.objects.filter(
        tipo__codigo="MOTIVO_OBSTRUCTIVO",
        codigo__in=codigos,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0015_cargar_motivos_infecciosos"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]
    
    
