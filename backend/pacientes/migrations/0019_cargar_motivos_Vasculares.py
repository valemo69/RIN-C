from django.db import migrations

# ==========================================================
# MOTIVOS PRINCIPALES DE INTERNACIÓN
# ==========================================================

VASCULARES = [
    ("SIN", "Sin motivo vascular", 1),
    ("TEP", "Tromboembolismo pulmonar", 2),
    ("HTP", "Hipertensión pulmonar", 3),
    ("HEMOPTISIS", "Hemoptisis", 4),
    ("OTRO", "Otra patología vascular pulmonar", 5),
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

    cargar_items("MOTIVO_VASCULAR", VASCULARES)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    codigos = [codigo for codigo, _, _ in VASCULARES]

    Catalogo.objects.filter(
        tipo__codigo="MOTIVO_VASCULAR",
        codigo__in=codigos,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
    ("pacientes", "0018_cargar_motivos_pleurales"),
        ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]
    
    
