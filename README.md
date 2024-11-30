# weaviate-k8s-local

## Introduction

This is my guide on deploying Weaviate on a local Kubernetes cluster using Helm.

## Prerequisites

- Install Python
- Install Helm
- Install kubectl
- Install Docker Desktop or Minikube for local Kubernetes cluster

NOTE: I used Docker Desktop for this guide.

## Setup Weaviate

1. Create a namespace for Weaviate
    - Run `kubectl create namespace weaviate`
2. Add the Weaviate Helm repository
    - Run `helm repo add weaviate https://weaviate.github.io/weaviate-helm`
3. Update the Helm repository
    - Run `helm repo update`
4. Configure the Weaviate Helm chart
    - Run `helm show values weaviate/weaviate > values.yaml`
4. Description of values.yaml
    - `values.yaml` is a file that contains the values for the Weaviate Helm chart.
    - It is used to customize the deployment of Weaviate.
    - Enabled the selected modules and associated models for vectorization and generation
5. Install Weaviate using Helm
    - Run `helm upgrade --install "weaviate" weaviate/weaviate --namespace "weaviate" --values ./values.yaml`
6. Set API keys in the .env file or using Kubernetes secrets

## Test Weaviate using Python

1. Clone the repository
2. Run `python rag.py`

## Clean up

- Run `helm uninstall weaviate -n weaviate`
- Delete the namespace
    - Run `kubectl delete namespace weaviate`
- Delete the Python virtual environment
    - Run `deactivate`
    - Run `rm -rf .venv`