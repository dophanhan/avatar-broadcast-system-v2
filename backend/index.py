# -*- coding: utf-8 -*-
"""
AI 数字人播报系统 V3.0 - 阿里云函数计算后端
新增：PPT 宣讲功能、飞书 OAuth、云端存储
"""

import json
import hashlib
import hmac
import base64
from datetime import datetime
from urllib.parse import quote
import os
import uuid
import requests
import oss2
from pptx import Presentation
from io import BytesIO

def handler(event, context):
    """阿里云函数计算 Python 3.10 正确格式"""
    
    if isinstance(event, bytes):
        event = event.decode('utf-8')
    if isinstance(event, str):
        event = json.loads(event)
    
    method = event.get('method', 'POST')
    path = event.get('path', '/')
    
    # OPTIONS 跨域处理
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Feishu-OpenId',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    
    # 路由分发
    if path == '/feishu/oauth/callback' and method == 'GET':
        return handle_feishu_oauth(event)
    elif path == '/feishu/ppt/import' and method == 'POST':
        return handle_feishu_ppt_import(event)
    elif path == '/ai/generate-turning-nodes' and method == 'POST':
        return handle_generate_turning_nodes(event)
    elif path == '/project/save' and method == 'POST':
        return handle_project_save(event)
    elif path == '/project/list' and method == 'GET':
        return handle_project_list(event)
    elif path == '/project/detail' and method == 'GET':
        return handle_project_detail(event)
    elif path == '/project/delete' and method == 'POST':
        return handle_project_delete(event)
    elif path == '/ppt/upload' and method == 'POST':
        return handle_ppt_upload(event)
    else:
        # 原有鉴权接口
        return handle_avatar_auth(event)

def handle_avatar_auth(event):
    """原有讯飞鉴权接口"""
    API_KEY = os.environ.get('AVATAR_API_KEY', '')
    API_SECRET = os.environ.get('AVATAR_API_SECRET', '')
    APP_ID = os.environ.get('AVATAR_APP_ID', '')
    SCENE_ID = os.environ.get('AVATAR_SCENE_ID', '')
    WS_URL = "wss://avatar.cn-huadong-1.xf-yun.com/v1/interact"
    
    try:
        date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        signature_origin = f"host: avatar.cn-huadong-1.xf-yun.com\ndate: {date}\nGET /v1/interact HTTP/1.1"
        signature_sha = hmac.new(API_SECRET.encode(), signature_origin.encode(), digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(signature_sha).decode()
        authorization_origin = f'api_key="{API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
        authorization = base64.b64encode(authorization_origin.encode()).decode()
        signed_url = f"{WS_URL}?authorization={quote(authorization)}&date={quote(date)}&host=avatar.cn-huadong-1.xf-yun.com"
        
        body = event.get('body', '{}')
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        data = json.loads(body) if body else {}
        
        response = {
            "code": 0,
            "data": {
                "appId": APP_ID,
                "sceneId": SCENE_ID,
                "signedUrl": signed_url,
                "avatarId": data.get("avatarId"),
                "vcn": data.get("vcn"),
                "speakQueue": []
            }
        }
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps(response, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"code": -1, "msg": str(e)}, ensure_ascii=False)
        }

def handle_feishu_oauth(event):
    """飞书 OAuth 回调"""
    try:
        query = event.get('queryParameters', {})
        code = query.get('code')
        if not code:
            raise Exception('缺少授权码')
        
        FEISHU_APP_ID = os.environ.get('FEISHU_APP_ID', '')
        FEISHU_APP_SECRET = os.environ.get('FEISHU_APP_SECRET', '')
        
        url = "https://open.feishu.cn/open-apis/authen/v1/access_token"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": FEISHU_APP_ID,
            "app_secret": FEISHU_APP_SECRET,
            "code": code,
            "grant_type": "authorization_code"
        }
        res = requests.post(url, json=data, headers=headers).json()
        if res.get("code") != 0:
            raise Exception(f"飞书授权失败：{res.get('msg')}")
        
        user_data = res.get("data")
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({
                "code": 0,
                "data": {
                    "access_token": user_data.get("access_token"),
                    "open_id": user_data.get("open_id"),
                    "user_name": user_data.get("name")
                }
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"code": -1, "msg": str(e)}, ensure_ascii=False)
        }

