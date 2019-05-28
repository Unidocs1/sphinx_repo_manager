---
title: "Services Deployment"
date: 2019-05-28T17:50:05-07:00
---

Every AcceleratXR service produces a [Docker](https://www.docker.com/) container image that can be deployed into a supporting container service. AcceleratXR recommends [Kubernetes](https://kubernetes.io/) and provides some useful resources to help deploy and manage individual services in a Kubernetes cluster environment which can be found [here](https://gitlab.com/AcceleratXR/Core/tools/k8s_deploy).

## Deploy Resource

Every service starts with a Deployment resource. The Deployment resource tells Kubernetes where to find the Docker container image to deploy within the cluster. Each service has an available image published on GitLab.

### Example: Account Services

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
    name: account-services
    namespace: axr-v1
    labels:
        app: account-services
spec:
    selector:
        matchLabels:
            app: account-services
    template:
        metadata:
            labels:
                app: account-services
        spec:
            imagePullSecrets:
                - name: gitlab-creds-account-services
            containers:
                - name: account-services
                  image: registry.gitlab.com/acceleratxr/core/account_services:latest
                  imagePullPolicy: Always
                  envFrom:
                      - configMapRef:
                            name: all-env-config
                      - configMapRef:
                            name: services-env-config
                      - configMapRef:
                            name: account-services-env-config
                  ports:
                      - containerPort: 3000
```

## Service Resource

The Server resource describes what services the deployed pod will provide. In the case of AcceleratXR services this will almost always be an NodePort service using the TCP protocol mapping the internal port `3000` to `80`.

### Example: Account Services

```yaml
---
apiVersion: v1
kind: Service
metadata:
    name: account-services
    namespace: axr-v1
    labels:
        run: account-services
spec:
    type: NodePort
    ports:
        - port: 80
          targetPort: 3000
          protocol: TCP
    selector:
        app: account-services
```

## Ingress Resource

The ingress resource is how multiple services can be combined into a singular public API endpoint for clients to access. As each service responds to its own set of endpoints it is often useful to map these endpoints to a single base path. However, it is not always necessary to do so and instead each of the service's supporting endpoints can be mapped individually.

## Example: API Ingress

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
    name: api-ingress
    namespace: axr-v1
    annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /$1
spec:
    tls:
        - hosts:
              - api.example.com
          secretName: tls-cert
    rules:
        - host: api.example.com
          http:
              paths:
                  - path: /v1/(assets.*)
                    backend:
                        serviceName: asset-services
                        servicePort: 80
                  - path: /v1/(auth.*)
                    backend:
                        serviceName: account-services
                        servicePort: 80
                    backend:
                        serviceName: asset-services
                        servicePort: 80
                  - path: /v1/(roles.*)
                    backend:
                        serviceName: account-services
                        servicePort: 80
                  - path: /v1/matchmaking/?(.*)
                    backend:
                        serviceName: matchmaking-services
                        servicePort: 80
                  - path: /v1/(servermanagers.*)
                    backend:
                        serviceName: server-manager-services
                        servicePort: 80
                  - path: /v1/(serverdownload.*)
                    backend:
                        serviceName: server-manager-services
                        servicePort: 80
                  - path: /v1/(sessions.*)
                    backend:
                        serviceName: session-services
                        servicePort: 80
                  - path: /v1/(snapshot.*)
                    backend:
                        serviceName: asset-services
                        servicePort: 80
                  - path: /v1/(upload.*)
                    backend:
                        serviceName: asset-services
                        servicePort: 80
                  - path: /v1/(users.*)
                    backend:
                        serviceName: account-services
                        servicePort: 80
```
