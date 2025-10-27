import os
import shutil
import random
import glob

source_dataset_path = r"C:\Users\BALAMURALI KRISHNA A\OneDrive\Documents\archive"

train_benign_path = r"breastcancerdataset\train\benign"
train_malignant_path = r"breastcancerdataset\train\malignant"
test_benign_path = r"breastcancerdataset\test\benign"
test_malignant_path = r"breastcancerdataset\test\malignant"

for path in [train_benign_path, train_malignant_path, test_benign_path, test_malignant_path]:
    os.makedirs(path, exist_ok=True)

patient_folders = [f for f in os.listdir(source_dataset_path) 
                   if os.path.isdir(os.path.join(source_dataset_path, f))]

benign_images = []
malignant_images = []

for patient_folder in patient_folders:
    patient_path = os.path.join(source_dataset_path, patient_folder)
    
    benign_folder = os.path.join(patient_path, "0")
    if os.path.exists(benign_folder):
        benign_files = glob.glob(os.path.join(benign_folder, "*.jpg")) + \
                       glob.glob(os.path.join(benign_folder, "*.png")) + \
                       glob.glob(os.path.join(benign_folder, "*.jpeg"))
        benign_images.extend(benign_files)
    
    malignant_folder = os.path.join(patient_path, "1")
    if os.path.exists(malignant_folder):
        malignant_files = glob.glob(os.path.join(malignant_folder, "*.jpg")) + \
                          glob.glob(os.path.join(malignant_folder, "*.png")) + \
                          glob.glob(os.path.join(malignant_folder, "*.jpeg"))
        malignant_images.extend(malignant_files)

print(f"Found {len(benign_images)} benign images and {len(malignant_images)} malignant images")

def split_and_copy_files(image_files, train_dir, test_dir, train_ratio=0.8):
    random.shuffle(image_files)
    split_idx = int(len(image_files) * train_ratio)
    
    # Split into train and test sets
    train_files = image_files[:split_idx]
    test_files = image_files[split_idx:]
    
    # Copy files to train directory
    for i, file in enumerate(train_files):
        filename = f"{i+1:05d}_{os.path.basename(file)}"  
        destination = os.path.join(train_dir, filename)
        shutil.copy2(file, destination)
    
    # Copy files to test directory
    for i, file in enumerate(test_files):
        filename = f"{i+1:05d}_{os.path.basename(file)}"  
        destination = os.path.join(test_dir, filename)
        shutil.copy2(file, destination)
    
    print(f"Copied {len(train_files)} files to {train_dir}")
    print(f"Copied {len(test_files)} files to {test_dir}")
    return len(train_files), len(test_files)

# Split and copy benign images
print("Organizing benign images...")
train_benign_count, test_benign_count = split_and_copy_files(benign_images, train_benign_path, test_benign_path)

# Split and copy malignant images
print("Organizing malignant images...")
train_malignant_count, test_malignant_count = split_and_copy_files(malignant_images, train_malignant_path, test_malignant_path)

print("\nDataset organization complete!")
print(f"Train set: {train_benign_count} benign, {train_malignant_count} malignant")
print(f"Test set: {test_benign_count} benign, {test_malignant_count} malignant")