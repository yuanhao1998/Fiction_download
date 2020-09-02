from base.data_manage import read_file


def package_param_data(filename):  # 返回获取到的字典数据
    data = read_file(filename)
    return list(data.values())