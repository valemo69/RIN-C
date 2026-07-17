from django import forms

from core.forms import BootstrapFormMixin

from .models import (
    Paciente,
    Internacion,
    InternacionCatalogo,
    Catalogo,
    RecorridoInternacion,
    InternacionSoporteRespiratorio,
    InternacionTratamientoAntimicrobiano,
    MuestraMicrobiologica,
    AislamientoMicrobiologico,
    SensibilidadMicrobiologica,
)

# ==========================================================
# BÚSQUEDA DE PACIENTES
# ==========================================================

class BusquedaPacienteForm(BootstrapFormMixin, forms.Form):

    numero_documento = forms.CharField(
        label="Documento",
        required=False,
        max_length=20,
    )

    apellido = forms.CharField(
        label="Apellido",
        required=False,
        max_length=100,
    )

    def clean(self):

        cleaned_data = super().clean()

        numero_documento = (
            cleaned_data.get("numero_documento", "")
            .strip()
        )

        apellido = (
            cleaned_data.get("apellido", "")
            .strip()
        )

        if not numero_documento and not apellido:

            raise forms.ValidationError(
                "Debe ingresar un documento, un apellido o ambos."
            )

        if numero_documento:

            if not numero_documento.isdigit():

                self.add_error(
                    "numero_documento",
                    "El documento debe contener únicamente números."
                )

            elif len(numero_documento) not in (7, 8):

                self.add_error(
                    "numero_documento",
                    "El documento debe tener 7 u 8 dígitos."
                )

        return cleaned_data
    
# ==========================================================
# PACIENTES
# ==========================================================

class PacienteForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:

        model = Paciente

        fields = (
            "tipo_documento",
            "numero_documento",
            "apellido",
            "nombre",
            "sexo",
            "fecha_nacimiento",
            "cobertura",
            "numero_afiliado",
            "estado_vital",
            "fecha_fallecimiento",
        )

        widgets = {
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date"}
            ),
            "fecha_fallecimiento": forms.DateInput(
                attrs={"type": "date"}
            ),
        }
        
    def clean(self):

        cleaned_data = super().clean()

        estado_vital = cleaned_data.get("estado_vital")
        fecha_fallecimiento = cleaned_data.get("fecha_fallecimiento")

        if estado_vital:

            if (
                estado_vital.codigo == "F"
                and not fecha_fallecimiento
            ):
                self.add_error(
                    "fecha_fallecimiento",
                    "Debe indicar la fecha de fallecimiento.",
                )

            if estado_vital.codigo == "A":
                cleaned_data["fecha_fallecimiento"] = None

        return cleaned_data
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        from .models import Catalogo

        # Tipo de documento: solo DNI y Otro
        self.fields["tipo_documento"].queryset = Catalogo.objects.filter(
            tipo__codigo="TIPO_DOCUMENTO",
            codigo__in=["DNI", "OTRO"],
        ).order_by("orden")

        # Coberturas ordenadas para el formulario
        self.fields["cobertura"].queryset = Catalogo.objects.filter(
            tipo__codigo="COBERTURA"
        ).order_by("descripcion")
# ==========================================================
# INTERNACIÓN
# ==========================================================

class InternacionForm(BootstrapFormMixin, forms.ModelForm):
    """
    Por qué "paciente" no está en fields (el mismo motivo que en
    RecorridoInternacionForm): el paciente ya se sabe por la URL
    (paciente_pk), no lo tiene que elegir el usuario desde acá. La
    vista lo asigna con form.save(commit=False) antes de guardar.
    """

    class Meta:

        model = Internacion

        fields = (
            "fecha_ingreso",
            "fecha_egreso",
            "procedencia",
            "destino_egreso",
            "insuficiencia_respiratoria",
            
        )

        widgets = {
            "fecha_ingreso": forms.DateInput(
                attrs={"type": "date"}
            ),
            "fecha_egreso": forms.DateInput(
                attrs={"type": "date"}
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
        }
    def clean(self):

        cleaned_data = super().clean()

        ingreso = cleaned_data.get("fecha_ingreso")
        egreso = cleaned_data.get("fecha_egreso")

        procedencia = cleaned_data.get("procedencia")
        destino = cleaned_data.get("destino_egreso")

        if ingreso and egreso:

            if egreso < ingreso:

                self.add_error(
                    "fecha_egreso",
                    "La fecha de egreso no puede ser anterior a la fecha de ingreso."
                )

        if not procedencia:

            self.add_error(
                "procedencia",
                "Debe indicar la procedencia."
            )

        if egreso and not destino:

            self.add_error(
                "destino_egreso",
                "Debe indicar el destino al egreso."
            )

        return cleaned_data    
    
# ==========================================================
# COMORBILIDADES E INMUNIZACIONES
# ==========================================================

class ComorbilidadesForm(BootstrapFormMixin, forms.Form):
    """
    Por qué esto es un forms.Form y no un ModelForm:
    un ModelForm sirve para crear/editar UN registro de UN modelo.
    Acá en cambio estamos decidiendo qué filas de InternacionCatalogo
    (la tabla que vincula una internación con ítems de catálogo)
    tienen que existir para esta internación: puede ser cero, una o
    varias. Eso es exactamente lo que ModelMultipleChoiceField +
    CheckboxSelectMultiple están hechos para manejar: una lista de
    casilleros, cada uno correspondiente a un Catalogo posible.

    Los querysets se filtran por tipo ("COMORBILIDAD" / "INMUNIZACION")
    para que este formulario solo pueda tildar ítems de esos dos
    tipos, y no cualquier fila de Catalogo del sistema.
    """

    comorbilidades = forms.ModelMultipleChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="COMORBILIDAD", activo=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    inmunizaciones = forms.ModelMultipleChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="INMUNIZACION", activo=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )


