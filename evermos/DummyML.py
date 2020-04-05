import os
import tensorflow as tf
import numpy as np
from src.CV_IO_utils import read_img
from src.CV_transform_utils import apply_transformer
from src.CV_transform_utils import resize_img, normalize_img
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def getModel(path):
    images = []
    for i in range(1525, 1600) :
        images.append('img/products/' + str(i) + '.jpg')
    return {'images':images}

class ImageTransformer(object):

    def __init__(self, shape_resize):
        self.shape_resize = shape_resize

    def __call__(self, img):
        img_transformed = resize_img(img, self.shape_resize)
        img_transformed = normalize_img(img_transformed)
        return img_transformed

class MachineLearning() :

    isReady = False
    knn = None
    imgs_train_name = None
    shape_img_resize = None
    input_shape_model = None
    output_shape_model = None
    model = None

    def __init__(self):
        self.get_ready()

    def get_ready(self) :
        print("Pickling knn..")
        with open(os.path.join(BASE_DIR, 'saved_model', 'knn.pkl'), 'rb') as temp :
            self.knn = pickle.load(temp)
        print("Pickling imgs_train_name..")
        with open(os.path.join(BASE_DIR, 'saved_model', 'imgs_train_name.pkl'), 'rb') as temp :
            self.imgs_train_name = pickle.load(temp)
        print("Pickling shape_img_resize..")
        with open(os.path.join(BASE_DIR, 'saved_model', 'shape_img_resize.pkl'), 'rb') as temp :
            self.shape_img_resize = pickle.load(temp)
        print("Pickling input_shape_model..")
        with open(os.path.join(BASE_DIR, 'saved_model', 'input_shape_model.pkl'), 'rb') as temp :
            self.input_shape_model = pickle.load(temp)
        print("Pickling output_shape_model..")
        with open(os.path.join(BASE_DIR, 'saved_model', 'output_shape_model.pkl'), 'rb') as temp :
            self.output_shape_model = pickle.load(temp)
        print("Loading model..")
        self.model = tf.keras.models.load_model(os.path.join(BASE_DIR, 'saved_model', 'model'))
        self.isReady = True

    def doit(self, path) :

        extensions = [".jpg", ".jpeg"]
        transformer = ImageTransformer(self.shape_img_resize)
        parallel = True

        imgs_test = [read_img(os.path.join(BASE_DIR, path[1:]))]
        imgs_test_transformed = apply_transformer(imgs_test, transformer, parallel=parallel)
        X_test = np.array(imgs_test_transformed).reshape((-1,) + self.input_shape_model)
        E_test = self.model.predict(X_test)
        E_test_flatten = E_test.reshape((-1, np.prod(self.output_shape_model)))

        print("Performing image retrieval on test images...")
        for i, emb_flatten in enumerate(E_test_flatten):
            _, indices = self.knn.kneighbors([emb_flatten])
            res = [idx for idx in indices.flatten()]
            imgs_retrieval_name = [self.imgs_train_name[idx].replace('img', 'img/products') for idx in res]
            return {'images':imgs_retrieval_name}
