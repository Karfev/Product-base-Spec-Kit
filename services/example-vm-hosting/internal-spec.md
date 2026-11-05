<!-- FILE: services/example-vm-hosting/internal-spec.md -->
<!-- Internal specification for EXAMPLE-VM-HOSTING v0.85
     Example service specification for OSS framework -->

# Internal Specification: EXAMPLE-VM-HOSTING

**Service Code:** EXAMPLE-VM-HOSTING
**Product:** [`products/platform/`](../../products/platform/) — Example Platform IaaS
**Service Name:** Example Cloud Platform as a Virtual Data Center Service
**Short Name:** Example VM Hosting
**Service Owner:** @platform-team
**External Specification:** [`external-spec.md`](./external-spec.md)
**Scope:** Business Service
**Criticality:** Critical
**Version:** 0.85
**Date:** 2026-03-02

---

## 1. Service Purpose

Delivery of a virtual data center cloud platform and compute resources to customers using Infrastructure-as-a-Service (IaaS) model.

---

## 2. Technology Description

### 2.1 Technical Architecture

> Detailed product architecture: [`products/platform/architecture/overview.md`](../../products/platform/architecture/overview.md)

The platform infrastructure is designed for cloud compute operations and comprises hardware, application, and system software. The system includes:

- **Compute Infrastructure** — physical servers for management (control cluster) and customer resources (compute clusters)
- **Storage Infrastructure** — shared storage with logical resource isolation (SAN zoning, storage partitioning)
- **Virtualization Platform** — management components, hypervisors for control and compute clusters
- **Network Infrastructure** — logically isolated segments of shared network fabric
- **Security Subsystem** — virtual firewalls, security controls; standard certifications apply
- **Monitoring Subsystem** — 24/7 infrastructure monitoring
- **Infrastructure Services** — supporting services
- **Management Portal** — unified management interface
- **Backup Subsystem** — data protection

**Related Systems:**

- **Data Center Engineering Infrastructure** (power, cooling, fire protection, physical access) — operated by dedicated team
- **Support System** — ticket reception, registration, and handling

**External Connectivity** ensures connection to external networks and Internet. Provisioned and maintained by connectivity provider.

**Resource Segmentation Approach:**

- Compute Infrastructure — dedicated servers; shared compute clusters across customers
- Storage Infrastructure — logical resource isolation (zoning + partitions)
- Virtualization Platform — separate management components, dedicated hypervisors
- Network Infrastructure — isolated VLAN segments
- Security Subsystem — virtual firewall isolation

### 2.2 Resource-Service Model

> Complete RSM with diagrams: [`rsm.md`](./rsm.md)

The resource-service model describes nine subsystems delivering the EXAMPLE-VM-HOSTING service:

| Subsystem | Description |
|---|---|
| Network Infrastructure | Network fabric, VLANs, firewalls, Internet channels |
| Storage Infrastructure | Storage systems, SAN zoning, three storage types |
| Security Subsystem | Virtual firewalls, security controls |
| Virtualization Platform (Control Cluster) | Management servers, control components |
| Virtualization Platform (Compute Cluster) | Hypervisors, resource pools |
| Monitoring Subsystem | Metrics and event monitoring system |
| Infrastructure Services | DNS, NTP, directory services, etc. |
| Backup Subsystem | Data protection tools |
| Management Portal + Terminal Servers | Platform console, VPN access |

---

## 3. Responsibility Distribution

> Machine-readable matrix: [`responsibilities.yml`](./responsibilities.yml)

### 3.1 By Architectural Component

| Component | Owner | Mode |
|---|---|---|
| Compute Infrastructure | @platform-team | Operate + Evolve |
| Storage Infrastructure | @platform-team | Operate + Evolve |
| Virtualization Platform | @platform-team | Operate + Evolve |
| Network Infrastructure | @platform-team | Operate + Evolve |
| Security Subsystem | @platform-team | Operate + Evolve |
| Monitoring Subsystem | @platform-team | Operate + Evolve |
| Infrastructure Services | @platform-team | Operate + Evolve |
| Management Portal | @platform-team | Operate + Evolve |
| Backup Subsystem | @platform-team | Operate + Evolve |
| Data Center Engineering | @infra-team | Operate + Evolve |
| External Connectivity | @infra-team | Operate + Evolve |
| Support System | @platform-team | Operate + Evolve |

---

## 4. Interaction Procedures

User support is provided according to internal procedures:

- **Incident Management** — internal procedures
- **Service Request Management** — internal procedures
- **Customer Interaction** — Support request handling procedures

SLTs for incidents are in [`ops/incident-catalog.yml`](./ops/incident-catalog.yml).
SLTs for requests are in [`ops/request-catalog.yml`](./ops/request-catalog.yml).
