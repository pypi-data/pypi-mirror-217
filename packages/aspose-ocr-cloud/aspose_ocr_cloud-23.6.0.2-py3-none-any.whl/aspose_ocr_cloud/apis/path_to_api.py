import typing_extensions

from aspose_ocr_cloud.paths import PathValues
from aspose_ocr_cloud.apis.paths.v5_binarize_image import V5BinarizeImage
from aspose_ocr_cloud.apis.paths.v5_convert_text_to_speech import V5ConvertTextToSpeech
from aspose_ocr_cloud.apis.paths.v5_deskew_image import V5DeskewImage
from aspose_ocr_cloud.apis.paths.v5_detect_regions import V5DetectRegions
from aspose_ocr_cloud.apis.paths.v5_dewarp_image import V5DewarpImage
from aspose_ocr_cloud.apis.paths.v5_dj_vu2_pdf import V5DjVu2PDF
from aspose_ocr_cloud.apis.paths.v5_identify_font import V5IdentifyFont
from aspose_ocr_cloud.apis.paths.v5_image_processing_post_upsampling_image_file import V5ImageProcessingPostUpsamplingImageFile
from aspose_ocr_cloud.apis.paths.v5_image_processing_post_binarization_file import V5ImageProcessingPostBinarizationFile
from aspose_ocr_cloud.apis.paths.v5_image_processing_post_skew_correction_file import V5ImageProcessingPostSkewCorrectionFile
from aspose_ocr_cloud.apis.paths.v5_image_processing_post_dewarping_file import V5ImageProcessingPostDewarpingFile
from aspose_ocr_cloud.apis.paths.v5_image_processing_get_result_task import V5ImageProcessingGetResultTask
from aspose_ocr_cloud.apis.paths.v5_image_processing_get_result_file import V5ImageProcessingGetResultFile
from aspose_ocr_cloud.apis.paths.v5_recognize_image import V5RecognizeImage
from aspose_ocr_cloud.apis.paths.v5_recognize_label import V5RecognizeLabel
from aspose_ocr_cloud.apis.paths.v5_recognize_pdf import V5RecognizePdf
from aspose_ocr_cloud.apis.paths.v5_recognize_receipt import V5RecognizeReceipt
from aspose_ocr_cloud.apis.paths.v5_recognize_regions import V5RecognizeRegions
from aspose_ocr_cloud.apis.paths.v5_recognize_table import V5RecognizeTable
from aspose_ocr_cloud.apis.paths.v5_text_to_speech_post_text_to_speech import V5TextToSpeechPostTextToSpeech
from aspose_ocr_cloud.apis.paths.v5_text_to_speech_get_text_to_speech_result import V5TextToSpeechGetTextToSpeechResult
from aspose_ocr_cloud.apis.paths.v5_text_to_speech_get_text_to_speech_result_file import V5TextToSpeechGetTextToSpeechResultFile
from aspose_ocr_cloud.apis.paths.v5_upscale_image import V5UpscaleImage

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V5_BINARIZE_IMAGE: V5BinarizeImage,
        PathValues.V5_CONVERT_TEXT_TO_SPEECH: V5ConvertTextToSpeech,
        PathValues.V5_DESKEW_IMAGE: V5DeskewImage,
        PathValues.V5_DETECT_REGIONS: V5DetectRegions,
        PathValues.V5_DEWARP_IMAGE: V5DewarpImage,
        PathValues.V5_DJ_VU2PDF: V5DjVu2PDF,
        PathValues.V5_IDENTIFY_FONT: V5IdentifyFont,
        PathValues.V5_IMAGE_PROCESSING_POST_UPSAMPLING_IMAGE_FILE: V5ImageProcessingPostUpsamplingImageFile,
        PathValues.V5_IMAGE_PROCESSING_POST_BINARIZATION_FILE: V5ImageProcessingPostBinarizationFile,
        PathValues.V5_IMAGE_PROCESSING_POST_SKEW_CORRECTION_FILE: V5ImageProcessingPostSkewCorrectionFile,
        PathValues.V5_IMAGE_PROCESSING_POST_DEWARPING_FILE: V5ImageProcessingPostDewarpingFile,
        PathValues.V5_IMAGE_PROCESSING_GET_RESULT_TASK: V5ImageProcessingGetResultTask,
        PathValues.V5_IMAGE_PROCESSING_GET_RESULT_FILE: V5ImageProcessingGetResultFile,
        PathValues.V5_RECOGNIZE_IMAGE: V5RecognizeImage,
        PathValues.V5_RECOGNIZE_LABEL: V5RecognizeLabel,
        PathValues.V5_RECOGNIZE_PDF: V5RecognizePdf,
        PathValues.V5_RECOGNIZE_RECEIPT: V5RecognizeReceipt,
        PathValues.V5_RECOGNIZE_REGIONS: V5RecognizeRegions,
        PathValues.V5_RECOGNIZE_TABLE: V5RecognizeTable,
        PathValues.V5_TEXT_TO_SPEECH_POST_TEXT_TO_SPEECH: V5TextToSpeechPostTextToSpeech,
        PathValues.V5_TEXT_TO_SPEECH_GET_TEXT_TO_SPEECH_RESULT: V5TextToSpeechGetTextToSpeechResult,
        PathValues.V5_TEXT_TO_SPEECH_GET_TEXT_TO_SPEECH_RESULT_FILE: V5TextToSpeechGetTextToSpeechResultFile,
        PathValues.V5_UPSCALE_IMAGE: V5UpscaleImage,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V5_BINARIZE_IMAGE: V5BinarizeImage,
        PathValues.V5_CONVERT_TEXT_TO_SPEECH: V5ConvertTextToSpeech,
        PathValues.V5_DESKEW_IMAGE: V5DeskewImage,
        PathValues.V5_DETECT_REGIONS: V5DetectRegions,
        PathValues.V5_DEWARP_IMAGE: V5DewarpImage,
        PathValues.V5_DJ_VU2PDF: V5DjVu2PDF,
        PathValues.V5_IDENTIFY_FONT: V5IdentifyFont,
        PathValues.V5_IMAGE_PROCESSING_POST_UPSAMPLING_IMAGE_FILE: V5ImageProcessingPostUpsamplingImageFile,
        PathValues.V5_IMAGE_PROCESSING_POST_BINARIZATION_FILE: V5ImageProcessingPostBinarizationFile,
        PathValues.V5_IMAGE_PROCESSING_POST_SKEW_CORRECTION_FILE: V5ImageProcessingPostSkewCorrectionFile,
        PathValues.V5_IMAGE_PROCESSING_POST_DEWARPING_FILE: V5ImageProcessingPostDewarpingFile,
        PathValues.V5_IMAGE_PROCESSING_GET_RESULT_TASK: V5ImageProcessingGetResultTask,
        PathValues.V5_IMAGE_PROCESSING_GET_RESULT_FILE: V5ImageProcessingGetResultFile,
        PathValues.V5_RECOGNIZE_IMAGE: V5RecognizeImage,
        PathValues.V5_RECOGNIZE_LABEL: V5RecognizeLabel,
        PathValues.V5_RECOGNIZE_PDF: V5RecognizePdf,
        PathValues.V5_RECOGNIZE_RECEIPT: V5RecognizeReceipt,
        PathValues.V5_RECOGNIZE_REGIONS: V5RecognizeRegions,
        PathValues.V5_RECOGNIZE_TABLE: V5RecognizeTable,
        PathValues.V5_TEXT_TO_SPEECH_POST_TEXT_TO_SPEECH: V5TextToSpeechPostTextToSpeech,
        PathValues.V5_TEXT_TO_SPEECH_GET_TEXT_TO_SPEECH_RESULT: V5TextToSpeechGetTextToSpeechResult,
        PathValues.V5_TEXT_TO_SPEECH_GET_TEXT_TO_SPEECH_RESULT_FILE: V5TextToSpeechGetTextToSpeechResultFile,
        PathValues.V5_UPSCALE_IMAGE: V5UpscaleImage,
    }
)
