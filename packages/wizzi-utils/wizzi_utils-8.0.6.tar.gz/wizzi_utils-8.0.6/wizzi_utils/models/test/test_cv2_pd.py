from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.misc.test import test_misc_tools as mtt
from wizzi_utils.open_cv.test import test_open_cv_tools as cvtt
from wizzi_utils.models.models_configs import MODELS_CONFIG
from wizzi_utils.models.models_configs import ModelType
from wizzi_utils.models.cv2_models import pose_detection as pd
from wizzi_utils.models.test.shared_code_for_tests import CAM_FRAMES, IMAGE_MS, VID_X_FRAMES_CV
from wizzi_utils.models.test.shared_code_for_tests import PD_OP, PD_IM_TEST, PD_CAM_TEST, PD_VID_TEST
from wizzi_utils.models.test.shared_code_for_tests import od_or_pd_Model_image_test
from wizzi_utils.models.test.shared_code_for_tests import od_or_pd_Model_video_test
from wizzi_utils.models.test.shared_code_for_tests import od_or_pd_Model_cam_test


def __get_pd_dict(op: int = 1):
    if op == 1:
        pd_solo = {
            # 'model_names': ['openpose_pose_mpi'],
            # 'model_names': ['openpose_pose_coco'],
            'model_names': ['openpose_pose_coco_multi'],
            # 'model_names': ['body25'],
            # 'model_names': ['hand_pose'],
            'dis_size': (640, 480),
            'grid': (1, 1),
        }
        pd_meta_dict = pd_solo
    elif op == 2:
        pd_dual = {
            'model_names': [
                'openpose_pose_mpi',
                # 'openpose_pose_coco'
                # 'openpose_pose_coco_multi'
                # 'model_names': ['body25'],
                'body25'
            ],
            'dis_size': (640 * 2, 480),
            'grid': (1, 2),
        }
        pd_meta_dict = pd_dual
    elif op == 3:
        all_models_names = pd.PdBaseModel.get_pose_detection_models(m_type='Cv2', ack=False)
        # remove hand pose - not the same work
        all_models_names.remove('hand_pose')
        pd_all_models = {
            'model_names': all_models_names,
            'dis_size': 'fs',
            'grid': (2, 2),  # we have 4 cv2 pd models
        }
        pd_meta_dict = pd_all_models
    else:
        pd_meta_dict = None
    return pd_meta_dict


def _get_models(model_names: list) -> list:
    models = []
    for model_name in model_names:
        model_cfg = MODELS_CONFIG[model_name]
        m_save_dir = '{}/{}/{}'.format(mtt.MODELS, MODELS_CONFIG[model_name]['job'], model_name)
        if model_cfg['model_type'] == ModelType.PdCvNormal.value:
            model = pd.Cv2PdModel(
                save_load_dir=m_save_dir,
                model_name=model_name,
                device='gpu'
            )
        elif model_cfg['model_type'] == ModelType.PdCvCocoMulti.value:
            model = pd.Cv2PdModelCocoMultiPoses(
                save_load_dir=m_save_dir,
                model_name=model_name,
                allowed_joint_names=[
                    "Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist",
                    "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle"
                ],
                device='gpu',
                min_p_valid_joints=0.3
            )
        else:
            model = None
            mt.exception_error('model type not found')
            exit(-1)
        print(model.to_string(tabs=1))
        models.append(model)
    return models


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))
    pd_meta_dict = __get_pd_dict(op=PD_OP)
    models = _get_models(pd_meta_dict['model_names'])
    # POSE DETECTION TESTS
    if PD_IM_TEST:
        # cv_img = cvtt.load_img_from_web(mtt.FACES, ack=False)
        # cv_img = cvtt.load_img_from_web(mtt.HAND, ack=False)  # if testing 'hand_pose', use HAND image
        cv_img = cvtt.load_img_from_web(mtt.F_MODEL, ack=False)
        # cv_img = cvt.load_img(path='{}/Input2/77.jpg'.format(mtt.IMAGES_PATH))
        # cv_img = cvt.load_img(path='{}/Input2/cam1_0.jpg'.format(mtt.IMAGES_PATH))
        # cv_img = cvt.load_img(path='{}/Input2/90.jpg'.format(mtt.IMAGES_PATH))
        od_or_pd_Model_image_test(
            cv_img=cv_img,
            models=models,
            ms=IMAGE_MS,
            dis_size=pd_meta_dict['dis_size'],
            grid=pd_meta_dict['grid'],
        )
    if PD_CAM_TEST:
        od_or_pd_Model_cam_test(
            models=models,
            max_frames=CAM_FRAMES,
            dis_size=pd_meta_dict['dis_size'],
            grid=pd_meta_dict['grid'],
        )
    if PD_VID_TEST:
        vid_path = cvtt.get_vid_from_web(name=mtt.WOMAN_YOGA)
        od_or_pd_Model_video_test(
            models=models,
            vid_path=vid_path,
            work_every_x_frames=VID_X_FRAMES_CV,
            dis_size=pd_meta_dict['dis_size'],
            grid=pd_meta_dict['grid'],
        )
    print('{}'.format('-' * 20))
    return
