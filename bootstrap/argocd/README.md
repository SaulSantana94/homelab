Usefull commands:

Reset admin password:

kubectl patch secret argocd-secret -n argocd -p '{"data": {"admin.password": null, "admin.passwordMtime": null}}'
kubectl delete pods -n argocd -l app.kubernetes.io/name=argocd-server
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d


Get Pods from argo

kubectl -n argocd get pods
kubectl -n argocd get secrets

Delete all Pods from argo
kubectl delete pods --all --namespace=argocd

Execute commands inside the pods:
kubectl exec -n argocd argocd-server-6dfc58bc9f-4z77c -- argocd --server argocd-server:8080 app sync argocd

Forward ports
kubectl port-forward -n vault service/vault 8200:8200
kubectl port-forward -n argocd service/argocd-server 8443:443


Secrets:
kubectl describe externalsecret argocd-secret  -n argocd
kubectl get externalsecrets -n argocd
kubectl get externalsecrets --all-namespaces
Refresh secret: kubectl patch externalsecret argocd-secret -n argocd --type=merge -p '{"metadata":{"annotations":{"kubectl.kubernetes.io/last-applied-configuration":"{}"}}}'

Logs:
kubectl -n argocd logs  argocd-server-6dfc58bc9f-btxck


Identify mount path of persistent volume:
mount | rg pvc-048a842f-a6f5-48ff-a5e1-aea53fef9c59

Copy data to volume
rsync -avz -e "ssh" dabol@192.168.1.249:/media/dabol/Data/data/MediaServer/Music/ /var/lib/kubelet/pods/39e85c56-cf58-4796-a716-9ca984b3ddbd/volumes/kubernetes.io~csi/pvc-048a842f-a6f5-48ff-a5e1-aea53fef9c59/mount


