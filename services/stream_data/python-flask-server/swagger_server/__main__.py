#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from swagger_server.controllers import transaction_controller


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Data Lake Stream Data Service API'})
    transaction_controller.init_stream_data()
    app.run(port=8087)


if __name__ == '__main__':
    main()
