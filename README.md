# StockyAPI

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)

## 🚀 Overview
A high-security microservice architecture that implements **Bring Your Own Key (BYOK)** logic. It decouples storage from sovereignty, ensuring that the database host (me) cannot access the user's sensitive payload (you).

**Key Features:**
* **Zero-Trust Persistence:** Data is encrypted *before* it hits the disk using a KEK (Key Encryption Key) held by the user.
* **CQRS Pattern:** Separate Read/Write paths optimized for ingestion speed vs. retrieval security.
* **Ephemeral State:** Decrypted payloads exist only in memory during the request lifecycle.

## 🛠️ Tech Stack
* **Framework:** FastAPI (Python)
* **Database:** Google Firestore (NoSQL)
* **Orchestration:** GCP Cloud Scheduler
* **Cryptography:** AES-GCM (Standard Library/Cryptography)

## 🏗️ Architecture
*(If you have a diagram, link it here. If not, describe the flow briefly)*
1.  **Ingestion:** Client sends Payload + KEK -> API Encrypts with DEK -> DEK wrapped with KEK -> Stored in Firestore.
2.  **Retrieval:** Client requests ID -> API fetches Ciphertext -> Client provides KEK -> API unwraps DEK -> Payload Decrypted -> Returned.

## 🏃‍♂️ Getting Started

### Prerequisites
* Python 3.11+
* Google Cloud Service Account (Firestore)

### Installation
1.  Clone the repo
    ```bash
    git clone [https://github.com/yourusername/vault-core.git](https://github.com/yourusername/vault-core.git)
    ```
2.  Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up Environment
    ```bash
    cp .env.example .env
    # Add your FIREBASE_CREDENTIALS path in .env
    ```

## 🔒 Security Note
This repository contains the *architectural implementation*. No actual keys or production data are stored here.

## 📜 License
This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
