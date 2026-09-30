# 🛡️ CallShield AI

### AI-Powered Deepfake Voice & Video Verification for Fraud-Call Detection

<p align="center">
  <strong>Simulate the attack. Detect the manipulation. Protect the call.</strong>
</p>

<p align="center">
  CallShield AI is an AI-powered verification system designed to identify manipulated voice and video content during suspicious calls.
</p>

---

## ⚡ What is CallShield AI?

**CallShield AI** is a deepfake detection and verification system designed for fraud-call scenarios.

Instead of attempting to create deceptive media for real-world use, our system uses **controlled deepfake simulations** to test whether our detection pipeline can identify manipulated content.

For video simulation, we use **Deep-Live-Cam** as an external research/testing component to generate controlled face-swapped samples.

> **Deep-Live-Cam simulates the attack. CallShield AI detects the attack.**

The generated samples are passed into our detection pipeline, where the system analyzes the media for manipulation indicators and produces a risk assessment.

---

# 🧠 Core Concept

```text
                    CONTROLLED SIMULATION
                           │
                           ▼
                ┌──────────────────────┐
                │   Deep-Live-Cam      │
                │                      │
                │ Face-Swap Simulation │
                └──────────┬───────────┘
                           │
                           │ Simulated Deepfake
                           ▼
                ┌──────────────────────┐
                │     CALLSHIELD       │
                │      INPUT           │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   PRE-PROCESSING     │
                │                      │
                │ Frame Extraction     │
                │ Face Detection       │
                │ Audio Extraction     │
                │ Signal Preparation   │
                └──────────┬───────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
     ┌─────────────────┐       ┌─────────────────┐
     │ VIDEO ANALYSIS  │       │ AUDIO ANALYSIS  │
     │                 │       │                 │
     │ Facial Artifacts│       │ Voice Features  │
     │ Temporal Signals│       │ Spectral Signals│
     │ Frame Consistency│      │ Manipulation    │
     └────────┬────────┘       └────────┬────────┘
              │                         │
              └────────────┬────────────┘
                           ▼
                ┌──────────────────────┐
                │  MULTI-MODAL FUSION  │
                │                      │
                │ Video + Audio        │
                │ Evidence Correlation │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   RISK ASSESSMENT    │
                │                      │
                │ Authenticity Score   │
                │ Manipulation Signals │
                │ Confidence           │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    CALLSHIELD        │
                │      ALERT           │
                │                      │
                │  ✓ Authentic         │
                │  ⚠ Suspicious        │
                │  ✕ Likely Manipulated│
                └──────────────────────┘
```

---

# 🔥 Why CallShield?

Traditional fraud detection often focuses on:

```text
Phone Number
     │
     ▼
Caller Identity
     │
     ▼
Known Fraud Patterns
```

Modern scams can additionally involve **synthetically manipulated audio and video**.

CallShield introduces another verification layer:

```text
             CALL
              │
       ┌──────┴──────┐
       ▼             ▼
     AUDIO          VIDEO
       │             │
       ▼             ▼
   ANALYSIS       ANALYSIS
       │             │
       └──────┬──────┘
              ▼
        MULTI-MODAL
        VERIFICATION
              │
              ▼
        RISK ASSESSMENT
```

---

# 🏗️ System Architecture

```text
                         ┌───────────────────┐
                         │   Incoming Call   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                     ┌─────────────────────────┐
                     │     Media Capture       │
                     │                         │
                     │ Audio + Video Stream    │
                     └────────────┬────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
          ┌──────────────────┐       ┌──────────────────┐
          │  Audio Pipeline  │       │  Video Pipeline  │
          └────────┬─────────┘       └────────┬─────────┘
                   │                          │
                   ▼                          ▼
          ┌──────────────────┐       ┌──────────────────┐
          │ Feature Extraction│       │ Face / Frame     │
          │                  │       │ Analysis         │
          └────────┬─────────┘       └────────┬─────────┘
                   │                          │
                   ▼                          ▼
          ┌──────────────────┐       ┌──────────────────┐
          │ Voice Detection  │       │ Deepfake Model   │
          └────────┬─────────┘       └────────┬─────────┘
                   │                          │
                   └────────────┬─────────────┘
                                ▼
                     ┌────────────────────┐
                     │  Evidence Fusion   │
                     └──────────┬─────────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │  Risk Engine       │
                     │                    │
                     │ Authenticity       │
                     │ Confidence         │
                     │ Evidence           │
                     └──────────┬─────────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │  CALLSHIELD UI     │
                     │                    │
                     │  STATUS            │
                     │  RISK              │
                     │  EVIDENCE          │
                     └────────────────────┘
```

