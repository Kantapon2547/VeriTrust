# VeriTrust

 This project proposes VeriTrust AI, a browser-based system designed to screen online images for AI-generated content. The system focuses on still images commonly found on social media platforms and web pages encountered during normal browsing.

## Overview

VeriTrust is a hybrid deep learning project designed to detect AI-generated images by combining:

- CNN-based visual feature extraction
- Hand-crafted forensic features
- Dual-branch neural architecture
- Statistical image analysis

The project explores whether engineered forensic signals can improve AI-image detection performance compared to pure end-to-end CNN approaches.

---

## Features

### Deep Learning Branch
- Transfer learning with pretrained CNN backbone
- Image classification pipeline using PyTorch
- Data augmentation and normalization

### Forensic Feature Branch
Extracted handcrafted features include:

- FFT energy ratio
- Laplacian variance
- LBP entropy
- Residual entropy
- Edge density
- Noise statistics
- Frequency-domain artifacts

### Hybrid Architecture
- CNN image embeddings
- Dense feature vector fusion
- Final binary classification:
  - Real Image
  - AI-Generated Image

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/VeriTrust.git
cd VeriTrust
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run VeriTrust API

Run the FastAPI server from the project root folder:

```bash
python -m uvicorn api:app --reload
```

If successful, open:
```bash
http://127.0.0.1:8000
```

Expected response:
```bash
{"message":"VeriTrust API is running"}
```

API documentation:
```bash
http://127.0.0.1:8000/docs
```

### Load Chrome Extension

1. Open Chrome
2. Go to chrome extensions
3. Enable Developer Mode
4. Click Load unpacked
5. Select veritrust-extension/

The extension should now run locally with the VeriTrust API.

---

## Training

Run training notebook:

```bash
jupyter notebook
```

Or execute training script:

```bash
python src/training/train.py
```

---

## Dataset

Recommended datasets:

- CIFAKE
- Diffusion-generated image datasets
- GAN-generated image datasets

Place datasets inside:

```txt
data/raw/
```

---

## Example Pipeline

1. Load image
2. Preprocess image
3. Extract forensic features
4. Generate CNN embeddings
5. Fuse features
6. Predict authenticity

---

## Technologies Used

- Python
- PyTorch
- OpenCV
- NumPy
- Scikit-learn
- Jupyter Notebook

---

## Git Best Practices

Ignored files include:

```gitignore
.ipynb_checkpoints/
__pycache__/
venv/
outputs/
data/
```

Optional notebook cleanup:

```bash
pip install nbstripout
nbstripout --install
```

---

## Results

| Model | Accuracy |
|---|---|
| CNN Only | Baseline |
| Hybrid CNN + Features | Improved |

The hybrid architecture demonstrated improved classification performance compared to feature-parallel baselines.

---

## Future Improvements

- Vision Transformer integration
- Explainable AI visualization
- Real-time inference API
- Web deployment with Django/React
- Expanded forensic feature extraction

---
