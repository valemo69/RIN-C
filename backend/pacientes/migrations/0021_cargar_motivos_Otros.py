from django.db import migrations

# ==========================================================
# MOTIVOS PRINCIPALES DE INTERNACIÓN
# ==========================================================

OTRAS = [
    ("SIN", "Sin otro motivo", 1),
    ("ESTUDIO", "Estudio de patología pulmonar", 2),
    ("PROC_DIAG", "Procedimiento diagnóstico", 3),
    ("PROC_TER", "Procedimiento terapéutico", 4),
    ("DOLOR", "Manejo del dolor", 5),
    ("ICC", "Insuficiencia cardíaca", 6),
    ("ARRITMIA", "Arritmia", 7),
    ("PREOP", "Evaluación preoperatoria", 8),
    ("OTRO", "Otro", 9),
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

    cargar_items("MOTIVO_OTROS", OTRAS)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    codigos = [codigo for codigo, _, _ in OTRAS]

    Catalogo.objects.filter(
        tipo__codigo="MOTIVO_OTROS",
        codigo__in=codigos,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
    ("pacientes", "0020_cargar_motivos_Oncológicos"),
        ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]
    
    