---

# 🧪 Deepfake Simulation Layer

CallShield requires manipulated media to validate its detection pipeline.

Rather than relying exclusively on naturally occurring fraud footage, we use a **controlled simulation environment**.

### Simulation Flow

```text
Reference Image
       │
       ▼
┌───────────────────┐
│  Deep-Live-Cam    │
│                   │
│ Controlled        │
│ Face-Swap         │
│ Simulation        │
└─────────┬─────────┘
          │
          ▼
 Simulated Deepfake
          │
          ▼
┌───────────────────┐
│    CallShield     │
│     Detector      │
└─────────┬─────────┘
          │
          ▼
Manipulation Analysis
          │
          ▼
 Detection Result
```

### Why use simulation?

Controlled generation allows us to create test cases where the manipulation source is known.

For example:

```text
Original Video
      │
      ├──► Authentic Sample
      │
      └──► Controlled Face-Swap
                    │
                    ▼
              Deepfake Sample
                    │
                    ▼
              CallShield Model
                    │
                    ▼
             Compare Results
```

This provides a reproducible environment for evaluating the detector.

---

# 👁️ First-View Detection

One of CallShield's key concepts is **early media verification**.

Instead of requiring a user to manually inspect an entire recording, the system begins analyzing the incoming media as soon as it becomes available.

```text
VIDEO FRAME
     │
     ▼
┌───────────────┐
│ Face Detection│
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Frame Analysis│
└───────┬───────┘
        │
        ▼
┌──────────────────┐
│ Temporal Analysis│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Manipulation     │
│ Indicators       │
└────────┬─────────┘
         │
         ▼
   Initial Risk
   Assessment
```

The first-view result is treated as an **early warning signal**, not as an absolute proof of manipulation.

---

# 🎙️ Audio Verification

The same principle can be applied to suspicious voice communication.

```text
VOICE STREAM
     │
     ▼
Audio Preprocessing
     │
     ▼
Feature Extraction
     │
     ├───────────────┐
     │               │
     ▼               ▼
Spectral Features   Temporal Features
     │               │
     └───────┬───────┘
             ▼
       Voice Model
             │
             ▼
      Manipulation
        Analysis
             │
             ▼
       Risk Signal
```

Potential signals can include:

* Spectral inconsistencies
* Temporal irregularities
* Synthetic voice characteristics
* Abnormal acoustic patterns
* Model confidence

---

# 🔗 Multi-Modal Verification

A major part of CallShield is combining evidence instead of relying on one signal.

```text
                 ┌──────────────┐
                 │    AUDIO     │
                 └──────┬───────┘
                        │
                        ▼
                  Audio Signal
                        │
                        │
                        ▼
                 ┌──────────────┐
                 │    FUSION    │
                 │    ENGINE    │
                 └──────┬───────┘
                        ▲
                        │
                        │
                  Video Signal
                        ▲
                        │
                 ┌──────┴───────┐
                 │    VIDEO     │
                 └──────────────┘

                        │
                        ▼
                 ┌──────────────┐
                 │ RISK ENGINE  │
                 └──────┬───────┘
                        │
                        ▼
             ┌────────────────────┐
             │  VERIFICATION      │
             │                    │
             │ Authentic          │
             │ Suspicious         │
             │ Manipulated        │
             └────────────────────┘
```

---

# 📊 Detection Result

CallShield is designed to provide more than a binary answer.

Example:

