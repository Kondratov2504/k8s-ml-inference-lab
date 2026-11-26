# k8s-ml-inference-lab

Учебная лабораторная работа по дисциплине **«Автоматизация машинного обучения»** (магистратура, направление «Прикладная информатика: Инженерия искусственного интеллекта»).

Цель — закрепить базовые концепции Kubernetes на примере ML-сервиса инференса: `Namespace`, `Pod`, `Deployment`, `Service`, манифесты, `kubectl`, масштабирование и обновление. Лабораторная выполняется в три этапа: от заглушки на `lorem` до реальной модели.

## Предварительные требования
| Инструмент | Версия | Назначение |
|---|---|---|
| Docker Desktop | 4.x | Сборка образа + локальный кластер Kubernetes |
| `kubectl` | 1.28+ | Управление кластером |
| Python | 3.11+ | Локальный запуск приложения |
| `curl` / Postman | — | Проверка API |

**Основной сценарий — Windows + Docker Desktop:** включите встроенный кластер
Kubernetes (Settings → Kubernetes → Enable Kubernetes) и дождитесь статуса
`Ready`:

```bash
kubectl get nodes
```
**Для Linux (ноутбуки без Docker Desktop)** используется minikube:
```bash
minikube start --driver=docker
```
Отличий для minikube ровно два: загрузка образа в кластер (```minikube image load```) и доступ к сервису (```minikube service``` или ```port-forward```).

## Структура репозитория
```text
k8s-ml-inference-lab/
├── README.md
├── stages/
│   ├── 01-lorem/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── requirements.txt
│   │   │   └── Dockerfile
│   │   └── k8s/
│   │       ├── namespace.yaml
│   │       ├── deployment.yaml
│   │       └── service.yaml
│   ├── 02-size-param/
│   └── 03-titanic/
└── docs/
    └── kubectl-cheatsheet.md
```
Каждый этап — самостоятельный каталог: своё приложение, свой Dockerfile, свои манифесты. Имя репозитория не привязано к конкретному заданию, поэтому новые задания добавляются как новые этапы.
**Пространство имён**. Каждый студент работает в своём namespace: ml-inference-studentNN (NN — порядковый номер по списку). Замените NN во всех командах на свой номер.

## Этапы
| Этап | Версия образа | Что добавляется | Что закрепляется в K8s |
|---|---|---|---|
|1|inference-api:v1.0|FastAPI + заглушка lorem, эндпоинт /infer без параметров|Namespace, Deployment, Pod, Service, port-forward, scale, rollout
|2|inference-api:v2.0|Параметр size (sentence / paragraph / text)|Обновление образа, kubectl set image, rollout undo
|3|inference-api:v3.0|Реальная модель по варианту (пример — «Титаник»)|Та же инфраструктура, меняется только контейнер

Архитектура K8s на всех этапах не меняется — меняется только образ и API. Это ключевой методический момент: инфраструктура стабильна, приложение эволюционирует.

## Быстрый старт (этап 1) 
```bash
# 1. Локальная проверка приложения (по желанию)
python3 -m venv .venv
source .venv/bin/activate            # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r stages/01-lorem/app/requirements.txt
uvicorn main:app --app-dir stages/01-lorem/app
# проверка: http://localhost:8000/health

# 2. Сборка образа
cd stages/01-lorem/app
docker build -t inference-api:v1.0 .

# 3. Развёртывание
kubectl apply -f ../k8s/namespace.yaml
kubectl apply -f ../k8s/deployment.yaml
kubectl apply -f ../k8s/service.yaml

# 4. Проверка
kubectl get all -n ml-inference-studentNN
curl http://localhost/infer
```