from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.template import loader
from .my_util import get_random_str
import logging
logger = logging.getLogger('django')
# Create your views here.

def send_my_email(req):
    title = '阿里offer'
    msg = '恭喜你获得酱油一瓶'
    email_from = settings.DEFAULT_FROM_EMAIL
    reciever = [
        '476745582@qq.com'
    ]
    # 发送邮件
    send_mail(title,msg,email_from,reciever)
    return HttpResponse('ok')

def sned_email_v1(req):
    title = '阿里offer'
    msg = ''
    email_from = settings.DEFAULT_FROM_EMAIL
    reciever = [
        '476745582@qq.com'
    ]
    # 加载模板
    template = loader.get_template('email.html')
    # 渲染模板
    html_str = template.render({'msg':'双击666'})
    # 发送邮件
    send_mail(title, msg, email_from, reciever,html_message=html_str)
    return HttpResponse('ok')

def verify(req):
    if req.method == 'GET':
        return render(req,'verify.html')
    else:
        params = req.POST
        email = params.get('email')
#         生成随机字符
        random_str = get_random_str()
#         拼接验证连接
        url = 'http://120.79.56.168:1234/gz08/active/'+random_str
        # 加载模板
        tmp = loader.get_template('active.html')
        # 渲染
        html_str = tmp.render({'url':url})
#         准备邮件数据
        title = '阿里offer'
        msg = ''
        email_from = settings.DEFAULT_FROM_EMAIL
        reciever = [
            email
        ]
        # 发送邮件
        send_mail(title, msg, email_from, reciever, html_message=html_str)
        # 记录token对应的邮箱是谁
        cache.set(random_str,email,120)
        return HttpResponse('ok')

def active(req, random_str):
#     拿参数对应的缓存数据
    res = cache.get(random_str)
    if res:
        # 通过邮箱找到对应的用户
        # 给用户的状态字段做更新 从未激活状态变为激活状态

        return HttpResponse(res+'激活成功')
    else:
        return HttpResponse('验证连接无效')


def test_log(req):
    logger.info('要下课了')
    return HttpResponse('好开心')
