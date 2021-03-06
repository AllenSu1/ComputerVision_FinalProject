# 評估&測試模型
import os
import cv2
import csv
import torch
import numpy
from pathlib import Path
from torchvision import datasets, models, transforms
import torch.nn as nn
import torchvision
import numpy as np
import matplotlib.pyplot as plt
from plotcm import plot_confusion_matrix
from sklearn.metrics import confusion_matrix
from PIL import Image
import model as res101_frezee
from tqdm import tqdm

device = torch.device("cuda")

# 設計超參數
batch_size = 16
num_workers = 0

model = torchvision.models.resnet101(pretrained=True, progress=True)
# model.load_state_dict(torch.load("model/resnet101.pth"))
# 提取參數fc的輸入參數
fc_features = model.fc.in_features
# 將最後輸出類別改為20
model.fc = nn.Linear(fc_features, 2)
# 輸入訓練好權重
model.load_state_dict(torch.load("model/val_loss0.501355.pth"))

# # 遷移學習 -> frezee
# for name, parameter in model.named_parameters():
#     # print(name)
#     if name == 'layer4.0.conv1.weight':
#         break
#     # if name == 'fc.weight':
#     #     break
#     parameter.requires_grad = False

model.to(device)

PATH_test = r"C:\Users\Allen\Desktop\1"
TEST = Path(PATH_test)

test_transforms = transforms.Compose([transforms.Resize((224, 224)),
                                      transforms.ToTensor(),
                                      transforms.Normalize([0.485, 0.456, 0.406],
                                                           [0.229, 0.224, 0.225])])
test_data = datasets.ImageFolder(TEST, transform=test_transforms)

test_loader = torch.utils.data.DataLoader(
    test_data, batch_size=batch_size,  num_workers=num_workers)
test_data_iter = iter(test_loader)
test_image, test_label = test_data_iter.next()

criterion = nn.CrossEntropyLoss()
criterion = criterion.to(device)

# monitor test loss and accuracy
test_loss = 0.
correct = 0.
total = 0.
# pred_cm = torch.empty(125, 8)
model.eval()

pred_cm = torch.tensor([]).to(device)
for (data, target) in tqdm((test_loader)):
    # move to GPU
    data, target = data.to(device), target.to(device)
    # forward pass: compute predicted outputs by passing inputs to the model
    output = model(data)
    # calculate the loss
    loss = criterion(output, target)
    # convert output probabilities to predicted class
    pred = output.data.max(1, keepdim=True)[1]
    pred_cm = torch.cat((pred_cm, pred), dim=0)
    # compare predictions to true label
    correct += np.sum(np.squeeze(pred.eq(target.data.view_as(pred))).cpu().numpy())
    total += data.size(0)

print('Test Accuracy: ', (correct / total))

cm = confusion_matrix(torch.tensor(test_data.targets), pred_cm.cpu())
print(type(cm))

classes = os.listdir(r'D:\Dataset\computer_vision\project2\train')

# 繪製混淆矩陣
plt.figure(figsize=(2, 2))
plot_confusion_matrix(cm, classes, normalize=False,
                      title='Confusion matrix', cmap=plt.cm.Blues)
