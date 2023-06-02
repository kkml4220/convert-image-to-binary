import os
import sys

from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR_NAME = "output"
# 出力ファイル名のprefix
OUTPUT_FILE_PREFIX = "bin-mapping"


def normalize_path(path):
    """パスを正規化する
    Unix系のOSでは"/"を使うがWindowsでは"\\"を使うため,
    これを"/"に正規化する
    """
    return os.path.normpath(path.replace('/', '\\'))


def is_absolute_path(path):
    """パスが絶対パスか判定"""
    return os.path.isabs(path)


def get_inputfile_abs_path(path):
    """入力ファイルのパスの絶対パスを取得
    Returns (str): 入力ファイルの絶対パスを返す
    """

    # 入力が絶対パスかどうか判定
    if not is_absolute_path(path):
        absolute_path = os.path.abspath(path)
    else:
        absolute_path = path

    if not os.path.exists(absolute_path):
        raise FileNotFoundError(f"{absolute_path} が見つかりません")

    return absolute_path


def get_output_dir_path():
    """出力先ディレクトリの絶対パス
        Return (str): 出力先のディレクトリの絶対パスを取得します
    """
    output_dir_path = os.path.join(BASE_DIR, OUTPUT_DIR_NAME)

    # ouputディレクトリが存在しない場合
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
        print(f"{output_dir_path}ディレクトリを作成しました")
        return output_dir_path

    return output_dir_path


def get_file_basename_without_extention(file_path):
    """ファイルのパスから拡張子なしのファイル名を取得
    Args:
        file_path (str): ファイルの絶対パスまたは相対パス
    Returns (str) : ファイルパスから拡張子なしのファイル名を取得します
    """
    basename = os.path.basename(file_path)
    file_name_without_extention = os.path.splitext(basename)[0]
    return file_name_without_extention


def decorator_print_arguments_and_result(original_function):
    """引数と結果を描画するデコレータ"""
    def wrapper_function(*args, **kwargs):
        # 引数の表示
        print("=" * 60)
        print(f"引数: {args}, {kwargs}")
        # 関数の実行
        result = original_function(*args, **kwargs)
        # 結果の表示
        print(f"結果: {result}")
        print("=" * 60)

        return result
    return wrapper_function


@decorator_print_arguments_and_result
def convert_image_to_binary(image_path):
    image = Image.open(image_path)
    filename_without_ext = get_file_basename_without_extention(image_path)
    # 出力ファイル名を定義
    filename = f"{OUTPUT_FILE_PREFIX}_{filename_without_ext}.txt"
    output_dir_path = get_output_dir_path()

    output_file_path = os.path.join(output_dir_path, filename)
    width, height = image.size

    with open(output_file_path, 'w') as file:
        # 画像のピクセル数を縦 横の順番で書き出す
        file.write(f"{height} {width}\n")
        # 画像のmappingをファイルに書き出す
        for y in range(height):
            for x in range(width):
                pixel = image.getpixel((x, y))
                if pixel == 255:  # 白
                    file.write('1')
                else:  # 黒
                    file.write('0')
            file.write('\n')

    return output_file_path


class ValidationError(Exception):
    """バリデーションエラー"""

    def __init__(self, message="バリデーションエラーです"):
        self.message = message
        super().__init__(self.message)


def validation_check(input_file_path):
    """入力時のバリデーションチェック"""

    # 入力引数の絶対パスを取得
    inputfile_abs_path = get_inputfile_abs_path(
        normalize_path(input_file_path))

    # ファイルが存在するか確認
    if not os.path.exists(inputfile_abs_path):
        raise ValidationError(f"{inputfile_abs_path}が見つかりません")

    return True


def main():
    args = sys.argv
    if len(args) != 2:
        raise ValidationError("コマンドライン引数が無効です")

    # 引数の受け取り
    input_file_path = args[1]

    # バリデーションチェック
    if validation_check(input_file_path):
        convert_image_to_binary(input_file_path)


if __name__ == "__main__":
    main()
