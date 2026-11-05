<!-- FILE: services/example-vm-hosting/rsm.md -->
<!-- Resource-Service Model for EXAMPLE-VM-HOSTING.
     Example service specification for OSS framework -->

# Resource-Service Model: EXAMPLE-VM-HOSTING

**Service:** Example Cloud Platform Delivery
**Product:** [`products/platform/`](../../products/platform/)
**Version:** 0.85
**Date:** 2026-03-02

---

## Legend

| Type | Description |
|---|---|
| 🔷 Box | Component/subsystem operated by @platform-team |
| 🔶 Box | Component operated by external provider |
| ➡️ Arrow | Dependency / resource consumption |

---

## Overall RSM Diagram

```mermaid
graph TD
    SVC["EXAMPLE-VM-HOSTING\n(Customer Platform Instance)"]

    subgraph "Platform Layer"
        VMW_COMP["Virtualization Platform\n(compute cluster)"]
        VMW_MGMT["Virtualization Platform\n(management cluster)"]
        PORTAL["Management Portal + Terminal Servers\n(customer console)"]
    end

    subgraph "Infrastructure Layer"
        COMPUTE["Compute Infrastructure\n(servers)"]
        STORAGE["Storage Infrastructure\n(storage systems, SAN)"]
        NETWORK["Network Infrastructure\n(switches, routers, firewalls)"]
        SEC["Security Subsystem\n(Platform Security)"]
        MON["Monitoring Subsystem"]
        INFRA_SVC["Infrastructure Services\n(DNS, NTP, Directory)"]
        BACKUP["Backup Subsystem"]
    end

    subgraph "External Providers"
        DC["Data Center Engineering\n(@infra-team)"]
        ISP["External Connectivity\n(@infra-team)"]
    end

    SVC --> VMW_COMP
    SVC --> PORTAL
    VMW_COMP --> COMPUTE
    VMW_COMP --> STORAGE
    VMW_COMP --> NETWORK
    VMW_MGMT --> VMW_COMP
    PORTAL --> VMW_MGMT
    PORTAL --> NETWORK
    SEC --> VMW_COMP
    SEC --> NETWORK
    MON --> VMW_COMP
    MON --> STORAGE
    MON --> NETWORK
    INFRA_SVC --> VMW_MGMT
    BACKUP --> STORAGE
    COMPUTE --> DC
    STORAGE --> DC
    NETWORK --> DC
    NETWORK --> ISP
```

---

## РСМ — Телекоммуникационная инфраструктура

Обеспечивает сетевую связность внутри ВЦОД, межсетевое экранирование и доступ в Интернет.

```mermaid
graph LR
    subgraph "Телекоммуникационная инфраструктура"
        SW_AGG["Агрегационные коммутаторы"]
        SW_TOR["ToR-коммутаторы (Top-of-Rack)"]
        FW["Виртуальные МСЭ\n(Stateful-Firewall)"]
        GW["Шлюзы / маршрутизаторы"]
        VLAN_POOL["Пул VLAN\n(изолированные сегменты)"]
    end
    SW_TOR --> SW_AGG
    SW_AGG --> GW
    FW --> SW_AGG
    VLAN_POOL --> SW_TOR
    GW --> ISP["External Connectivity\n(@infra-team)"]
```

| Component | Type | Owner |
|---|---|---|
| Aggregation switches | Physical | @platform-team |
| ToR switches | Physical | @platform-team |
| Virtual firewalls | Virtual | @platform-team |
| Gateways/routers | Physical | @platform-team |
| External connectivity | Service | @infra-team |

---

## Storage Infrastructure

Provides three storage types with different IOPS and latency characteristics.

```mermaid
graph LR
    subgraph "Storage Infrastructure"
        SAN["Storage Network (SAN)"]
        SSD_NVMe["Storage Type 3\n(NVMe, latency ≤5ms, 2000 IOPS/TB)"]
        SSD["Storage Type 2\n(SSD, latency ≤20ms, 200 IOPS/TB)"]
        HDD["Storage Type 1\n(HDD, latency ≤100ms, 20 IOPS/TB)"]
    end
    SAN --> SSD_NVMe
    SAN --> SSD
    SAN --> HDD
```

---

## РСМ — Платформа виртуализации VMware (кластер вычислений)

```mermaid
graph LR
    subgraph "Кластер вычислений"
        vCenter["vCenter Server"]
        ESXi_1["ESXi Гипервизор 1"]
        ESXi_N["ESXi Гипервизор N"]
        VTSOD["ВЦОД Потребителя\n(VM Pool, Resource Pool)"]
    end
    vCenter --> ESXi_1
    vCenter --> ESXi_N
    ESXi_1 --> VTSOD
    ESXi_N --> VTSOD
```

**Параметры лимитов платформы VMware:**

| Параметр | Мин | Макс |
|---|---|---|
| vCPU для одной ВМ | 1 | 48 |
| vRAM для одной ВМ | 1 Гб | 768 Гб |
| vHDD для одной ВМ | 1 Гб | 15 ТБ |
| Кол-во vHDD для одной ВМ | 1 | 26 |
| vNIC для одной ВМ | 1 | 10 |
| Пропускная способность vNIC | 1 Гбит/с | 10 Гбит/с |
| VLAN | 10 | 400 |
| Пропускная способность МСЭ | 2 Гбит/с | 10 Гбит/с |
| Терминальных серверов | 1 | 6 |
| Сетевых шлюзов | 1 на VLAN | — |

---

## РСМ — Подсистема мониторинга

```mermaid
graph LR
    subgraph "Подсистема мониторинга"
        MON_SRV["Серверы мониторинга"]
        MON_AGENTS["Агенты сбора метрик"]
        ALERTS["Система алертинга"]
    end
    MON_AGENTS --> MON_SRV
    MON_SRV --> ALERTS
```

Хранение исторических данных: **6 месяцев**.