```text
╔══════════════════════════════════════╗
║          CALLSHIELD RESULT           ║
╠══════════════════════════════════════╣
║                                      ║
║  STATUS       : SUSPICIOUS           ║
║                                      ║
║  VIDEO SIGNAL : HIGH RISK            ║
║  AUDIO SIGNAL : LOW RISK             ║
║                                      ║
║  CONFIDENCE   : 87%                  ║
║                                      ║
║  SIGNALS DETECTED:                   ║
║    • Facial inconsistency            ║
║    • Temporal artifact               ║
║    • Frame-level anomaly             ║
║                                      ║
╚══════════════════════════════════════╝
```

The system can expose the **evidence behind a decision**, making the result more useful for verification than a simple "AI says fake."

---

# 🧩 Major Components

```text
CALLSHIELD
│
├── 📥 Input Layer
│   ├── Video
│   ├── Audio
│   └── Camera Stream
│
├── 🧹 Preprocessing
│   ├── Frame Extraction
│   ├── Face Detection
│   ├── Audio Extraction
│   └── Signal Normalization
│
├── 🧠 AI Detection
│   ├── Video Detection
│   ├── Audio Detection
│   └── Feature Analysis
│
├── 🔗 Fusion Engine
│   ├── Audio Evidence
│   ├── Video Evidence
│   └── Confidence
│
├── ⚠️ Risk Engine
│   ├── Risk Classification
│   ├── Evidence Generation
│   └── Alert Generation
│
└── 🖥️ Interface
    ├── Live Status
    ├── Risk Score
    ├── Evidence
    └── Verification Result
```

---

# 🧪 Testing Strategy

CallShield can be evaluated using multiple categories of media.

### 01 — Authentic

```text
Real Person
     │
     ▼
Original Video
     │
     ▼
CallShield
     │
     ▼
Expected → LOW MANIPULATION RISK
```

### 02 — Simulated Face Swap

```text
Reference Face
     │
     ▼
Deep-Live-Cam
     │
     ▼
Controlled Deepfake
     │
     ▼
CallShield
     │
     ▼
Expected → HIGHER MANIPULATION RISK
```

### 03 — Mixed Conditions

```text
Deepfake
   +
Low Light
   +
Compression
   +
Camera Noise
       │
       ▼
   CallShield
       │
       ▼
Robustness Evaluation
```

This helps evaluate whether the detector remains useful when real-world video quality is poor.

---

# 🔬 Evaluation

Important evaluation metrics include:

```text
                MODEL EVALUATION
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    Accuracy        Precision       Recall
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                  F1 Score
                       │
                       ▼
              False Positive Rate
                       │
                       ▼
              False Negative Rate
```

For a fraud-detection system, **false positives and false negatives should both be tracked**, rather than relying only on overall accuracy.

---

# 🛡️ Responsible AI

CallShield is designed around defensive use.

The deepfake generator is used only as a **controlled simulation component for testing and validating detection**.

```text
         ┌───────────────────────┐
         │ Controlled Simulation  │
         └───────────┬───────────┘
                     │
                     ▼
              Test Dataset
                     │
                     ▼
            Detection Research
                     │
                     ▼
             Model Evaluation
                     │
                     ▼
              Fraud Defense
```

We do not position the simulation component as a mechanism for impersonating real people or conducting deceptive activity.

Any testing involving real individuals should use appropriate consent and comply with applicable laws and institutional requirements.

---

# ⚠️ Important Note About Deep-Live-Cam

Deep-Live-Cam is **not the CallShield detection model**.

It is used as an external tool to create controlled face-manipulation samples for testing.

The roles are intentionally separated:

```text
┌──────────────────────┐
│    DEEP-LIVE-CAM     │
│                      │
│  Attack Simulation  │
└──────────┬───────────┘
           │
           │ simulated media
           ▼
┌──────────────────────┐
│     CALLSHIELD       │
│                      │
│ Detection + Analysis │
└──────────────────────┘
```

**Simulation ≠ Detection**

This separation allows us to evaluate whether CallShield can recognize manipulated content generated by an independent system.

---

# 🚀 Demonstration Flow

Our hackathon demonstration follows this sequence:

