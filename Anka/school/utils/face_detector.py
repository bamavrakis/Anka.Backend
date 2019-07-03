
import mxnet as mx
from .core.symbol import P_Net, R_Net, O_Net
from .core.detector import Detector
from .core.fcn_detector import FcnDetector
from .tools.load_model import load_param
from .core.MtcnnDetector import MtcnnDetector


class FaceDetector:
    def __init__(self, prefix=['model/pnet', 'model/rnet', 'model/onet'],
                 epoch=[16, 16, 16], batch_size=[2048, 256, 16],
                 ctx=mx.cpu(0),
                 thresh=[0.6, 0.6, 0.7], min_face_size=24,
                 stride=2):

        args, auxs = load_param(prefix[0], epoch[0], convert=True, ctx=ctx)
        PNet = FcnDetector(P_Net("test"), ctx, args, auxs)

        # load rnet model
        args, auxs = load_param(prefix[1], epoch[0], convert=True, ctx=ctx)
        RNet = Detector(R_Net("test"), 24, batch_size[1], ctx, args, auxs)

        # load onet model
        args, auxs = load_param(prefix[2], epoch[2], convert=True, ctx=ctx)
        ONet = Detector(O_Net("test"), 48, batch_size[2], ctx, args, auxs)

        self.mtcnn = MtcnnDetector(detectors=[PNet, RNet, ONet],
                                   ctx=ctx,
                                   min_face_size=min_face_size,
                                   stride=stride, threshold=thresh,
                                   slide_window=False)

    def find_faces(self, img):
        _, boxes_c = self.mtcnn.detect_pnet(img)
        _, boxes_c = self.mtcnn.detect_rnet(img, boxes_c)
        _, boxes_c = self.mtcnn.detect_onet(img, boxes_c)
        return boxes_c
