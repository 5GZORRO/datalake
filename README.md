# 5GZORRO Datalake 

## Overview
This repository contains code and other files to implement the 5GZORRO datalake.

The main datalake API functionality is provided in the directory python-flask-server, much of which was generated by swagger.codegen.

The API itself is specified in datalake_swagger.yaml and datalake_api.html.

This code is work-in-progess.

## Requirements
The datalake server requires that there first be running: kubernetes, kafka, argo.
Kubernetes should use Docker container management for argo to work properly.

For kubernetes, it is possible to run a simulated minikube cluster.

## Usage
In the python-flask-server directory, fill in the proper values in conf.yaml and follow the instructions in the README file.
