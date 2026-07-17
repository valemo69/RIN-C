from django.db import migrations

# ==========================================================
# MOTIVOS PRINCIPALES DE INTERNACIÓN
# ==========================================================

PLEURALES = [
    ("SIN", "Sin motivo pleural", 1),
    ("DERRAME", "Derrame pleural", 2),
    ("DERRAME_LOC", "Derrame pleural loculado", 3),
    ("NEUMOTORAX", "Neumotórax", 4),
    ("HIDRONEUMOTORAX", "Hidroneumotórax", 5),
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

    cargar_items("MOTIVO_PLEURAL", PLEURALES)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    codigos = [codigo for codigo, _, _ in PLEURALES]

    Catalogo.objects.filter(
        tipo__codigo="MOTIVO_PLEURAL",
        codigo__in=codigos,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
    ("pacientes", "0017_cargar_motivos_Intersticiales"),
        ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]
    
    
