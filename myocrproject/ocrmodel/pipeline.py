import os, glob
import subprocess

from .config.config import ROOT_DIR


def process(folder_path, save_dir):
      for file_path in glob.glob(folder_path):
            print(f"Processing Document: {file_path}")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$save result")
            command = ['python', os.path.join(ROOT_DIR, "OCR", "tools", "infer", "predict_system.py"), '--use_onnx=True', 
                        f'--det_model_dir={os.path.join(ROOT_DIR, "models", "det_onnx")}', 
                        f'--rec_model_dir={os.path.join(ROOT_DIR, "models", "rec_onnx")}', 
                        f'--cls_model_dir={os.path.join(ROOT_DIR, "models", "cls_onnx")}', 
                        f'--image_dir={file_path}', f'--draw_img_save_dir={save_dir}',
                        f'--rec_char_dict_path={os.path.join(ROOT_DIR, "misc", "en_dict.txt")}', 
                        f'--vis_font_path={os.path.join(ROOT_DIR, "misc", "arial.ttf")}']

            result = subprocess.call(command)
