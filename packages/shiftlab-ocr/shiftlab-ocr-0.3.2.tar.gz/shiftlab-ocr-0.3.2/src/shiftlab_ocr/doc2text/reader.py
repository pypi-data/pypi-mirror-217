import os
import urllib

from PIL import Image

from shiftlab_ocr.doc2text.crop import Crop
from shiftlab_ocr.doc2text.recognition import Recognizer
from shiftlab_ocr.doc2text.segmentation import Detector


class Reader:
    def __init__(
            self,
            yolo_path=os.path.join(os.path.dirname(__file__), "yolov5"),
            detector_weights=None,
            recognizer_weights=None,
    ):

        if recognizer_weights is None:
            if not os.path.exists(os.path.join(os.path.dirname(__file__), 'ocr_transformer_4h2l_simple_conv_64x256.pt')):
                urllib.request.urlretrieve(
                    "https://github.com/konverner/shiftlab_ocr/raw/main/doc2text/weights/ocr_transformer_4h2l_simple_conv_64x256.pt",
                    os.path.join(os.path.dirname(__file__), 'ocr_transformer_4h2l_simple_conv_64x256.pt'))
            recognizer_weights = os.path.join(os.path.dirname(__file__), 'ocr_transformer_4h2l_simple_conv_64x256.pt')

        if detector_weights is None:
            if not os.path.exists(os.path.join(os.path.dirname(__file__), 'yolo5_weights.pt')):
                urllib.request.urlretrieve(
                    "https://github.com/konverner/shiftlab_ocr/raw/main/doc2text/weights/weights.pt",
                    os.path.join(os.path.dirname(__file__), 'yolo5_weights.pt'))
            detector_weights = os.path.join(os.path.dirname(__file__), 'yolo5_weights.pt')

        self.recognizer = Recognizer()
        self.recognizer.load_model(recognizer_weights)
        self.detector = Detector(yolo_path, detector_weights)

    def doc2text(self, image_path):
        """
      params
      ---
      image_path : str
      path to .png or .jpg file with image to read

      returns
      ---
      text : str
      crops : list of PIL.image objects
      crops are sorted
      """
        text = ''
        image = Image.open(image_path)
        boxes = self.detector.run(image_path)
        crops = []
        for box in boxes:
            cropped = image.crop((box[0], box[1],
                                  box[2], box[3]))

            crops.append(Crop([[box[0], box[1]], [box[2], box[3]]], img=cropped))
        crops = sorted(crops)
        for crop in crops:
            text += self.recognizer.run(crop.img) + ' '

        return text, crops
