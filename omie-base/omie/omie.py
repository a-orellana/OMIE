# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from zeep import Client, Settings
from requests import Session
from zeep.transports import Transport
import logging

import osv.osv


class CustomTransport(Transport):

    def post_xml(self, address, envelope, headers):
        # Modifica l'adreça aquí abans d'enviar la petició
        new_address = address.replace("www.mercado.omie.es", "www.pruebas.omie.es")
        return super(CustomTransport, self).post_xml(new_address, envelope, headers)

    def post(self, address, message, headers):
        # Modifica l'adreça aquí per a peticions POST si és necessari
        new_address = address.replace("www.mercado.omie.es", "www.pruebas.omie.es")
        return super(CustomTransport, self).post(new_address, message, headers)

    def get(self, address, params, headers):
        # Modifica l'adreça aquí per a peticions GET si és necessari
        new_address = address.replace("www.mercado.omie.es", "www.pruebas.omie.es")
        return super(CustomTransport, self).get(new_address, params, headers)


CustomTransport()


class Client(Client, Settings):

    servicios_consulta_mercados = [
        'ServicioConsultaMercados',
        'ServicioConsultaMensajesActivos'
    ]
    servicios_consultas = [
        'ServicioConsultaDirectorioConsultas',
        'ServicioConsultaConfiguracionConsulta',
        'ServicioEjecucionConsultaEncolumnada',
        'ServicioEjecucionConsultaAnexo',
        'ServicioEjecucionConsultaPrograma'
    ]
    servicios_consultas_auxiliares = [
        'ServicioConsultaTiposFicheros',
        'ServicioConsultaNuevosFicheros0',
        'ServicioConsultaNuevosFicherosLiq',
        'ServicioConsultaNuevosFicherosFact'
    ]
    servicios_idiomas = [
        'ServicioConsultaIdiomas',
        'ServicioSeleccionIdioma'
    ]
    servicios_consulta_documento = [
        'ServicioConsultaCertificado',
        'ServicioConsultaFactura'
    ]

    def __init__(self):
        self.settings = Settings(strict=False, xml_huge_tree=True)
        logging.basicConfig(level=logging.INFO)
        session = Session()
        session.verify = False
        session.cert = (
            '/data/omie.cert',
            '/data/omie.key'
        )
        self.pruebasTransport = CustomTransport(session=session)

    def get_cliente(self, servicio):
        """
        - Nos devuelve el cliete del fichero deseado pasándole el nombre de la llamada del servicio
        :param servicio: String con el nombre de la llamada del servicio
        :return: - Nos devuelve el cliete del fichero deseado pasándole el nombre de la llamada del servicio
                 - Si no existe el servicio, devolverá False
        """
        if servicio in self.servicios_consulta_mercados:
            url = '/services/ServicioConsultaMercados.wsdl'
        elif servicio in self.servicios_consultas:
            url = '/services/ServiciosConsultas.wsdl'
        elif servicio in self.servicios_consultas_auxiliares:
            url = '/services/ServiciosConsultasAuxiliares.wsdl'
        elif servicio in self.servicios_idiomas:
            url = '/services/ServiciosIdiomas.wsdl'
        elif servicio in self.servicios_consulta_documento:
            url = '/services/ServiciosConsultaDocumento.wsdl'
        else:
            url = '/services/{}.wsdl'.format(servicio)
        try:
            client = Client(url, settings=self.settings, transport=self.pruebasTransport)
            return client
        except Exception as e:
            print(f"Error al obtener el servicio '{servicio}': {e}")
            return False

    def __getattr__(self, servicio):
        """
        - Se obtiene el cliente para llamar al servicio, que finalmente se llama.

        :param servicio: String con el nombre del servicio que deseamos llamar.
        :return: - Nos devolverá la llamada del servicio deseado.
                 - Lanzará una excepción 'AttributeError' si el servicio no existe.
        """
        cliente = self.get_cliente(servicio)

        if cliente:
            return cliente.service.__getattr__(servicio)
        else:
            raise AttributeError(f"El siguiente servicio no existe: {servicio}")


Client()