# ==========================================================
# ELEMENTOS DE LA INTERNACIÓN
# ==========================================================

class InternacionCatalogoForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:

        model = InternacionCatalogo

        fields = (
            "internacion",
            "catalogo",
        )
        



# ==========================================================
# RECORRIDO DE INTERNACIÓN
# ==========================================================

class RecorridoInternacionForm(BootstrapFormMixin, forms.ModelForm):
    """
    Formulario para agregar UNA fila al recorrido de una internación.

    Por qué "internacion" y "orden" no están en fields:
    - "internacion" no lo elige el usuario desde este formulario:
      ya sabemos a qué internación pertenece por la URL (viene como
      internacion_pk en pacientes:recorrido_agregar). Si lo
      dejáramos como campo del formulario, alguien podría mandar
      cualquier id de internación por POST y "colgarle" el recorrido
      a una internación de otro paciente.
    - "orden" tampoco lo completa el usuario a mano: la vista lo
      calcula sola (el siguiente número después del último
      recorrido existente), para que no dependa de que la persona
      recuerde qué número va.
    Ambos se asignan en la vista antes de guardar (form.save(commit=False)).
    """

    class Meta:

        model = RecorridoInternacion

        fields = (
            "sector",
            "fecha_desde",            
            )

        widgets = {
            "fecha_desde": forms.DateInput(
                attrs={"type": "date"}
            ),
           
        }

    def clean(self):

        cleaned_data = super().clean()

        desde = cleaned_data.get("fecha_desde")
        hasta = cleaned_data.get("fecha_hasta")

        if desde and hasta and hasta < desde:

            self.add_error(
                "fecha_hasta",
                "La fecha hasta no puede ser anterior a la fecha desde."
            )

        return cleaned_data


# ==========================================================
# SOPORTES RESPIRATORIOS
# ==========================================================

class InternacionSoporteRespiratorioForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:

        model = InternacionSoporteRespiratorio

        fields = (
            "internacion",
            "soporte",
            "fecha_desde",
            "fecha_hasta",
        )

        widgets = {
            "fecha_desde": forms.DateInput(
                attrs={"type": "date"}
            ),
            "fecha_hasta": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

# ==========================================================
# TRATAMIENTOS ANTIMICROBIANOS
# ==========================================================

class InternacionTratamientoAntimicrobianoForm(BootstrapFormMixin, forms.ModelForm):
    """
    "internacion" no está en fields: la asigna la vista (internacion_pk
    en la URL), mismo criterio que en el resto de los formularios
    "hijos" de una internación (RecorridoInternacionForm, etc).
    """

    class Meta:

        model = InternacionTratamientoAntimicrobiano

        fields = (
            "antimicrobiano",
            "indicacion",
            "via",
            "fecha_desde",
            "fecha_hasta",
            "dosis",
            "observaciones",
        )

        widgets = {
            "fecha_desde": forms.DateInput(
                attrs={"type": "date"}
            ),
            "fecha_hasta": forms.DateInput(
                attrs={"type": "date"}
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "rows": 3,
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        desde = cleaned_data.get("fecha_desde")
        hasta = cleaned_data.get("fecha_hasta")

        if desde and hasta and hasta < desde:

            self.add_error(
                "fecha_hasta",
                "La fecha hasta no puede ser anterior a la fecha desde."
            )

        return cleaned_data


# ==========================================================
# MUESTRAS MICROBIOLÓGICAS
# ==========================================================

class MuestraMicrobiologicaForm(BootstrapFormMixin, forms.ModelForm):
    """
    "internacion" no está en fields por el mismo motivo que en
    InternacionForm/RecorridoInternacionForm: ya se sabe por la URL
    (internacion_pk), la vista la asigna con commit=False.

    "mtb_detectado" y "resistencia_rifampicina" quedan opcionales
    (required=False) porque solo tienen sentido cuando tipo_muestra
    es GeneXpert MTB/RIF; para cualquier otro tipo de muestra se
    dejan vacíos.
    """

    class Meta:

        model = MuestraMicrobiologica

        fields = (
            "fecha_toma",
            "tipo_muestra",
            "resultado",
            "mtb_detectado",
            "resistencia_rifampicina",
        )

        widgets = {
            "fecha_toma": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mtb_detectado"].required = False
        self.fields["resistencia_rifampicina"].required = False


# ==========================================================
# AISLAMIENTOS
# ==========================================================

class AislamientoMicrobiologicoForm(BootstrapFormMixin, forms.ModelForm):
    """"muestra" no está en fields: la asigna la vista (muestra_pk en la URL)."""

    class Meta:

        model = AislamientoMicrobiologico

        fields = (
            "germen",
            "significativo",
        )


# ==========================================================
# SENSIBILIDAD
# ==========================================================

class SensibilidadMicrobiologicaForm(BootstrapFormMixin, forms.ModelForm):
    """"aislamiento" no está en fields: la asigna la vista (aislamiento_pk en la URL)."""

    class Meta:

        model = SensibilidadMicrobiologica

        fields = (
            "antibiotico",
            "resultado",
        )