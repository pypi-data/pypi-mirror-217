# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from aspose_ocr_cloud.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    V5_BINARIZE_IMAGE = "/BinarizeImage"
    V5_CONVERT_TEXT_TO_SPEECH = "/ConvertTextToSpeech"
    V5_DESKEW_IMAGE = "/DeskewImage"
    V5_DETECT_REGIONS = "/DetectRegions"
    V5_DEWARP_IMAGE = "/DewarpImage"
    V5_DJ_VU2PDF = "/DjVu2PDF"
    V5_IDENTIFY_FONT = "/IdentifyFont"
    V5_IMAGE_PROCESSING_POST_UPSAMPLING_IMAGE_FILE = "/ImageProcessing/PostUpsamplingImageFile"
    V5_IMAGE_PROCESSING_POST_BINARIZATION_FILE = "/ImageProcessing/PostBinarizationFile"
    V5_IMAGE_PROCESSING_POST_SKEW_CORRECTION_FILE = "/ImageProcessing/PostSkewCorrectionFile"
    V5_IMAGE_PROCESSING_POST_DEWARPING_FILE = "/ImageProcessing/PostDewarpingFile"
    V5_IMAGE_PROCESSING_GET_RESULT_TASK = "/ImageProcessing/GetResultTask"
    V5_IMAGE_PROCESSING_GET_RESULT_FILE = "/ImageProcessing/GetResultFile"
    V5_RECOGNIZE_IMAGE = "/RecognizeImage"
    V5_RECOGNIZE_LABEL = "/RecognizeLabel"
    V5_RECOGNIZE_PDF = "/RecognizePdf"
    V5_RECOGNIZE_RECEIPT = "/RecognizeReceipt"
    V5_RECOGNIZE_REGIONS = "/RecognizeRegions"
    V5_RECOGNIZE_TABLE = "/RecognizeTable"
    V5_TEXT_TO_SPEECH_POST_TEXT_TO_SPEECH = "/TextToSpeech/PostTextToSpeech"
    V5_TEXT_TO_SPEECH_GET_TEXT_TO_SPEECH_RESULT = "/TextToSpeech/GetTextToSpeechResult"
    V5_TEXT_TO_SPEECH_GET_TEXT_TO_SPEECH_RESULT_FILE = "/TextToSpeech/GetTextToSpeechResultFile"
    V5_UPSCALE_IMAGE = "/UpscaleImage"
