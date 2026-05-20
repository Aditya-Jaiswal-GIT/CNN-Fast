import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms,models
from torch.utils.data import DataLoader
from PIL import Image
from pathlib import Path
device = ('cuda' if torch.cuda.is_available() else 'cpu')
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
class Lung(nn.Module):
    def __init__(self):
        super(Lung,self).__init__()
        self.model = models.resnet18(weights='ResNet18_Weights.DEFAULT')
        self.model.fc = nn.Linear(self.model.fc.in_features,4)
    def forward(self,x):
        return self.model(x)
model = Lung().to(device)

_MODEL_PATH = Path(__file__).resolve().parent / 'lung.pt'
model.load_state_dict(torch.load(_MODEL_PATH, map_location=device))

def prediction(img : Image.Image):
    model.eval()

    img = img.convert('RGB')
    img = transform(img).unsqueeze(0).to(device)


    output = model(img)

    _, pred = torch.max(output, 1)

    classes = ['Corona','Normal','Pneumonia','Tuberculosis']
    return {
        'label': classes[pred.item()]  
    }