```text
        START
          │
          ▼
   ┌───────────────┐
   │ Authentic     │
   │ Media Sample  │
   └───────┬───────┘
           │
           ▼
      CallShield
           │
           ▼
      Verification
           │
           ▼
      Baseline Result
           │
           ▼
   ┌───────────────┐
   │ Controlled    │
   │ Deepfake      │
   │ Simulation    │
   └───────┬───────┘
           │
           ▼
      CallShield
           │
           ▼
   First-View Analysis
           │
           ▼
   Detection Signals
           │
           ▼
    Risk Assessment
           │
           ▼
      🚨 ALERT
```

---

# 🎯 Core Innovation

CallShield is not simply:

> **"Is this video fake?"**

The broader approach is:

```text
                MEDIA
                  │
                  ▼
          ┌───────────────┐
          │   ANALYZE    │
          └───────┬───────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
      AUDIO                VIDEO
        │                   │
        └─────────┬─────────┘
                  ▼
            CORRELATE
                  │
                  ▼
          EXTRACT EVIDENCE
                  │
                  ▼
           ASSESS RISK
                  │
                  ▼
          PROTECT THE USER
```

The goal is to transform deepfake detection from a hidden model prediction into an **explainable verification layer for suspicious communication**.

---

# 🧰 Technology Stack

```text
Frontend
   ├── React / Web UI
   └── Real-time visualization

Backend
   ├── Python
   ├── FastAPI
   └── REST / WebSocket APIs

AI / ML
   ├── Computer Vision
   ├── Deepfake Detection
   ├── Audio Analysis
   └── Multi-modal Fusion

Media
   ├── OpenCV
   ├── FFmpeg
   └── Video / Audio Processing

Simulation
   └── Deep-Live-Cam
       └── Controlled test generation
```

---

# 📁 Project Structure

```text
CallShield/
│
├── frontend/
│   ├── components/
│   ├── pages/
│   └── assets/
│
├── backend/
│   ├── api/
│   ├── models/
│   ├── detection/
│   ├── audio/
│   ├── video/
│   └── fusion/
│
├── simulation/
│   ├── samples/
│   └── README.md
│
├── datasets/
│   ├── authentic/
│   └── simulated/
│
├── models/
│   └── detection_models/
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# 🔄 End-to-End Pipeline

```text
             ┌─────────────────────┐
             │     CALL / MEDIA    │
             └──────────┬──────────┘
                        │
                        ▼
              ┌───────────────────┐
              │  MEDIA INGESTION  │
              └─────────┬─────────┘
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
        ┌───────────┐       ┌───────────┐
        │   AUDIO   │       │   VIDEO   │
        └─────┬─────┘       └─────┬─────┘
              │                   │
              ▼                   ▼
        ┌───────────┐       ┌───────────┐
        │ FEATURES  │       │ FEATURES  │
        └─────┬─────┘       └─────┬─────┘
              │                   │
              └─────────┬─────────┘
                        ▼
                 ┌──────────────┐
                 │ AI DETECTION │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ EVIDENCE     │
                 │ FUSION       │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ RISK ENGINE  │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ CALLSHIELD   │
                 │   RESULT     │
                 └──────────────┘
```

---

# 🏆 The One-Line Explanation

> **CallShield AI uses controlled deepfake simulations to challenge a multi-modal detection pipeline that analyzes audio and video evidence and provides an early risk assessment for suspicious calls.**

---

# ⚖️ Disclaimer

CallShield AI is a research and defensive-security project.

Deepfake generation tools referenced by the project are used solely for controlled testing, benchmarking, and validation of detection systems.

Users are responsible for ensuring that any media used during testing complies with applicable laws, consent requirements, intellectual-property rights, and ethical standards.

Detection results should be treated as **risk indicators rather than absolute proof of authenticity or fraud**.

---

# 👥 Team

**Team ElevateX**

Building technology for safer digital communication.

```text
       ┌─────────────────────────┐
       │       CALLSHIELD        │
       │                         │
       │   SIMULATE → DETECT     │
       │       → VERIFY          │
       │                         │
       └─────────────────────────┘
```

### 🛡️ CallShield AI

**Don't trust the face.
Don't trust the voice.
Verify the signal.**
