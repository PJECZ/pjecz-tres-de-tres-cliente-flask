"""
Solicitudes, vistas
"""
from flask import abort, Blueprint, render_template, redirect, request, url_for
import requests

from config.settings import API_BASE_URL, API_TIMEOUT
from lib.safe_string import safe_email, safe_string
from lib.hashids import descifrar_id

from tres_de_tres_cliente_flask.blueprints.solicitudes.forms import IngresarForm

solicitudes = Blueprint("solicitudes", __name__, template_folder="templates")


@solicitudes.route("/solicitud", methods=["GET", "POST"])
def ingresar():
    """Ingresar datos personales"""
    form = IngresarForm()

    # Si viene el formulario
    if form.validate_on_submit():
        # Solicitar a la API un nuevo registro
        request_body = {
            "cit_cliente_nombres": safe_string(form.nombres.data, save_enie=True),
            "cit_cliente_apellido_primero": safe_string(form.apellido_primero.data, save_enie=True),
            "cit_cliente_apellido_segundo": safe_string(form.apellido_segundo.data, save_enie=True),
            "cit_cliente_curp": safe_string(form.curp.data),
            "cit_cliente_email": safe_email(form.email.data),
            "cit_cliente_telefono": safe_string(form.telefono.data),
            "tdt_partido_siglas": safe_string(form.partido.data),
            "municipio_id_hasheado": safe_string(form.municipio.data),
            "cargo": safe_string(form.cargo.data),
            "principio": safe_string(form.principio.data),
            "domicilio_calle": safe_string(form.calle.data),
            "domicilio_numero": safe_string(form.numero.data),
            "domicilio_colonia": safe_string(form.colonia.data),
            "domicilio_cp": safe_string(form.codigo.data),
            "identificacion_oficial_url": "",
            "comprobante_domicilio_url": "",
            "autorizacion_url": "",
        }
        try:
            respuesta = requests.post(
                f"{API_BASE_URL}/tdt_solicitudes/solicitar",
                json=request_body,
                timeout=API_TIMEOUT,
            )
            respuesta.raise_for_status()
        except requests.exceptions.ConnectionError as error:
            abort(500, "No se pudo conectar con la API 3de3. " + str(error))
        except requests.exceptions.Timeout as error:
            abort(500, "Tiempo de espera agotado al conectar con la API 3de3. " + str(error))
        except requests.exceptions.HTTPError as error:
            abort(500, "Error HTTP porque la API de 3de3 arrojó un problema: " + str(error))
        except requests.exceptions.RequestException as error:
            abort(500, "Error desconocido con la API 3de3. " + str(error))
        datos = respuesta.json()

        # Verificar que haya tenido exito
        if not "success" in datos:
            abort(400, "No se logro la comunicacion con la API.")
        if datos["success"] is False:
            return redirect(url_for("resultados.fallido", message=datos["message"]))

        # Enviar a la API el documento INE
        archivo_ine = request.files["ine"]
        try:
            respuesta = requests.post(
                f"{API_BASE_URL}/tdt_solicitudes/subir/identificacion_oficial?id_hasheado={datos['id_hasheado']}",
                files={"archivo": archivo_ine.stream.read()},
                timeout=API_TIMEOUT,
            )
            respuesta.raise_for_status()
        except requests.exceptions.ConnectionError as error:
            abort(500, "No se pudo conectar con la API 3de3. " + str(error))
        except requests.exceptions.Timeout as error:
            abort(500, "Tiempo de espera agotado al conectar con la API 3de3. " + str(error))
        except requests.exceptions.HTTPError as error:
            abort(500, "Error HTTP porque la API de 3de3 arrojó un problema: " + str(error))
        except requests.exceptions.RequestException as error:
            abort(500, "Error desconocido con la API 3de3. " + str(error))
        datos_ine = respuesta.json()

        # Verificar que haya tenido exito
        if not "success" in datos_ine:
            abort(400, "No se logro la comunicacion con la API.")
        if datos["success"] is False:
            return redirect(url_for("resultados.fallido", message=datos_ine["message"]))

        # Enviar a la API el comprobante de domicilio
        archivo_comprobante = request.files["comprobante"]
        try:
            respuesta = requests.post(
                f"{API_BASE_URL}/tdt_solicitudes/subir/comprobante_domicilio?id_hasheado={datos['id_hasheado']}",
                files={"archivo": archivo_comprobante.stream.read()},
                timeout=API_TIMEOUT,
            )
            respuesta.raise_for_status()
        except requests.exceptions.ConnectionError as error:
            abort(500, "No se pudo conectar con la API 3de3. " + str(error))
        except requests.exceptions.Timeout as error:
            abort(500, "Tiempo de espera agotado al conectar con la API 3de3. " + str(error))
        except requests.exceptions.HTTPError as error:
            abort(500, "Error HTTP porque la API de 3de3 arrojó un problema: " + str(error))
        except requests.exceptions.RequestException as error:
            abort(500, "Error desconocido con la API 3de3. " + str(error))
        datos_comprobante = respuesta.json()

        # Verificar que haya tenido exito
        if not "success" in datos_comprobante:
            abort(400, "No se logro la comunicacion con la API.")
        if datos["success"] is False:
            return redirect(url_for("resultados.fallido", message=datos_comprobante["message"]))

        # Enviar a la API el documento de autorizacion
        archivo_autorizacion = request.files["autorizacion"]
        try:
            respuesta = requests.post(
                f"{API_BASE_URL}/tdt_solicitudes/subir/autorizacion?id_hasheado={datos['id_hasheado']}",
                files={"archivo": archivo_autorizacion.stream.read()},
                timeout=API_TIMEOUT,
            )
            respuesta.raise_for_status()
        except requests.exceptions.ConnectionError as error:
            abort(500, "No se pudo conectar con la API 3de3. " + str(error))
        except requests.exceptions.Timeout as error:
            abort(500, "Tiempo de espera agotado al conectar con la API 3de3. " + str(error))
        except requests.exceptions.HTTPError as error:
            abort(500, "Error HTTP porque la API de 3de3 arrojó un problema: " + str(error))
        except requests.exceptions.RequestException as error:
            abort(500, "Error desconocido con la API 3de3. " + str(error))
        datos_autorizacion = respuesta.json()

        # Verificar que haya tenido exito
        if not "success" in datos_autorizacion:
            abort(400, "No se logro la comunicacion con la API.")
        if datos["success"] is False:
            return redirect(url_for("resultados.fallido", message=datos_autorizacion["message"]))

        # Redireccionar a la página de resultados
        return redirect(url_for("resultados.registrado", folio="F-" + str(descifrar_id(datos["id_hasheado"])).zfill(5)))

    # Mostrar el formulario
    return render_template(
        "solicitudes/solicitud.jinja2",
        form=form,
    )
