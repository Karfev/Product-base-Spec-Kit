<!-- FILE: services/example-vm-hosting/external-spec.md -->
<!-- External specification for EXAMPLE-VM-HOSTING v0.6
     Example service specification for OSS framework -->

# External Specification: EXAMPLE-VM-HOSTING

**Service Code:** EXAMPLE-VM-HOSTING
**Service Class:** Platform IaaS (Example Virtual Data Center)
**Service Name:** Example Cloud Platform as a Virtual Data Center Service
**Short Name:** EXAMPLE-VM-HOSTING
**Service Owner:** @platform-team
**Internal Specification:** [`internal-spec.md`](./internal-spec.md)
**Scope:** Business Service
**Criticality:** Critical
**Version:** 0.6
**Date:** 2026-03-02

---

## 1. Service Purpose

Delivery of a virtual data center cloud platform and compute resources to customers using Infrastructure-as-a-Service (IaaS) model.

---

## 2. Service Delivery Terms

### 2.1 Service Functionality and Composition

The service includes:

- Delivery of logically isolated data center infrastructure with specified resource characteristics
- Internet connectivity with dedicated public IP address allocation
- Network segmentation and firewall protection
- Unified management console interface for the cloud platform
- Remote console access via Internet using certified VPN client and terminal server(s)

Upon customer request, the provider performs: virtual firewall configuration, access rule creation, VLAN setup, NAT configuration, and user account management.

IT infrastructure is certified at standard security levels. Third-party certification applies.

Полный перечень функциональных требований — в [`requirements.yml`](./requirements.yml).

#### 2.1.1 Cloud Platform Functional Characteristics

| Parameter | Minimum | Maximum |
|---|---|---|
| vCPU per VM | 1 | 48 |
| vRAM per VM | 1 GB | 768 GB |
| vHDD per VM | 1 GB | 15 TB |
| Number of vHDD per VM | 1 | 26 |
| vNIC bandwidth | 1 Gbps | 10 Gbps |
| vNIC per VM | 1 | 10 |
| VLANs | 10 | 400 |
| Firewall (Stateful) throughput | 2 Gbps | 10 Gbps |
| Terminal servers for console | 1 | 6 |
| Network gateways | 1 per VLAN | — |
| Network pools | No limits | — |
| Platform users | No limits | — |

#### 2.1.2 Management Console Functional Characteristics

The management console provides: VM creation/start/stop/delete; resource adjustment (vCPU/vRAM/vHDD); hot-add capabilities; snapshot creation; template deployment; OVF import/export; affinity rule configuration; resource usage statistics visualization.

### 2.2 Billable Parameters

> Machine-readable reference: [`billing/parameters.yml`](./billing/parameters.yml)

| Parameter | Unit | Step |
|---|---|---|
| Processor cores, vCPU | qty | 4 |
| RAM, vRAM | GB | 16 |
| Storage type 1 (HDD) | GB | 1000 |
| Storage type 2 (SSD) | GB | 500 |
| Storage type 3 (NVMe) | GB | 500 |
| Internet access channel | Mbps | 100 |
| Public IPv4 address | qty | 1 |
| VLAN | qty | 10 |
| Firewall throughput | Mbps | 500 |
| VPN client | qty | 1 |
| Terminal server | qty | 1 |
| Premium SQL license, 2 cores | qty | 1 |
| Remote desktop license, 1 user | qty | 1 |

### 2.3 Quality Characteristics

> Machine-readable reference: [`ops/slo.yaml`](./ops/slo.yaml)

| Parameter | Specification |
|---|---|
| vCPU base frequency | 2.9 GHz |
| vCPU wait time | max 10% |
| vRAM swap overhead | max 10% of configured |
| HDD latency | max 100 ms |
| HDD IOPS | 20 IOPS/TB |
| SSD latency | max 20 ms |
| SSD IOPS | 200 IOPS/TB |
| NVMe latency | max 5 ms |
| NVMe IOPS | 2000 IOPS/TB |
| Internal network latency | max 10 ms |
| Internal packet loss | max 0.2% |
| Internet latency | max 10 ms |
| Internet packet loss | max 0.5% |
| Traffic volume | unlimited |

### 2.4 Limitations

The provider does **not** offer:

- Configuration, modification, or upgrade of customer application and system software
- Monitoring of customer VM availability and performance
- Security measures for customer infrastructure

