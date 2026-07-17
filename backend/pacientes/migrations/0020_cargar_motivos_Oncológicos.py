from django.db import migrations

# ==========================================================
# MOTIVOS PRINCIPALES DE INTERNACIÓN
# ==========================================================

ONCOLOGICAS = [
    ("SIN", "Sin motivo oncológico", 1),
    ("CA_PULMON", "Cáncer de pulmón", 2),
    ("NODULO", "Nódulo pulmonar en estudio", 3),
    ("MASA", "Masa pulmonar en estudio", 4),
    ("MASA_MEDIASTINAL", "Masa mediastinal", 5),
    ("MESOTELIOMA", "Mesotelioma pleural", 6),
    ("METASTASIS", "Metástasis pulmonares", 7),
    ("OTRO", "Otra patología oncológica torácica", 8),
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

    cargar_items("MOTIVO_ONCOLOGICO", ONCOLOGICAS)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    codigos = [codigo for codigo, _, _ in ONCOLOGICAS]

    Catalogo.objects.filter(
        tipo__codigo="MOTIVO_ONCOLOGICO",
        codigo__in=codigos,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
    ("pacientes", "0019_cargar_motivos_Vasculares"),
        ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]
    
    
