import argparse
import time

import cv2

from preprocessing import extract_parts, draw

from config_reader import config_reader
from cmu_model import get_testing_model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, help='input image')
    parser.add_argument('--output', type=str, default='result.png', help='output image')
    parser.add_argument('--model', type=str, default='../../large_file/model.h5', help='path to the weights file')

    args = parser.parse_args()
    image_path = args.image
    output = args.output
    keras_weights_file = args.model

    tic = time.time()
    print('start processing...')

    # load model

    # authors of original model don't use
    # vgg normalization (subtracting mean) on input images
    model = get_testing_model()
    model.load_weights(keras_weights_file)

    # load config
    params, model_params = config_reader()
    
    input_image = cv2.imread("./data/full_pose.jpg")  # B,G,R order

    all_peaks, subset, candidate = extract_parts(input_image, params, model, model_params)
    canvas = draw(input_image, all_peaks, subset, candidate)
    
    toc = time.time()
    print('processing time is %.5f' % (toc - tic))

    cv2.imwrite("./data/full_pose_v1.jpg", canvas)

    cv2.destroyAllWindows()
