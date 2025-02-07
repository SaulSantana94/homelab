# MetalLB Configuration Guide

MetalLB is a load-balancer implementation for Kubernetes clusters, enabling the use of Kubernetes services of type LoadBalancer in environments lacking a native load balancer. MetalLB supports two modes: Layer 2 (ARP) and BGP. This guide details the configuration steps for MetalLB in Layer 2 mode (ARP) as BGP mode is not supported by my router.

## Prerequisites

Before configuring MetalLB, ensure that ArgoCD is configured.

## Configuration

In this implementation, MetalLB is utilized to manage load balancers within the Kubernetes cluster. The configurations for MetalLB are stored in the `metallb-system` namespace, with specific details outlined in three key files:

### `metallb-system/values.yaml`:

This file contains configuration values for MetalLB. Here's a detailed breakdown of the configurations:

- `metallb.existingConfigMap`: Specifies the name of an existing ConfigMap for MetalLB configuration. This ConfigMap allows you to customize MetalLB behavior by providing additional configuration options.
- `metallb.controller.enabled`: Specifies whether the MetalLB controller component is enabled or not.
- `metallb.controller.resources.requests.cpu / memory`: Defines the CPU and memory resource requests for the MetalLB controller pod.
- `metallb.controller.resources.limits.memory`: Sets the memory limit for the MetalLB controller pod.
- `metallb.controller.livenessProbe.enabled`: Specifies whether the liveness probe for the MetalLB controller pod is enabled.
- `metallb.controller.livenessProbe.periodSeconds`: Specifies the period (in seconds) at which the liveness probe will be performed.
- `metallb.controller.livenessProbe.timeoutSeconds`: Sets the timeout (in seconds) for the liveness probe.
- `metallb.speaker.resources.requests.cpu / memory`: Defines the CPU and memory resource requests for the MetalLB speaker pod.
- `metallb.speaker.resources.limits.memory`: Sets the memory limit for the MetalLB speaker pod.
- `metallb.speaker.livenessProbe.enabled`: Specifies whether the liveness probe for the MetalLB speaker pod is enabled.
- `metallb.speaker.livenessProbe.periodSeconds`: Specifies the period (in seconds) at which the liveness probe will be performed.
- `metallb.speaker.livenessProbe.timeoutSeconds`: Sets the timeout (in seconds) for the liveness probe.
- `metallb.protocol`: Specifies the protocol used by MetalLB. In this case, it's set to "layer2" for ARP mode.

Liveness Probe

A liveness probe is a mechanism used to determine if a container in a Kubernetes pod is alive and healthy. MetalLB's controller and speaker components have liveness probes configured to ensure their health and availability.

The liveness probe periodically checks the health of the container by sending requests to a specified endpoint or by executing a command inside the container. If the probe fails to receive a successful response within the specified timeout period, the container is considered unhealthy, and Kubernetes may restart it.

Consequences:

- Liveness probes help ensure the reliability and availability of MetalLB components by automatically restarting them if they become unresponsive.
- This helps maintain the desired state of the MetalLB deployment and ensures that load balancing functionality is consistently available.

MetalLB Controller Pod

The MetalLB controller is responsible for managing the configuration and state of MetalLB within the Kubernetes cluster. It monitors changes to MetalLB configurations, such as IP address pools and speaker configurations, and ensures that the cluster's state matches the desired state.

Consequences:

- The controller pod handles the dynamic allocation and release of IP addresses from the configured address pools.
- It monitors the health of MetalLB components and ensures they are functioning correctly.

MetalLB Speaker

The MetalLB speaker is responsible for advertising and managing the allocated IP addresses to the external network. It communicates with the network infrastructure to ensure that traffic destined for the allocated IP addresses is correctly routed to the Kubernetes cluster.

Consequences:

- The speaker pod acts as the interface between MetalLB and the network infrastructure, ensuring that external traffic is correctly load balanced to the appropriate services within the cluster.
- It handles the ARP announcements necessary to make the allocated IP addresses reachable from outside the cluster.


### `metallb-system/templates/ipaddresspool.yaml`:

This file defines the IP address pool that MetalLB will allocate from. In this case, it defines a pool named "default" with the CIDR 192.168.1.240-192.168.1.244.
An IP address pool in MetalLB defines the range of IP addresses from which MetalLB can allocate addresses for load balancers. In this configuration, a pool named "default" with the CIDR 192.168.1.240-192.168.1.244 is specified. This means that MetalLB will allocate IP addresses from the range 192.168.1.240 to 192.168.1.244.

Consequences of defining this pool named "default":

- Any Kubernetes service of type LoadBalancer that doesn't specify a specific IP address pool will use this "default" pool.
- If you need to allocate addresses from a different range for a specific service, you can define additional IP address pools with different CIDRs.

### `metallb-system/Chart.yaml`:

This file provides metadata about the Helm chart. It specifies the name, version, and dependencies of the chart. In this case, it depends on MetalLB version 0.14.3.

These configurations ensure that MetalLB is properly set up and configured within the Kubernetes cluster. They define parameters such as IP address allocation and resource requirements for MetalLB components. The configurations are managed and synced with the cluster using ArgoCD, ensuring consistency between the desired and actual states of the cluster.

## Conclusion

MetalLB facilitates load-balancing in Kubernetes clusters, particularly useful in environments lacking native cloud-based load balancers. By following these steps, you can configure MetalLB in Layer 2 mode (ARP) to efficiently manage load balancing tasks within your Kubernetes cluster.

By understanding these concepts and their roles within MetalLB, you can effectively configure and manage load balancing within your Kubernetes cluster.

### IPs:

- 192.168.1.241 : ingres internal
- 192.168.1.242 : ingres external
- 192.168.1.243 : #kanidmd
- 192.168.1.244 : wireguard
- 192.168.1.245 : 


- 192.168.1.231 : #jellyfin
- 192.168.1.232 : #navidrome
- 192.168.1.233 : #radarr
- 192.168.1.234 : #sonarr
- 192.168.1.235 : #prowlarr
- 192.168.1.236 : qbittorrent
- 192.168.1.237 : unifi
- 192.168.1.238 : hass
