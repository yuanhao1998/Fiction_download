import pytest

from base.load_response import load
from base.request_manage import post_url
from base.test_base_func import package_param_data


class TestLogin:
    @pytest.mark.parametrize('url', [package_param_data('/user/missing_parameter.yaml')[0]])
    @pytest.mark.parametrize('user', package_param_data('/user/missing_parameter.yaml')[1])
    def test_missing_param(self, url, user):
        response = post_url(url, data=user)
        assert response.status_code == 200, '路径不存在'
        res = load(response)
        assert res['errno'] == 4103, '缺失参数未识别'

    @pytest.mark.parametrize('url', [package_param_data('/user/error_user.yaml')[0]])
    @pytest.mark.parametrize('user', package_param_data('/user/error_user.yaml')[1])
    def test_fail_login(self, url, user):
        response = post_url(url, data=user)
        assert response.status_code == 200, '路径不存在'
        res = load(response)
        assert res['errno'] == 4104, '错误数据未识别'

    @pytest.mark.parametrize('url', [package_param_data('/user/success_login.yaml')[0]])
    @pytest.mark.parametrize('user', package_param_data('/user/success_login.yaml')[1])
    def test_success_login(self, url, user):
        response = post_url(url, data=user)
        assert response.status_code == 200, '路径不存在'
        res = load(response)
        assert res['errno'] == 0, '正确数据无法登录'