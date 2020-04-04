from src import autoencoder, CV_IO_utils, CV_plot_utils, CV_transform_utils, utils

def getModel(path):
    images = []
    for i in range(1525, 1600) :
        images.append('img/products/' + str(i) + '.jpg')
    return {'images':images}

def search_knn() :
    pass