#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from swagger_server.controllers import resource_controller


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Data Lake Catalog Service API'})
    resource_controller.init_catalog_access()
    app.run(port=8086)


if __name__ == '__main__':
    main()
