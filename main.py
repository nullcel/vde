import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class ReverseImageSearch:
    def __init__(self, samples_dir="samples", embedding_file="embeddings.pkl"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.resnet50(pretrained=True).to(self.device)
        self.model.eval()
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])
        self.samples_dir = samples_dir
        self.embedding_file = embedding_file
        self.embeddings = {}

        if os.path.exists(self.embedding_file):
            with open(self.embedding_file, "rb") as f:
                self.embeddings = pickle.load(f)

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def _get_embedding(self, image_path):
        image = Image.open(image_path).convert("RGB")
        image = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.model(image).squeeze().cpu().numpy()
        return embedding

    def add_image(self, image_path):
        embedding = self._get_embedding(image_path)
        self.embeddings[image_path] = embedding

    def add_samples(self):
        for filename in os.listdir(self.samples_dir):
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                image_path = os.path.join(self.samples_dir, filename)
                self.add_image(image_path)

    def save_embeddings(self):
        with open(self.embedding_file, "wb") as f:
            pickle.dump(self.embeddings, f)

    def search(self, query_image_path, top_k=5):
        query_embedding = self._get_embedding(query_image_path)
        scores = []
        for image_path, embedding in self.embeddings.items():
            score = cosine_similarity([query_embedding], [embedding])[0][0]
            scores.append((image_path, score))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        return scores[:top_k]

if __name__ == "__main__":
    ris = ReverseImageSearch()
    ris.add_samples()
    ris.save_embeddings()
    results = ris.search("subject.jpg")
    print("Top results:")
    for image_path, score in results:
        print(f"Image: {image_path}, Similarity: {score}")
