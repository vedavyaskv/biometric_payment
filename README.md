# 🛡️ BioPay: Secure Biometric Payment System

BioPay is a secure digital wallet application that replaces traditional PINs and passwords with **Targeted Biometric Authentication**. By combining facial recognition, liveness detection (blink test), and QR technology, it ensures that transactions can only be authorized by the actual account holder.

## 🚀 Key Features

* **Targeted Identity Verification**: Strictly matches the person in the camera against the specific ID attempting the transaction to prevent identity fraud.
* **Active Liveness Detection**: Integrated "Blink Test" prevents spoofing attacks using static photos or videos.
* **Dual-ID Payment Terminal**: Supports both manual Bio-ID entry and high-speed QR code scanning.
* **Professional Transaction UI**: Features a custom CSS-animated success tick and detailed digital receipts.
* **Automated Wallet Management**: Real-time balance deduction and transaction logging within localized JSON metadata.
* **Biometric Directory**: Visual management of registered profiles with the ability to view unique QR codes or purge data.

---

## 🛠️ Technical Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend UI** | Streamlit (Python Framework) |
| **Computer Vision** | OpenCV (Open Source Computer Vision Library) |
| **Machine Learning** | Local Binary Patterns Histograms (LBPH) |
| **Data Storage** | JSON (Local Metadata) |
| **QR Engine** | Python-QRCode & OpenCV Detector |
| **Serialization** | Pickle (Label Mapping) |

---

## 🧠 Biometric Architecture & ML Logic

### 1. Facial Recognition (LBPH Algorithm)
The system utilizes the **Local Binary Patterns Histograms (LBPH)** recognizer. 
* **Mechanism**: Summarizes local structures in images by comparing each pixel with its neighbors. It is robust against changes in lighting and facial expressions.
* **Training**: During registration, 30 grayscale samples of the face are captured and trained into a `.yml` model.

### 2. Strict Identity Mapping (The "Targeted" Fix)
To prevent unauthorized users from accessing other accounts, we implemented a mapping system:
* **Label Mapping**: During training, folder names are mapped to unique integer IDs in `labels.pkl`.
* **Restrictive Auth**: The system retrieves the logged-in user's specific ID and only returns `True` if the camera prediction matches that ID exactly.

### 3. Liveness Check (Blink Detection)
To ensure a real human is present, the system uses a **Haar Cascade Eye Detector**.
* **Temporal Logic**: Requires a "Closed-Open" eye sequence across multiple frames.
* **Debouncing**: A blink is registered only if eyes are missing for at least 2 consecutive frames and then re-detected.

---

## 📂 Project Structure

```text
biometric_payment_system/
├── app.py                # Main Streamlit Application
├── face_auth.py          # Secure Targeted Face Verification
├── blink_auth.py         # Liveness (Blink) Detection Module
├── face_register.py      # Enrollment & QR Generation Engine
├── model_utils.py        # ML Training & Label Mapping Logic
├── user_utils.py         # JSON Metadata & Wallet Management
├── dataset/              # Biometric Sample Storage (Folders per user)
└── model/                # Trained .yml models and labels.pkl
🔧 Installation & Implementation
1. Prerequisites
Python 3.9 or higher

Functioning Webcam

2. Install Dependencies
pip install streamlit opencv-contrib-python qrcode[pil] numpy plotly geocoder

3. Run the Application
streamlit run app.py

4. Standard Workflow
Enroll: Use the REGISTER tab to capture your face and generate your Bio-ID.

Verify: Go to the HOME tab and use Secure Balance to biometrically lock your session.

Pay: In the PAYMENT tab, scan a QR or enter a Bio-ID. Complete the two-step verification (Face + Blink) to send money.
