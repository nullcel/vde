import os
import pickle
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# config
SAMPLES_DIR = "samples"
EMBEDDING_FILE = "embeddings.pkl"
IMAGE_SIZE = (224, 224)
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]
TOP_K = 5

class ReverseImageSearch:
    def __init__(self, samples_dir=SAMPLES_DIR, embedding_file=EMBEDDING_FILE):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._initialize_model()
        self.samples_dir = samples_dir
        self.embedding_file = embedding_file
        self.embeddings = self._load_embeddings()
        self.transform = self._get_transform()

    def _initialize_model(self):
        """Initialize and prepare the ResNet model for feature extraction."""
        model = models.resnet50(pretrained=True).to(self.device)
        model.eval()
        return torch.nn.Sequential(*list(model.children())[:-1])

    def _load_embeddings(self):
        """Load saved embeddings from a file if available."""
        if os.path.exists(self.embedding_file):
            with open(self.embedding_file, "rb") as f:
                return pickle.load(f)
        return {}

    def _get_transform(self):
        """Define the transformation pipeline for input images."""
        return transforms.Compose([
            transforms.Resize(IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(mean=MEAN, std=STD),
        ])

    def _get_embedding(self, image_path):
        """Generate the feature embedding for a single image."""
        image = Image.open(image_path).convert("RGB")
        image = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.model(image).squeeze().cpu().numpy()
        return embedding

    def add_image(self, image_path):
        """Add an image and its embedding to the collection."""
        embedding = self._get_embedding(image_path)
        self.embeddings[image_path] = embedding

    def add_samples(self):
        """Load and process all images from the samples directory."""
        print(f"[Debug] Looking for images in: {self.samples_dir}")
        if not os.path.exists(self.samples_dir):
            print(f"[Warning] Samples directory '{self.samples_dir}' does not exist. Creating it.")
            os.makedirs(self.samples_dir)
            return

        added = False
        for filename in os.listdir(self.samples_dir):
            if filename.lower().endswith((".jpg", ".jpeg")):
                image_path = os.path.join(self.samples_dir, filename)
                print(f"[Debug] Adding image: {image_path}")
                self.add_image(image_path)
                added = True

        if not added:
            print(f"[Warning] No images found in the samples directory: {self.samples_dir}")

    def save_embeddings(self):
        """Save the current embeddings to a file."""
        with open(self.embedding_file, "wb") as f:
            pickle.dump(self.embeddings, f)

    def search(self, query_image_path, top_k=TOP_K):
        """Search for the top-k most similar images to the query image."""
        print(f"[Debug] Query image: {query_image_path}")
        if not os.path.exists(query_image_path):
            print(f"[Error] Query image '{query_image_path}' not found.")
            return []

        query_embedding = self._get_embedding(query_image_path)
        print(f"[Debug] Query embedding: {query_embedding[:10]}")  # Display a preview of the query embedding

        scores = [
            (image_path, cosine_similarity([query_embedding], [embedding])[0][0])
            for image_path, embedding in self.embeddings.items()
        ]

        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        print(f"[Debug] Top {top_k} results: {scores[:top_k]}")  # Display the top-k results
        return scores[:top_k]

if __name__ == "__main__":
    ris = ReverseImageSearch()
    ris.add_samples()
    ris.save_embeddings()

    query_image = "subject.jpg"
    results = ris.search(query_image)
    print("Top results:")
    for image_path, score in results:
        print(f"Image: {image_path}, Similarity: {score}")