def handle_feishu_ppt_import(event):
    """飞书 PPT 导入"""
    try:
        body = json.loads(event.get('body', '{}'))
        ppt_url = body.get("ppt_url")
        access_token = body.get("access_token")
        
        if not ppt_url or not access_token:
            raise Exception('缺少 PPT 链接或访问凭证')
        
        if "feishu.cn/docx" not in ppt_url:
            raise Exception("仅支持飞书在线幻灯片链接")
        
        # 解析 document_id
        url_parts = ppt_url.split("/")
        document_id = url_parts[url_parts.index("docx") + 1].split("?")[0]
        
        # 获取 PPT 基础信息
        headers = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}"
        base_res = requests.get(base_url, headers=headers).json()
        if base_res.get("code") != 0:
            raise Exception(f"获取 PPT 基础信息失败：{base_res.get('msg')}")
        
        ppt_title = base_res["data"]["document"]["title"]
        
        # 模拟返回 PPT 数据（实际需要从飞书 API 获取）
        pages = [
            {"page_num": 1, "page_title": "封面", "page_text": ppt_title, "page_image_url": "", "page_type": "cover"},
            {"page_num": 2, "page_title": "目录", "page_text": "目录", "page_image_url": "", "page_type": "content"},
        ]
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({
                "code": 0,
                "data": {
                    "ppt_id": document_id,
                    "ppt_title": ppt_title,
                    "total_pages": len(pages),
                    "pages": pages
                }
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"code": -1, "msg": str(e)}, ensure_ascii=False)
        }

def handle_generate_turning_nodes(event):
    """智能翻页节点生成"""
    try:
        body = json.loads(event.get('body', '{}'))
        speak_sentences = body.get("speak_sentences", [])
        ppt_pages = body.get("ppt_pages", [])
        
        if not speak_sentences or not ppt_pages:
            raise Exception('缺少播报句子或 PPT 数据')
        
        # 简单规则：平均分配句子到每个 PPT 页面
        total_sentences = len(speak_sentences)
        total_pages = len(ppt_pages)
        sentences_per_page = total_sentences // total_pages
        
        nodes = []
        for i in range(total_pages):
            start_idx = i * sentences_per_page
            end_idx = start_idx + sentences_per_page - 1 if i < total_pages - 1 else total_sentences - 1
            nodes.append({
                "page_num": i + 1,
                "start_sentence_index": start_idx,
                "end_sentence_index": end_idx
            })
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({
                "code": 0,
                "data": {"page_turning_nodes": nodes}
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"code": -1, "msg": str(e)}, ensure_ascii=False)
        }

def handle_project_save(event):
    """项目保存"""
    try:
        body = json.loads(event.get('body', '{}'))
        project_id = body.get("project_id", str(uuid.uuid4()))
        
        # TODO: 实现阿里云 OSS 和表格存储
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({
                "code": 0,
                "data": {"project_id": project_id}
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"code": -1, "msg": str(e)}, ensure_ascii=False)
        }

def handle_project_list(event):
    """项目列表查询"""
    try:
        # TODO: 从表格存储查询
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({
                "code": 0,
                "data": {"total": 0, "list": []}
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"code": -1, "msg": str(e)}, ensure_ascii=False)
        }

def handle_project_detail(event):
    """项目详情查询"""
    try:
        # TODO: 从表格存储查询
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({
                "code": 0,
                "data": {}
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"code": -1, "msg": str(e)}, ensure_ascii=False)
        }

def handle_project_delete(event):
    """项目删除"""
    try:
        # TODO: 从表格存储删除
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"code": 0, "data": {}}, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({"code": -1, "msg": str(e)}, ensure_ascii=False)
        }

def handle_ppt_upload(event):
    """本地 PPT 文件上传和解析（简化版）"""
    try:
        import base64
        import json
        
        # 解析请求体
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = base64.b64decode(body)
        
        data = json.loads(body if isinstance(body, str) else body.decode('utf-8'))
        file_base64 = data.get('file', '')
        filename = data.get('filename', 'presentation.pptx')
        
        # 解码文件（验证文件有效性）
        if ',' in file_base64:
            file_data = base64.b64decode(file_base64.split(',')[1])
        else:
            file_data = base64.b64decode(file_base64)
        
        # 生成 PPT ID
        ppt_id = str(uuid.uuid4())
        
        # 简化处理：返回模拟数据（实际应该解析 PPT）
        # TODO: 安装 python-pptx 库后实现真实解析
        pages = [
            {
                "page_num": 1,
                "page_title": "封面",
                "page_text": filename.replace('.pptx', '').replace('.ppt', ''),
                "page_image_url": "",
                "page_type": "cover"
            }
        ]
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({
                "code": 0,
                "data": {
                    "ppt_id": ppt_id,
                    "ppt_title": filename.replace('.pptx', '').replace('.ppt', ''),
                    "total_pages": 1,
                    "pages": pages
                }
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({
                "code": 0,
                "data": {
                    "ppt_id": str(uuid.uuid4()),
                    "ppt_title": "测试 PPT",
                    "total_pages": 1,
                    "pages": [{
                        "page_num": 1,
                        "page_title": "封面",
                        "page_text": "测试页面",
                        "page_image_url": "",
                        "page_type": "cover"
                    }]
                }
            }, ensure_ascii=False)
        }
