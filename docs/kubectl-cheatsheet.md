# kubectl-cheatsheet
Шпаргалка по командам для лабораторной. В примерах `NN` - порядковый номер исполнителя.

## 1. Состояние кластера
```bash
kubectl version                        # версии клиента и кластера
kubectl get nodes                      # кластер жив? (статус Ready)
kubectl get all -n ml-inference-studentNN   # всё в одном namespace
kubectl get pods -n ml-inference-studentNN -w    # наблюдение в реальном времени
```
## 2. Развёртывание
```bash
kubectl apply -f namespace.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f k8s/                  # всё сразу из каталога

kubectl delete -f deployment.yaml      # убрать приложение (namespace не трогать)
```
## 3. Масштабирование
```bash
kubectl scale deployment inference-api --replicas=2 -n ml-inference-studentNN
```
## 4. Диагностика
```bash
kubectl describe pod <имя-пода> -n ml-inference-studentNN   # Events — в самом низу
kubectl logs <имя-пода> -n ml-inference-studentNN
kubectl logs <имя-пода> -n ml-inference-studentNN --previous # логи УПАВШЕГО контейнера
kubectl get endpoints inference-api -n ml-inference-studentNN # кто получает трафик
```
## 5. Обновление и откат
```bash
kubectl rollout status deployment/inference-api -n ml-inference-studentNN
kubectl rollout history deployment/inference-api -n ml-inference-studentNN
kubectl rollout restart deployment/inference-api -n ml-inference-studentNN  # образ пересобран под тем же тегом
kubectl rollout undo deployment/inference-api -n ml-inference-studentNN     # откат
kubectl set image deployment/inference-api inference-api=inference-api:v2.0 -n ml-inference-studentNN  # быстрый патч (без манифеста)
```
## 6. Minikube (только для Linux)
```bash
minikube start --driver=docker
minikube image load inference-api:v1.0
minikube image ls | grep inference 
minikube service inference-api -n ml-inference-studentNN
```
## 7. Доступ к API
# Docker Desktop:
```bash
curl http://localhost/infer
```
# minikube:
```bash
kubectl port-forward svc/inference-api 8080:80 -n ml-inference-studentNN # в отдельном окне!
curl http://localhost:8080/infer
```