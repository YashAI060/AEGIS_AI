# 🛡️ AEGIS - Setup & Usage Guide

Welcome to the AEGIS project! Please follow these steps strictly to set up the Face ID system and run the assistant on your local machine.

## 🚀 How to Run (Step-by-Step)

Follow these instructions in the exact order to initialize the project:

### Step 1: Generate Face Data
First, we need to collect your biometric data (images) for the Face ID system.

1. Navigate to the **`sample`** folder.
2. Run the **`generate_dataset.py`** script:
   ```bash
   cd sample
   python generate_dataset.py
3. The camera will open. The script will automatically capture 100 images of your face. Please stay stable in front of the camera until the process is complete.

⚠️ Step 2: Critical Cleanup (Important!)
Do not skip this step.

Once the dataset is generated, you must move the **`generate_dataset.py`** file out of the **`sample`** folder.

Cut and paste the file into the main root directory (or anywhere outside sample).

Why? The sample folder must contain only image files for the training script to work correctly.

Step 3: Train the Model
Now, we need to train the recognition model using the collected data.

Navigate back to the main project folder.

Run the **`train_model.py`** script:

Bash
python train_model.py
This will process the images and generate the necessary model file (e.g., trainer.yml) for face recognition.

Step 4: Launch `AEGIS`
Once the setup is complete, you can launch the assistant.

Run the **`interface.py`** file:

Bash
python interface.py
AEGIS is now live! The system will verify your face and you can start using voice commands and automation features.