# Nginx

Nginx is a popular open-source web server, reverse proxy server, and load balancer. It's known for its high performance, scalability, and reliability, making it widely used in production environments to serve web content, handle HTTP requests, and perform load balancing tasks.

## Key Features of Nginx:

- **Web Server:** Nginx can serve static and dynamic content over HTTP and HTTPS protocols. It efficiently handles client requests and serves web pages, images, videos, and other web resources.

- **Reverse Proxy:** Nginx can act as a reverse proxy server, forwarding client requests to backend servers and then returning the responses to clients. This enables load balancing, caching, and SSL termination at the reverse proxy layer.

- **Load Balancer:** Nginx can distribute incoming traffic across multiple backend servers to improve performance, reliability, and scalability. It supports various load balancing algorithms and can perform health checks to ensure that traffic is routed to healthy servers.

- **TLS/SSL Termination:** Nginx can terminate TLS/SSL connections, decrypting encrypted traffic from clients and then forwarding unencrypted traffic to backend servers. This offloads the computational overhead of encryption from backend servers and enables centralized management of TLS certificates.

Nginx is highly configurable and can be extended with third-party modules to add additional functionality. It's commonly used as a front-end web server and load balancer in Kubernetes clusters to route traffic to applications running in pods.

## Ingress-nginx Service Configurations:

### 1. system/ingress-nginx-external/Chart.yaml:

This file provides metadata about the Helm chart used for deploying the Ingress-nginx controller.

- `apiVersion`: Specifies the API version of the Helm chart (v2 in this case).
- `name`: Specifies the name of the Helm chart (ingress-nginx).
- `version`: Specifies the version of the Helm chart (0.0.0).
- `dependencies`: Lists the dependencies of the Helm chart, in this case, it depends on the Ingress-nginx chart version 4.10.0.

### 2. /srv/Projects/homelab/system/ingress-nginx-external/values.yaml:

This file contains configuration values for the Ingress-nginx controller. Here's a detailed breakdown of the configurations:


- **Admission Webhooks:** Specifies configuration for admission webhooks, including a timeout of 30 seconds.
  
- **Replica Count:** Sets the desired number of replicas for the controller to 2.
  
- **Config:** Configures additional settings for the NGINX server, such as HTTP snippets, handling of forwarded headers, and annotation support.
  
- **Ingress Class Resource:** Defines the Ingress class resource for the controller, specifying its name, enabling it, and setting a custom value for the controller.

- **Ingress Class:** Specifies the name of the Ingress class as "nginx-external".
  
- **Resources:** Sets resource requests and limits for the controller pods.
  
- **Affinity:** Configures node affinity to prefer scheduling the controller pods on specific nodes based on various criteria.
  
- **Autoscaling:** Enables autoscaling for the controller with a minimum of 2 replicas, a maximum of 11 replicas, and target CPU and memory utilization percentages.
  
- **Topology Spread Constraints:** Defines constraints to spread controller pods across nodes evenly based on hostname.
  
- **Service:** Configures the Kubernetes service for the Ingress-nginx controller, enabling HTTP and HTTPS, setting ports, and specifying LoadBalancer type with annotations for MetalLB integration.
  
- **Extra Volume Mounts and Extra Volumes:** Mounts an extra volume to the controller pods for shared memory usage.
  
- **Metrics:** Enables metrics collection and sets up a ServiceMonitor for monitoring.
  
- **TCP:** Specifies TCP ports to expose and their corresponding backend services.

### 3. Consequences:

The configuration ensures that the Ingress-nginx controller is deployed with the specified resources, including CPU and memory limits, and replica count. Autoscaling is enabled for the controller, allowing it to dynamically adjust the number of replicas based on CPU and memory utilization. Topology spread constraints ensure that controller pods are distributed across nodes in a balanced manner. The Kubernetes service for the Ingress-nginx controller is configured as a type LoadBalancer, allowing external traffic to be routed to the controller. Additional annotations and configurations are applied to the service, including the use of MetalLB for load balancing (`metallb.universe.tf/loadBalancerIPs`) and enabling HTTP and HTTPS traffic. Metrics collection is enabled for monitoring purposes.

By understanding these configurations, you can effectively deploy and manage the Ingress-nginx controller within your Kubernetes cluster, ensuring efficient and reliable routing of external traffic to your applications.
