---
title: "Services"
date: 2019-03-17T19:49:18-07:00
weight: 1
---

This guide will help you get any of the _AcceleratXR_ services up and running locally.

## Workstation Setup

Before any of the services will run you will need to install a few developer tools.

### Docker & Kubernetes

All services can be run locally without the use of a container system like Docker. However Docker & Kubernetes is recommended as it is how all _AcceleratXR_ services are built and deployed in a production cluster environment. All services also come with _docker-compose_ files to make it easier to run locally.

#### Windows (Chocolatey)

On Windows it is recommended that you install [Docker for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows). You can install Docker for Windows easily using Chocolatey.

```powershell
cinst docker-for-windows
```

Once installed and started make sure to enable the [Kubernetes](https://docs.docker.com/docker-for-windows/kubernetes/) engine.

#### Mac OS X (Brew)

On Mac OS X it is recommended that you install [Docker for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac). Once installed and started make sure to enable the [Kubernetes](https://docs.docker.com/docker-for-mac/kubernetes/) engine.

#### Ubuntu / Debian

For Ubuntu / Debian you will need to install Docker and Kubernetes separately. This can be easily accomplished using apt.

```bash
apt-get update && apt-get install docker docker-compose minikube
```

### NodeJS

The next thing you will need is [NodeJS](https://nodejs.org). All _AcceleratXR_ services are developed with NodeJS and written in the [TypeScript](https://www.typescriptlang.org/) language.

#### Windows (Chocolatey)

You can easily install NodeJS via Powershell using Chocolatey.

```powershell
cinst nodejs
```

#### Mac OS X (Brew)

You can easily install NodeJS via Terminal using Brew.

```bash
brew install nodejs
```

#### Ubuntu / Debian

You can easily install NodejS using Apt.

```bash
apt-get update && apt-get install nodejs
```

### Visual Studio Code

While you can use any IDE you choose, [Visual Studio Code](https://code.visualstudio.com/) is the recommended IDE of choice by the AcceleratXR team and all services already have pre-configured project workspaces ready to go out of the box.

#### Recommended Plugins

Some recommended plug-ins that you should consider installing are:

-   [Jest](https://marketplace.visualstudio.com/items?itemName=Orta.vscode-jest)
-   [Jest Test Explorer](https://marketplace.visualstudio.com/items?itemName=rtbenfield.vscode-jest-test-adapter)
-   [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
-   [TSLint](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-typescript-tslint-plugin)

## Building & Running

Once you've got all the above developer tools installed it's time to try starting your first _AcceleratXR_ service. After you've pulled down the project code from the [GitLab](https://gitlab.com/AcceleratXR/Core) repository you're ready to begin.

Open up your favorite shell or terminal and run the following commands.

```bash
docker-compose build && docker-compose up
```
