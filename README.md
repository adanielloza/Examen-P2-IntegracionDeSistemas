# Examen P2 – Integración de Sistemas

Este repositorio contiene la solución completa para el Proyecto de Integración de Sistemas de la Universidad, donde integramos tres microservicios (REST, SOAP y JWT) dentro de un Service Mesh con Istio, expuestos a través de un API Gateway. También aplicamos patrones de resiliencia (reintentos y circuit-breaker) y habilitamos monitoreo y trazabilidad.

---

## 🔍 Visión General

- **AcademicService** (FastAPI)  
  - Endpoints:  
    - `POST /solicitudes`  
    - `GET  /solicitudes/{id}`  
  - Verifica JWT contra **SecurityService** y llama al mock SOAP de **CertificationService**.  
- **SecurityService** (FastAPI)  
  - Endpoint:  
    - `GET /verify`  
  - Decodifica y valida tokens JWT (HS256).  
- **CertificationService** (Spyne SOAP)  
  - Operación SOAP: `RegisterCert(studentId, type) → bool`  
  - Mock que siempre responde éxito.  
- **Kong API Gateway** (opcional) o Istio Ingress Gateway / VirtualService para exponer `/verify` y `/solicitudes` con un solo punto de entrada.  
- **Istio** (demo profile)  
  - Side-car injection en cada pod.  
  - **Gateway** + **VirtualService** para enrutar tráfico HTTP.  
  - **DestinationRule** + **VirtualService** para circuit-breaker y retry en la llamada SOAP.  
- **Observabilidad**  
  - **Prometheus** scrapea métricas de Envoy y apps.  
  - **Grafana** dashboards (P50/P95, error rate, retries, ejections).  
  - **Jaeger** trazas distribuidas (Client → Academic → Security → Cert).  
  - **Kiali** vista topológica y health overview.

---

## 🏗️ Diagrama de Arquitectura

Ubicado en `/docs/architecture.png`.  
- Caja **Service Mesh** englobando los tres servicios + side-cars  
- Flechas:  
  - Client → (Kong / Istio Gateway) → AcademicService → SecurityService  
  - AcademicService → CertificationService (⚡ Circuit-Breaker + Retry=2)  
- Debajo: Istio Control-Plane (istiod)  
- Al lado: Prometheus, Jaeger, Kiali conectados a Envoy

---

## ⚙️ Desarrollo Local

### 1. Crear entornos virtuales e instalar dependencias

Para cada servicio (`SecurityService`, `AcademicService`, `CertificationService`):

```bash
cd <ServiceFolder>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
│
├── AcademicService/
│   ├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── SecurityService/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── CertificationService/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── k8s/
│   ├── security-deploy.yaml
│   ├── academic-deploy.yaml
│   ├── cert-deploy.yaml
│   ├── istio-gateway.yaml
│   ├── istio-virtualservices.yaml
│   └── soap-cb-retry.yaml
│
└── docs/
    ├── architecture.png
    └── observabilidad.md
