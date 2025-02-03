from kubernetes import client, config, watch
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_kube_config():
    load_dotenv()
    kube_config_content = os.getenv('KUBE_CONFIG')
    if kube_config_content:
        config.load_kube_config_from_dict(config.kube_config.yaml.safe_load(StringIO(kube_config_content)))
    else:
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()

def monitor_nvidia_pods():
    load_kube_config()
    v1 = client.CoreV1Api()
    w = watch.Watch()

    label_selector = "runtime-class=nvidia"  # Asume que los pods de NVIDIA tienen esta etiqueta

    try:
        for event in w.stream(v1.list_pod_for_all_namespaces, label_selector=label_selector):
            pod = event['object']
            pod._status.reason
            if pod.status.phase == 'Failed' and pod.status.reason == 'UnexpectedAdmissionError':
                logger.info(f"UnexpectedAdmissionError detected - Pod: {pod.metadata.name}, Namespace: {pod.metadata.namespace}")
                try:
                    v1.delete_namespaced_pod(
                        name=pod.metadata.name,
                        namespace=pod.metadata.namespace,
                        body=client.V1DeleteOptions(propagation_policy="Background")
                    )
                    logger.info(f"Deleted pod {pod.metadata.name} in namespace {pod.metadata.namespace}")
                except client.exceptions.ApiException as e:
                    logger.error(f"Failed to delete pod {pod.metadata.name}: {e}")
    except Exception as e:
        logger.error(f"Error in watch stream: {e}")

if __name__ == "__main__":
    monitor_nvidia_pods()
