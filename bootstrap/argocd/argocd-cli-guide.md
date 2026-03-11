# Argo CD CLI Usage Guide

## Login to Argo CD Server

```bash
argocd login localhost:8080
```

### Credentials

- **Username:** `admin`
- **Password:**

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d && echo
```

## List All Applications

```bash
argocd app list
```

## Get Status of an Application

```bash
argocd app get argocd/tisdp
```

## Sync Applications

### Sync a Single Application

```bash
argocd app get argocd/tisdp
argocd app get argocd/iiotlink
```

## Sync Applications

### Sync a Single Application

```bash
argocd app sync argocd/tisdp
argocd app sync argocd/iiotlink
```

### List the Repos

```bash
argocd repo list
```


### Add a repo
kubectl create secret generic github-pot-repo -n argocd --from-literal=type=git --from-literal=url=https://github.com/lhpot/pot-stag2-vpc0-euw1-vm-sand5.git --from-literal=username=git --from-literal=password=github_pat_<your_pat> --dry-run=client -o yaml | kubectl label -f - argocd.argoproj.io/secret-type=repository --local -o yaml | kubectl apply -f -