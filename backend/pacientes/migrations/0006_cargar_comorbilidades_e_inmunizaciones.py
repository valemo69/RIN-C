from django.db import migrations

# ==========================================================
# POR QUÉ ESTA MIGRACIÓN
# ==========================================================
#
# "COMORBILIDAD" ya existía como TipoCatalogo desde la migración
# 0003, pero nunca se cargó ningún ítem adentro (estaba vacío).
# "INMUNIZACION" ni siquiera existía como tipo: en el mockup de
# comorbilidades.html las vacunas (Antigripal, COVID-19, etc)
# están mezcladas visualmente con las comorbilidades, pero
# conceptualmente son otra cosa (una vacuna no es una enfermedad),
# así que les damos su propio TipoCatalogo.
#
# Los ítems de acá abajo son una transcripción directa de los
# checkboxes que ya estaban en pacientes/templates/pacientes/
# comorbilidades.html, agrupados con el mismo campo "grupo" que
# usa esa pantalla para armar las tarjetas (Cardiovasculares,
# Endócrino - Metabólicas, etc).


COMORBILIDADES = [
    # (grupo,                        codigo,             descripcion,                              orden)
    ("Cardiovasculares", "HTA", "HTA", 1),
    ("Cardiovasculares", "INSUF_CARDIACA", "Insuficiencia cardíaca", 2),
    ("Cardiovasculares", "CARDIOPATIA_ISQ", "Cardiopatía isquémica", 3),
    ("Cardiovasculares", "ARRITMIAS", "Arritmias", 4),
    ("Cardiovasculares", "VALVULOPATIAS", "Valvulopatías", 5),
    ("Cardiovasculares", "CARDIO_OTRAS", "Otras", 6),
    ("Endócrino - Metabólicas", "DIABETES", "Diabetes", 1),
    ("Endócrino - Metabólicas", "OBESIDAD", "Obesidad", 2),
    ("Endócrino - Metabólicas", "HIPOTIROIDISMO", "Hipotiroidismo", 3),
    ("Endócrino - Metabólicas", "HIPERTIROIDISMO", "Hipertiroidismo", 4),
    ("Endócrino - Metabólicas", "DISLIPIDEMIA", "Dislipidemia", 5),
    ("Reumatológicas", "ARTRITIS_REUMATOIDEA", "Artritis reumatoidea", 1),
    ("Reumatológicas", "ESCLEROSIS_SISTEMICA", "Esclerosis sistémica", 2),
    ("Reumatológicas", "LES", "Lupus eritematoso sistémico", 3),
    ("Reumatológicas", "DERMATOMIOSITIS", "Dermatomiositis", 4),
    ("Reumatológicas", "POLIMIOSITIS", "Polimiositis", 5),
    ("Reumatológicas", "SME_ANTISINTETASA", "Síndrome antisintetasa", 6),
    ("Reumatológicas", "EMTC", "Enfermedad mixta del tejido conectivo", 7),
    ("Reumatológicas", "SJOGREN", "Síndrome de Sjögren", 8),
    # Vasculitis
    ("Reumatológicas", "GPA", "Granulomatosis con poliangeítis (GPA)", 9),
    ("Reumatológicas", "MPA", "Poliangeítis microscópica (MPA)", 10),
    (
        "Reumatológicas",
        "EGPA",
        "Granulomatosis eosinofílica con poliangeítis (EGPA)",
        11,
    ),
    ("Reumatológicas", "PAN", "Poliarteritis nudosa", 12),
    (
        "Reumatológicas",
        "GOODPASTURE",
        "Enfermedad por anticuerpos anti-MBG (Goodpasture)",
        13,
    ),
    ("Reumatológicas", "BEHCET", "Enfermedad de Behçet", 14),
    ("Reumatológicas", "CRIOGLOBULINEMIA", "Vasculitis crioglobulinémica", 15),
    ("Reumatológicas", "IGA", "Vasculitis por IgA", 16),
    ("Reumatológicas", "ANCA_OTRA", "Otra vasculitis ANCA", 17),
    ("Reumatológicas", "NO_ANCA_OTRA", "Otra vasculitis no ANCA", 18),
    ("Reumatológicas", "REUMA_OTRAS", "Otras", 19),
    ("Neurológicas", "ACV", "ACV", 1),
    ("Neurológicas", "TRASTORNO_COGNITIVO", "Trastorno cognitivo", 2),
    ("Neurológicas", "COMPROMISO_MUSCULAR", "Compromiso muscular", 3),
    ("Neurológicas", "SARCOPENIA_GRAVE", "Sarcopenia grave", 4),
    ("Inmunológicas", "HIV", "HIV", 1),
    ("Inmunológicas", "TRASPLANTE", "Trasplante", 2),
    ("Inmunológicas", "TTO_INMUNOSUPRESOR", "Tratamiento inmunosupresor", 3),
    ("Oncológicas", "TUMOR_SOLIDO_EXTRAPULMONAR", "Tumor sólido extrapulmonar", 1),
    ("Oncológicas", "ENF_ONCOHEMATOLOGICA", "Enfermedad oncohematológica", 2),
    ("Otras comorbilidades", "HEPATOPATIA_CRONICA", "Hepatopatía crónica", 1),
    ("Otras comorbilidades", "IRC", "Insuficiencia renal crónica", 2),
]

INMUNIZACIONES = [
    ("Inmunizaciones", "ANTIGRIPAL", "Antigripal", 1),
    ("Inmunizaciones", "COVID19", "COVID-19", 2),
    ("Inmunizaciones", "NEUMOCOCO", "Neumococo", 3),
    ("Inmunizaciones", "VSR", "VSR", 4),
]


def cargar(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")
    Catalogo = apps.get_model("pacientes", "Catalogo")

    tipo_inmunizacion, _ = TipoCatalogo.objects.get_or_create(
        codigo="INMUNIZACION",
        defaults={
            "nombre": "Inmunización",
            "descripcion": "",
            "orden": 50,
            "protegido": True,
            "activo": True,
        },
    )

    tipo_comorbilidad = TipoCatalogo.objects.get(codigo="COMORBILIDAD")

    for grupo, codigo, descripcion, orden in COMORBILIDADES:
        Catalogo.objects.get_or_create(
            tipo=tipo_comorbilidad,
            codigo=codigo,
            defaults={
                "descripcion": descripcion,
                "grupo": grupo,
                "orden": orden,
            },
        )

    for grupo, codigo, descripcion, orden in INMUNIZACIONES:
        Catalogo.objects.get_or_create(
            tipo=tipo_inmunizacion,
            codigo=codigo,
            defaults={
                "descripcion": descripcion,
                "grupo": grupo,
                "orden": orden,
            },
        )


def deshacer(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")
    Catalogo = apps.get_model("pacientes", "Catalogo")

    Catalogo.objects.filter(tipo__codigo__in=["COMORBILIDAD", "INMUNIZACION"]).delete()

    TipoCatalogo.objects.filter(codigo="INMUNIZACION").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0005_alter_paciente_estado_vital_alter_paciente_sexo"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]