The provider is not responsible for recovery of lost VMs, files, data, or software due to customer actions.

### 2.5 Quality Monitoring

The provider performs 24/7 monitoring of infrastructure components, compute resources, connectivity, and quality metrics. Values exceeding limits are classified as incidents per [`ops/incident-catalog.yml`](./ops/incident-catalog.yml).

Monitoring data retention: **6 months**.

### 2.6 Billing

Billing is performed each billing period. Service volume is defined in the contract prior to the period start.

Billing parameters are in [`billing/parameters.yml`](./billing/parameters.yml).

### 2.7 Onboarding / Offboarding

- **Resource allocation:** 5 business days from contract signature.
- **Credentials delivery:** within 2 business days (email); includes VPN client and encryption keys.
- **Customer setup:** within 3 business days of receiving credentials.
- **Service start:** 6th business day after contract signature.
- Technical connection terms are in [`appendices/connection-guide.md`](./appendices/connection-guide.md).

The provider does not develop infrastructure documentation or perform acceptance testing.

### 2.8 Change Implementation

> Machine-readable reference: [`ops/change-catalog.yml`](./ops/change-catalog.yml)

Changes are implemented based on customer change requests.

**Standard change:**
- Effective period: **4 calendar months** (from change implementation date)
- Implementation time: per change request SLT
- Billing rules: increases in period are billed at new level for full period; decreases apply next period

**Non-standard change** (outside `change-catalog.yml`):
- Technical feasibility review: **20 business days**
- Maximum implementation time: **4 calendar months**

---

## 3. Technical Support

The provider offers technical support throughout the service delivery period.

Support channels:
- Hotline (phone + email): business days 09:00–18:00 UTC+3
- ServiceDesk system: 24x7

### 3.1 Incident Resolution

> Machine-readable reference: [`ops/incident-catalog.yml`](./ops/incident-catalog.yml)

Classification, thresholds, and SLTs are in `incident-catalog.yml`.

**Incident**: unplanned failure, equipment/software outage, or event causing service quality degradation or interruption.

### 3.2 Standard Requests

> Machine-readable reference: [`ops/request-catalog.yml`](./ops/request-catalog.yml)

9 request types (3 service requests, 2 change requests, 3 information requests + ad-hoc). Full catalog in `request-catalog.yml`. Forms in [`appendices/request-forms.md`](./appendices/request-forms.md).

---

## 4. Quality Parameters

> Machine-readable reference: [`ops/slo.yaml`](./ops/slo.yaml)

### 4.1 Availability

| Parameter | Value |
|---|---|
| Service hours | 24x7x365 |
| Availability target | 99.5% |
| Single outage limit | max 3 hours |
| Maintenance windows per quarter | max 1 |
| Maintenance window duration | max 3 hours |

**Approved outages:**

| Category | Duration | Notice |
|---|---|---|
| Maintenance | max 12 h/year, min 30 day intervals | 3 business days |
| Critical updates | actual install time | immediately before |

### 4.2 Service Level Targets

> Full SLTs in [`ops/incident-catalog.yml`](./ops/incident-catalog.yml) and [`ops/request-catalog.yml`](./ops/request-catalog.yml)

| Priority | Response | Resolution | Mode |
|---|---|---|---|
| 1 (Critical) | 10 min | 1.5 h | 24x7 |
| 2 (High) | 15 min | 2 h | 24x7 |
| 3 (Medium) | 15 min | 4 h | 24x7 |
| 4 — Service requests | 30 min | 4 h | Business hours |
| 4 — Info requests | 30 min | 16 h | Business hours |

---

## 5. Reporting

Reports are provided at period end:

- **Service Availability** — incident count, total downtime, availability %
- **Support Activity & SLA** — avg/max response/resolution time, % SLA violations by category

Formats: `.pdf`, `.doc(x)`, `.xls(x)`. Delivery: email.
Report templates in [`appendices/report-templates.md`](./appendices/report-templates.md).

---

## 6. Acceptance

- Provider delivers reports, acceptance documents, invoices within **5 business days** of period end.
- Customer signs acceptance or submits objections within **3 business days**.
- Service is accepted without objections if no response within **15 business days** of document delivery.
- For objections: bilateral document listing issues; dispute resolution per contract.
