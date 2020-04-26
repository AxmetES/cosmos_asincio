def load_img(file_name):
    with open(file_name, 'r')as file:
        result = file.read()
        return result
