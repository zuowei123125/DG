import os
import threading

def clear_folder_contents(folder_paths):
    def clear_folder(folder_path):
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        clear_folder(file_path)
                        os.rmdir(file_path)
                except Exception as e:
                    print(f"无法删除 {file_path}: {e}")
        except Exception as e:
            print(f"无法列出文件夹内容 {folder_path}: {e}")

    for folder_path in folder_paths:
        thread = threading.Thread(target=clear_folder, args=(folder_path,))
        thread.start()

def another_function():
    folder1_to_clear = "D:\PSMarktemp"
    #folder2_to_clear = "D:\MarkTemp\DXFmarktemp"
    folder3_to_clear = "D:\markTemp"
    folders_to_clear = [folder1_to_clear,folder3_to_clear]
    clear_folder_contents(folders_to_clear)

# 在另一个函数中执行清空两个文件夹内容的操作

 #     folder_paths = [r"D:\MarkTemp\PSMarktemp", r"D:\MarkTemp\marktemp", r"D:\MarkTemp\marktemp"]