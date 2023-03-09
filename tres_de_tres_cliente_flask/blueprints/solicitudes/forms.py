"""
Solicitudes, formularios
"""
from flask import abort
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import BooleanField, EmailField, SelectField, StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Length
import requests

from config.settings import API_BASE_URL, API_TIMEOUT


def partidos_politicos():
    """Consultar los partidos políticos"""
    try:
        respuesta = requests.get(
            f"{API_BASE_URL}/tdt_partidos",
            timeout=API_TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        abort(500, "No se pudo conectar con la API 3de3. " + str(error))
    except requests.exceptions.Timeout as error:
        abort(500, "Tiempo de espera agotado al conectar con la API 3de3. " + str(error))
    except requests.exceptions.HTTPError as error:
        abort(500, "Error HTTP porque la API 3de3 arrojó un problema: " + str(error))
    except requests.exceptions.RequestException as error:
        abort(500, "Error desconocido con la API 3de3. " + str(error))
    datos = respuesta.json()
    items = datos["result"]["items"]
    return [("", "Selecciona un partido")] + [(key["siglas"], key["nombre"]) for key in items]


def municipios():
    """Consultar los municipios"""
    try:
        respuesta = requests.get(
            f"{API_BASE_URL}/municipios",
            timeout=API_TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        abort(500, "No se pudo conectar con la API Municipios. " + str(error))
    except requests.exceptions.Timeout as error:
        abort(500, "Tiempo de espera agotado al conectar con la API Municipios. " + str(error))
    except requests.exceptions.HTTPError as error:
        abort(500, "Error HTTP porque la API Municipios arrojó un problema: " + str(error))
    except requests.exceptions.RequestException as error:
        abort(500, "Error desconocido con la API Municipios. " + str(error))
    datos = respuesta.json()
    items = datos["result"]["items"]
    return [("", "Selecciona un municipio")] + [(key["id_hasheado"], key["nombre"]) for key in items]


class IngresarForm(FlaskForm):
    """Formulario para ingresar datos personales"""

    nombres = StringField(
        "Nombres",
        default="Carlos Gabriel",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    apellido_primero = StringField(
        "Primer apellido",
        default="Hernandez",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    apellido_segundo = StringField(
        "Segundo apellido",
        default="Salas",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    curp = StringField(
        "CURP",
        default="HESC741104HCLRLR09",
        validators=[DataRequired(), Length(min=18, max=18)],
        render_kw={"placeholder": "18 caracteres"},
    )
    email = EmailField(
        "Email",
        default="carlos.hernandez@coahuila.gob.mx",
        validators=[DataRequired(), Length(min=3, max=128)],
    )
    telefono = StringField(
        "Telefono celular",
        default="8442180123",
        validators=[DataRequired(), Length(min=10, max=10)],
        render_kw={"placeholder": "10 dígitos sin espacios ni guiones"},
    )
    colonia = StringField(
        "Colonia",
        default="Lomas de Lourdes",
        validators=[DataRequired(), Length(min=10, max=50)],
    )
    calle = StringField(
        "Calle",
        default="Correcaminos",
        validators=[DataRequired(), Length(min=10, max=50)],
    )
    numero = StringField(
        "Numero",
        default="1290",
        validators=[DataRequired(), Length(min=2, max=15)],
    )
    codigoPostal = StringField(
        "Codigo Postal",
        default="25090",
        validators=[DataRequired(), Length(min=5, max=5)],
    )
    municipio = SelectField(
        "Municipio",
        validators=[DataRequired()],
        choices=municipios(),
    )
    partido = SelectField(
        "Partido Político",
        validators=[DataRequired()],
        choices=partidos_politicos(),
        default="MORENA",
    )
    cargo = SelectField(
        "Cargo",
        validators=[DataRequired()],
        choices=[("", "Selecciona un cargo"), ("GOBERNATURA", "Gobernatura"), ("PRESIDENCIA MUNICIPAL", "Presidencia Municipal"), ("REGIDURIA", "Regiduría"), ("SINDICATURA", "Sindicatura")],
        default="SINDICATURA",
    )
    principio = SelectField(
        "Principio",
        validators=[DataRequired()],
        choices=[("", "Selecciona un principio"), ("MAYORIA RELATIVA", "Mayoría relativa"), ("REPRESENTACION PROPORCIONAL", "Representación proporcional")],
        default="MAYORIA RELATIVA",
    )
    ine = FileField(
        "Credencial de elector",
        validators=[DataRequired()],
        render_kw={"placeholder": "Seleccione un archivo PDF con la INE por ambos lados", "accept": "application/pdf"},
    )
    comprobante = FileField(
        "Comprobante de domicilio",
        validators=[DataRequired()],
        render_kw={"placeholder": "Seleccione un archivo PDF del comprobante de domicilio", "accept": "application/pdf"},
    )
    autorizacion = FileField(
        "Autorización firmada",
        validators=[DataRequired()],
        render_kw={"placeholder": "Autorización firmada en archivo PDF", "accept": "application/pdf"},
    )
    recaptcha = RecaptchaField()
    aceptar = BooleanField(
        "He leído y acepto el <a href='/aviso' class='nav-link link-aviso'>Aviso de Privacidad</a>",
        validators=[DataRequired()],
        default="checked",
    )
    registrar = SubmitField("Registrar")
