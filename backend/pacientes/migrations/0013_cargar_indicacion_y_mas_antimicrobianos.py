from django.db import migrations

# ==========================================================
# POR QUÉ ESTA MIGRACIÓN
# ==========================================================
#
# INDICACION_ATB no tenía ningún ítem cargado (necesario para el
# formulario de Tratamiento). Además, el mockup de tratamiento.html
# separaba visualmente "Antibióticos" / "Antituberculosos" /
# "Antifúngicos" / "Antivirales" en 4 bloques, pero los 4 son
# exactamente el mismo concepto en el modelo (un
# InternacionTratamientoAntimicrobiano: un antimicrobiano + vía +
# dosis + fechas). En vez de crear 3 modelos nuevos para lo mismo,
# ampliamos el catálogo ANTIMICROBIANO para que también incluya
# antituberculosos y antivirales, y en la pantalla va a quedar como
# una sola lista de tratamientos (más flexible: permite dosis y
# fechas por droga, que un simple checkbox no tenía).


INDICACIONES = [
    ("EMPIRICO", "Empírico", 1),
    ("DIRIGIDO", "Dirigido", 2),
    ("PROFILAXIS", "Profilaxis", 3),
]

ANTITUBERCULOSOS = [
    ("ISONIACIDA", "Isoniacida", 60),
    ("PIRAZINAMIDA", "Pirazinamida", 61),
    ("ETAMBUTOL", "Etambutol", 62),
    # Rifampicina ya existe en el catálogo desde la migración 0007.
]

ANTIVIRALES = [
    ("OSELTAMIVIR", "Oseltamivir", 70),
    ("ACICLOVIR", "Aciclovir", 71),
    ("GANCICLOVIR", "Ganciclovir", 72),
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
                defaults={"descripcion": descripcion, "orden": orden},
            )

    cargar_items("INDICACION_ATB", INDICACIONES)
    cargar_items("ANTIMICROBIANO", ANTITUBERCULOSOS)
    cargar_items("ANTIMICROBIANO", ANTIVIRALES)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    codigos_indicacion = [codigo for codigo, _, _ in INDICACIONES]
    codigos_atb = [codigo for codigo, _, _ in ANTITUBERCULOSOS + ANTIVIRALES]

    Catalogo.objects.filter(
        tipo__codigo="INDICACION_ATB", codigo__in=codigos_indicacion
    ).delete()

    Catalogo.objects.filter(
        tipo__codigo="ANTIMICROBIANO", codigo__in=codigos_atb
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0012_cargar_germenes_y_atb_completos"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]
