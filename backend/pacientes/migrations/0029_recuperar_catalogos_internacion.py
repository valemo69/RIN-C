from django.db import migrations


def recuperar_catalogos_internacion(apps, schema_editor):
    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")
    Catalogo = apps.get_model("pacientes", "Catalogo")

    def crear_tipo(codigo, nombre, descripcion=""):
        tipo, _ = TipoCatalogo.objects.get_or_create(
            codigo=codigo,
            defaults={
                "nombre": nombre,
                "descripcion": descripcion,
                "protegido": True,
                "orden": 0,
                "activo": True,
            },
        )
        return tipo
    
    def crear_item(tipo, codigo, descripcion, orden):
        Catalogo.objects.get_or_create(
            tipo=tipo,
            codigo=codigo,
            defaults={
                "descripcion": descripcion,
                "grupo": "",
                "subgrupo": "",
                "orden": orden,
                "activo": True,
            },
        )
class Migration(migrations.Migration):

    dependencies = [
        (
            "pacientes",
            "0028_alter_aislamientomicrobiologico_options_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(recuperar_catalogos_internacion),
    ]