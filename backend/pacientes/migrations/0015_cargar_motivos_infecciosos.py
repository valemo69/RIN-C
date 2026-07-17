from django.db import migrations

# ==========================================================
# MOTIVOS PRINCIPALES DE INTERNACIÓN
# ==========================================================

INFECCIOSOS = [
    ("SIN", "Sin motivo infeccioso", 1),
    ("NAC", "Neumonía adquirida en la comunidad (NAC)", 2),
    ("NIH", "Neumonía intrahospitalaria (NIH)", 3),
    ("NEUMONIA_VIRAL", "Neumonía viral", 4),
    ("TBC", "Tuberculosis", 5),
    ("MNT", "Infección por micobacterias no tuberculosas", 6),
    ("MICOSIS", "Micosis pulmonares", 7),
    ("ABSCESO", "Absceso pulmonar", 8),
    ("Pulmón secuelar sobreinfectado", "Pulmón secuelar sobreinfectado", 9),
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

    cargar_items("MOTIVO_INFECCIOSO", INFECCIOSOS)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    codigos = [codigo for codigo, _, _ in INFECCIOSOS]

    Catalogo.objects.filter(
        tipo__codigo="MOTIVO_INFECCIOSO",
        codigo__in=codigos,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0014_cargar_coberturas"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]
    
    
