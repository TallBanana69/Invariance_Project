# Component Detection and Classification Repository

This repository contains scripts, notebooks, and models for detecting and classifying components in PCB images. It is designed to provide a complete pipeline, including augmentation, feature extraction, model training, and evaluation.

---

## Repository Structure

- **Golden_PCB_Change_Detection**  
  - Contains `gui.py` for detecting changes between a reference PCB image and an input PCB image.
- **yolo_model**  
  - YOLO model and related files for component detection.
- **CNN_Model.ipynb**  
  - Implements a Convolutional Neural Network (CNN) for component classification.
- **Feature_Extraction_Models.ipynb**  
  - Extracts image features and applies SVM, Random Forest, and ANN models for classification.
- **Image_Augmentation_Pipeline.ipynb**  
  - Handles data augmentation for image datasets.
- **Yolo_Component_Detector.ipynb**  
  - Trains YOLO for detecting PCB components.
- **Our_Dataset.zip**  
  - Zipped dataset for training and testing models.
- **features.csv**  
  - CSV containing extracted features for machine learning models.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TallBanana69/Invariance_Project
   cd Invariance_Project
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Modules

### Golden PCB Change Detection
Run the `gui.py` script inside the `Golden_PCB_Change_Detection` folder:

```bash
python gui.py
```

This GUI compares a reference PCB image to an input PCB image and highlights changes.

### YOLO Component Detector
The `Yolo_Component_Detector.ipynb` trains a YOLO model for PCB component detection. Configure the notebook to train, evaluate, and visualize component detection results.

### Image Augmentation Pipeline
Use the `Image_Augmentation_Pipeline.ipynb` to generate augmented images by applying:

- Flipping
- Rotation
- Cropping
- Color shifting

### Feature Extraction Models
The `Feature_Extraction_Models.ipynb` performs feature extraction for classification, such as:

- Color ratios
- Normalized RGB
- Correlation with dominant shapes
- Brightness and intensity statistics

It trains classifiers like:

- SVM
- Random Forest
- Artificial Neural Networks (ANN)

### CNN Model
The `CNN_Model.ipynb` contains a simple CNN model for image-based component classification. Use this notebook to directly classify components from images without additional feature extraction.

---

## Dependencies

All required libraries are listed in the `requirements.txt` file. Run the following command to install them:

```bash
pip install -r requirements.txt
