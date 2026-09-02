# Fuzzy-Bayesian Streaming Anomaly & Fraud Detection

A real-time fraud detection system that combines **Fuzzy Logic** and **Bayesian risk modeling** to detect suspicious transaction patterns.

Traditional fraud systems often depend on fixed rules such as:

`IF amount > $10,000 → FLAG`

This can be easily bypassed by spreading transactions across smaller amounts. This project instead looks at multiple behavioral signals and calculates risk continuously.

## How It Works

```text
Transaction
     ↓
Kafka / Redpanda
     ↓
Stream Consumer
     ↓
Redis Feature Store
     ↓
Feature Engineering
     ↓
Fuzzy Logic Engine
     ↓
Risk Score
     ↓
Bayesian / Probability Fusion
     ↓
Decision Engine
     ↓
Approve / Verify / Challenge / Block
```

## Main Features

* Real-time transaction stream processing
* Transaction velocity detection
* Amount deviation analysis
* Geographic speed detection
* Behavioral drift detection
* Fuzzy Logic based risk scoring
* Bayesian-inspired risk probability
* Cold-start handling for new users
* Redis-based real-time state
* PostgreSQL audit logging
* Fraud alert streaming
* Live Streamlit monitoring dashboard
* Explainable decisions
* Robust error and fallback handling

## Technology Stack

* **Python**
* **Apache Kafka / Redpanda**
* **Redis**
* **PostgreSQL**
* **scikit-fuzzy**
* **FastAPI**
* **Streamlit**
* **Docker**

## Example Risk Signals

The system looks at signals such as:

* Too many transactions in a short period
* Unusually large or unusually small transaction amounts
* Impossible geographic movement
* Sudden changes in spending behavior
* High transaction volume
* New or suspicious devices
* Suspicious IP or device context

Instead of treating each signal as simply `true` or `false`, the system evaluates how strongly each signal indicates risk.

## Fuzzy Logic

Fuzzy Logic converts numerical values into gradual risk levels.

For example:

```text
Velocity = 3 transactions
→ Low risk

Velocity = 8 transactions
→ Moderate risk

Velocity = 15 transactions
→ High/Burst risk
```

This allows the system to handle situations where the boundary between normal and suspicious behavior is not clear.

## Bayesian Risk

The system maintains a historical risk state for each user.

New evidence updates the previous risk estimate:

```text
Previous Risk
     +
New Evidence
     ↓
Updated Risk Probability
```

The final probability is then used by the decision engine.

## Decision System

The system does not rely only on `Approve` or `Block`.

```text
Tier 0 → Silent Approval
Tier 1 → Silent Verification
Tier 2 → Soft Challenge
Tier 3 → Hard Block
```

High-risk decisions can also use hysteresis so that a single noisy transaction does not immediately cause a hard block.

## Reliability

The system is designed to handle:

* Missing data
* Invalid data
* Insufficient user history
* Zero variance
* Missing location information
* Out-of-order events
* Infrastructure failures
* Numerical edge cases

Features maintain explicit states such as:

```text
VALID
UNKNOWN
INVALID
```

so that missing information is never incorrectly treated as zero risk.

## Project Goal

The main goal is to build a **low-latency, explainable, streaming fraud detection system** that demonstrates how soft computing, probabilistic reasoning, and modern distributed systems can work together.

The target is a decision pipeline capable of operating within a **sub-50 ms latency budget** in the final streaming architecture.

## Project Status

🚧 Currently under development.

Development will proceed in stages:

1. Mathematical foundation
2. Feature engineering
3. Fuzzy inference engine
4. Risk fusion
5. Decision engine
6. Redis integration
7. Kafka/Redpanda integration
8. PostgreSQL audit logging
9. Fraud simulation
10. Streamlit dashboard
11. Testing and benchmarking

## Disclaimer

This is an educational/research project using synthetic transaction data. It is not intended to be used as a production financial fraud prevention system without further validation, security review, monitoring, and regulatory compliance work.
