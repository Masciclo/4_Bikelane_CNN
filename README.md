# **Bikelane Classification Pipeline**  
*Automated Geospatial Sampling & CNN-based Bikelane Quality Assessment*  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![GeoSampler](https://img.shields.io/badge/Geo-Sampler-FF6F00)](https://github.com/Masciclo/Bikelane_CNN/blob/main/geom%20sampler%20console.ipynb)  
[![ResNet-18](https://img.shields.io/badge/PyTorch-ResNet18-CB3234)](https://github.com/Masciclo/Bikelane_CNN/blob/main/resnet_ciclo.ipynb)  

---
<img src="https://github.com/user-attachments/assets/e1ee251e-3a7f-4f0e-86cc-c0791544d3bc" alt="Image" width="800"/>

## **Project Overview**  
This repository contains a two-stage pipeline for analyzing bicycle lane infrastructure:  
1. **GeoSampler Console**: Geospatial preprocessing tool that aligns video frames (MP4) + GPS tracks (GPX) with cadastral bicycle lane geometries (GeoJSON).  
2. **ResNet-18 Classifier**: CNN model trained on sampled frames to classify bicycle lane conditions/types.  

---

## **1. GeoSampler Console**  
*(https://github.com/Masciclo/Bikelane_CNN/tree/main/Functions)*  

### **Key Features**  
- **Inputs**:  
  - `cadaster.geojson`: Vector layer with bicycle lane segments + metadata (ID, surface type, condition labels).  
  - `*.mp4` + `*.gpx`: Synchronized video recordings and GPS tracks from bicycle-mounted cameras.  
- **Process**:  
  1. Spatial filtering using buffer operations around target geometries.  
  2. Temporal alignment of GPS points with video frames.  
  3. Frame extraction + metadata logging into Pandas DataFrame.  

### **Workflow**  
```python  
# Sample Usage (from geom sampler console.ipynb)
from Functions.geo_processor import GeoFilter
from Functions.frame_extractor import VideoSampler

# 1. Filter GPX points within 5m of cadastral segments with 'surface=asphalt'
gf = GeoFilter(cadaster_path='data/cadaster.geojson', 
               buffer_dist=5, 
               attribute_filter={'surface': 'asphalt'})
gpx_points = gf.filter_gpx('data/session_2023.gpx')

# 2. Extract frames corresponding to filtered GPS timestamps
vs = VideoSampler(video_path='data/session_2023.mp4')
df = vs.sample_frames(gpx_points, output_dir='sampled_frames/')
```  

### **Parameters**  
| Component | Key Parameters | Description |  
|-----------|----------------|-------------|  
| `GeoFilter` | `buffer_dist=5` (meters), `attribute_filter` | Spatial query constraints |  
| `VideoSampler` | `frame_size=(640,480)`, `time_tolerance=0.5s` | Temporal alignment thresholds |  

### **Output Structure**  
```  
sampled_frames/  
├── frame_001.png  # Image with EXIF metadata (GPS time, geometry ID)  
├── frame_002.png  
└── metadata.csv   # Columns: [frame_path, bikelane_id, surface_type, condition_score]  
```  

---

## **2. ResNet-18 Classifier**  
*(https://github.com/Masciclo/Bikelane_CNN/blob/main/resnet_ciclo.ipynb)*  

### **Architecture**  
- **Model**: Modified ResNet-18 with:  
  - Input layer: Adjusted for 640x480 RGB frames  
  - Output layer: Custom heads for multi-task classification (surface type + condition)  
- **Training**:  
  ```python  
  from resnet_ciclo import BikelaneResNet
  model = BikelaneResNet(num_surface_classes=4,  # asphalt, concrete, gravel, mixed  
                         num_condition_levels=3) # good, fair, poor  
  model.cuda()
  ```  

### **Data Pipeline**  
```python  
from Functions.dataloader import BikelaneDataset
dataset = BikelaneDataset(metadata='sampled_frames/metadata.csv',
                          transform=...)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
```  

### **Training Parameters**  
| Hyperparameter | Value |  
|----------------|-------|  
| Optimizer | AdamW (lr=3e-4) |  
| Loss Function | CrossEntropy (surface) + OrdinalLoss (condition) |  
| Augmentation | RandomCrop, HorizontalFlip, ColorJitter |  

---

## **Repository Structure**  
```  
Bikelane_CNN/  
├── geom sampler console.ipynb       # GeoSampler interface  
├── resnet_ciclo.ipynb               # ResNet training/eval  
├── Functions/  
│   ├── geo_processor.py             # GeoJSON/GPX spatial ops  
│   ├── frame_extractor.py           # MP4 frame sampling  
│   └── dataloader.py                # Custom DataLoader  
├── sampled_frames/                  # Output directory  
└── models/                          # Pretrained weights (TODO)  
```  

## **License**  
MIT License - See [LICENSE](LICENSE) for details.
