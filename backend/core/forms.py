from django import forms


class BootstrapFormMixin:
    """
    Mixin para formularios de Django que agrega automáticamente las
    clases CSS de Bootstrap a cada campo (form-control, form-select,
    form-check-input) según el tipo de widget.

    Por qué existe esto:
    El CSS del proyecto (core/static/core/css/forms.css) ya define
    estilos para esas clases, pero Django no las agrega solo: si no
    hacemos nada, cada <input> se renderiza sin ninguna clase y sale
    "feo" (blanco, sin el estilo oscuro del resto del sitio).

    En vez de escribir widgets={"campo": forms.TextInput(attrs={"class":
    "form-control"})} en cada campo de cada formulario (repetitivo y
    fácil de olvidar), este mixin recorre TODOS los campos una sola vez
    en __init__ y les asigna la clase que corresponda.

    Cómo se usa: en vez de heredar de forms.Form o forms.ModelForm,
    se hereda de (BootstrapFormMixin, forms.Form/ModelForm), por ejemplo:

        class MiForm(BootstrapFormMixin, forms.ModelForm):
            ...

    El orden importa: BootstrapFormMixin va primero para que Python
    ejecute su __init__ (que llama a super().__init__ igual) dentro
    de la cadena de herencia de forma correcta (MRO).
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            widget = field.widget

            # Checkbox y radio usan form-check-input, no form-control.
            if isinstance(widget, (forms.CheckboxInput,)):
                clase = "form-check-input"

            elif isinstance(widget, (forms.CheckboxSelectMultiple, forms.RadioSelect)):
                clase = "form-check-input"

            # Select simple o múltiple usan form-select.
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                clase = "form-select"

            # Todo lo demás (texto, número, fecha, textarea, etc.)
            # usa form-control.
            else:
                clase = "form-control"

            clases_existentes = widget.attrs.get("class", "")

            if clases_existentes:
                widget.attrs["class"] = f"{clases_existentes} {clase}".strip()
            else:
                widget.attrs["class"] = clase

            # Si el campo es un <select> que apunta al modelo Catalogo
            # (ModelChoiceField/ModelMultipleChoiceField), por defecto
            # Django arma cada opción con str(item), que para Catalogo
            # es "Tipo - Descripción" (ej: "Sexo - Femenino"). Repetir
            # el nombre del tipo en cada opción de un <select> que ya
            # está filtrado a un solo tipo es redundante ("Sexo -
            # Femenino", "Sexo - Masculino"...), así que acá lo
            # cambiamos para que solo muestre la descripción.
            queryset = getattr(field, "queryset", None)

            if queryset is not None and hasattr(queryset.model, "descripcion"):
                field.label_from_instance = lambda obj: obj.descripcion
