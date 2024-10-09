import torch
import torch.backends.cudnn as cudnn
from torchvision import datasets, transforms
import os

def init():
    global device, model_ft
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model_ft = torch.load('cat-detector/pittin-classifier')
    model_ft = model_ft.to(device)


cudnn.benchmark = True

def isPittin() -> bool:

    data_transforms = {
        'test': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    }

    data_dir = 'cat-detector/data/cats-photos'
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                            data_transforms[x])
                    for x in ['test']}

    test_dataloader = {'test': torch.utils.data.DataLoader(image_datasets['test'], batch_size=1, shuffle=False, num_workers=1)}

    
    #device = torch.device('cpu')

    def test_image(model) -> bool:
        was_training = model.training
        model.eval()

        with torch.no_grad():
            for (inputs, labels) in test_dataloader['test']: # name folder with test image as 'test'
                inputs = inputs.to(device)
                labels = labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)

                return bool(preds[0])
                
            model.train(mode=was_training)

    

    return test_image(model_ft)

if __name__ == '__main__':
    print(isPittin())