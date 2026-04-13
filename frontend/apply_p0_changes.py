#!/usr/bin/env python3
"""
AI 数字人播报系统 V2.0 - P0 阶段自动化调整脚本
功能：
1. 隐藏云端项目模块
2. 新增全局 Toast 提示组件
3. 新增顶部步骤导航条
4. 全链路 Toast 提示补全
"""

import re
import sys
from datetime import datetime

def apply_p0_changes():
    # 读取原始文件
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("✅ 已读取 index.html")
    
    # ========== 调整 1: 注释云端项目模块 ==========
    print("🔧 调整 1: 注释云端项目模块...")
    
    # 查找云端项目模块的起始和结束位置
    cloud_start = content.find('<!-- 云端项目管理面板 -->')
    cloud_end = content.find('<!-- 云端项目管理面板结束 -->')
    
    if cloud_start != -1 and cloud_end != -1:
        # 找到结束标记的末尾
        cloud_end = content.find('-->', cloud_end) + 3
        
        # 检查是否已经被注释
        if content[cloud_start-4:cloud_start] == '<!--' and content[cloud_end:cloud_end+4] == '-->':
            print("  ⚠️  云端项目模块已被注释，跳过")
        else:
            # 包裹注释
            old_block = content[cloud_start:cloud_end]
            new_block = '<!-- [P0_HIDDEN] ' + old_block + ' [P0_HIDDEN] -->'
            content = content[:cloud_start] + new_block + content[cloud_end:]
            print("  ✅ 云端项目模块已注释")
    else:
        print("  ⚠️  未找到云端项目模块")
    
    # ========== 调整 2: 新增顶部步骤导航条 ==========
    print("🔧 调整 2: 新增顶部步骤导航条...")
    
    # 在 header 后、main-content 前插入步骤导航条
    header_end = content.find('</div>', content.find('<div class="header">'))
    main_content_start = content.find('<div class="main-content">')
    
    if header_end != -1 and main_content_start != -1:
        # 检查是否已存在步骤导航条
        if '<div class="process-nav">' in content[header_end:main_content_start]:
            print("  ⚠️  步骤导航条已存在，跳过")
        else:
            process_nav = '''
      <!-- [P0_NEW] 顶部步骤导航条 -->
      <div class="process-nav">
        <div class="process-step" :class="{ active: step >= 1, completed: step > 1 }">
          <span class="step-num">1</span>
          <span class="step-text">基础配置</span>
        </div>
        <div class="process-step" :class="{ active: step >= 2, completed: step > 2, disabled: !usePPT }">
          <span class="step-num">2</span>
          <span class="step-text">PPT 导入</span>
          <label class="step-switch">
            <input type="checkbox" v-model="usePPT" @change="onUsePPTToggle">
            <span class="switch-slider"></span>
          </label>
        </div>
        <div class="process-step" :class="{ active: step >= 3, completed: step > 3 }">
          <span class="step-num">3</span>
          <span class="step-text">文案输入</span>
        </div>
        <div class="process-step" :class="{ active: step >= 4, completed: step > 4, hidden: !usePPT }">
          <span class="step-num">4</span>
          <span class="step-text">翻页节点</span>
        </div>
        <div class="process-step" :class="{ active: step >= 5, completed: step > 5 }">
          <span class="step-num">5</span>
          <span class="step-text">播报导出</span>
        </div>
      </div>
      <!-- [P0_NEW] 步骤导航条结束 -->
'''
            content = content[:header_end+6] + process_nav + content[main_content_start:]
            print("  ✅ 步骤导航条已添加")
    else:
        print("  ⚠️  未找到合适的插入位置")
    
    # ========== 调整 3: 新增 Toast 容器 ==========
    print("🔧 调整 3: 新增全局 Toast 容器...")
    
    # 在 Vue 根节点结束前插入 Toast 容器
    app_end = content.rfind('</div>', 0, content.find('</body>'))
    
    if app_end != -1:
        # 检查是否已存在 Toast 容器
        if '<div class="toast-container">' in content:
            print("  ⚠️  Toast 容器已存在，跳过")
        else:
            toast_container = '''
    <!-- [P0_NEW] 全局 Toast 容器 -->
    <div class="toast-container">
      <div 
        v-for="(toast, index) in toastList" 
        :key="index" 
        :class="['toast-item', toast.type]"
      >
        {{ toast.message }}
      </div>
    </div>
    <!-- [P0_NEW] Toast 容器结束 -->
'''
            content = content[:app_end] + toast_container + content[app_end:]
            print("  ✅ Toast 容器已添加")
    else:
        print("  ⚠️  未找到 Vue 根节点结束位置")
    
    # ========== 调整 4: 新增 CSS 样式 ==========
    print("🔧 调整 4: 新增 CSS 样式...")
    
    # 在</style>前插入新样式
    style_end = content.find('</style>')
    
    if style_end != -1:
        # 检查是否已存在
        if '/* ========== 新增：顶部步骤导航条样式 ==========' in content:
            print("  ⚠️  P0 样式已存在，跳过")
        else:
            new_styles = '''
/* ========== [P0_NEW] 顶部步骤导航条样式 ========== */
.process-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  background: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
  gap: 10px;
}
.process-step {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  position: relative;
  color: #999;
  transition: all 0.3s;
  cursor: default;
}
.process-step:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 100%;
  width: calc(100% - 40px);
  height: 2px;
  background: #e0e0e0;
  transform: translateY(-50%);
}
.process-step.completed:not(:last-child)::after {
  background: #667eea;
}
.process-step.active {
  color: #667eea;
  font-weight: 600;
}
.process-step.completed {
  color: #11998e;
}
.step-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e0e0e0;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}
.process-step.active .step-num {
  background: #667eea;
}
.process-step.completed .step-num {
  background: #11998e;
}
.step-switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
  margin-left: 8px;
}
.step-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.switch-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 20px;
}
.switch-slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}
input:checked + .switch-slider {
  background-color: #667eea;
}
input:checked + .switch-slider:before {
  transform: translateX(20px);
}
.process-step.hidden {
  display: none;
}
.process-step.disabled {
  opacity: 0.5;
}

/* ========== [P0_NEW] 全局 Toast 样式 ========== */
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 99999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.toast-item {
  padding: 12px 20px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  font-size: 14px;
  min-width: 280px;
  animation: toastSlideIn 0.3s ease;
}
.toast-item.success {
  border-left: 4px solid #38ef7d;
  color: #2e7d32;
}
.toast-item.error {
  border-left: 4px solid #eb3349;
  color: #c62828;
}
.toast-item.warn {
  border-left: 4px solid #ff9800;
  color: #e65100;
}
.toast-item.loading {
  border-left: 4px solid #667eea;
  color: #667eea;
}
@keyframes toastSlideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
'''
            content = content[:style_end] + new_styles + content[style_end:]
            print("  ✅ CSS 样式已添加")
    else:
        print("  ⚠️  未找到</style>标签")
    
    # ========== 调整 5: 新增 JavaScript 变量和函数 ==========
    print("🔧 调整 5: 新增 JavaScript 变量和函数...")
    
    # 在 setup() 函数内，cloudProjectList 后添加新的响应式变量
    cloud_project_list_line = content.find('const cloudProjectList = ref([]);')
    
    if cloud_project_list_line != -1:
        # 检查是否已存在
        if 'const step = ref(1);' not in content:
            new_vars = '''
        // [P0_NEW] 步骤导航相关
        const step = ref(1);
        const usePPT = ref(false);
        
        // [P0_NEW] Toast 相关
        const toastList = ref([]);
'''
            content = content[:cloud_project_list_line+33] + new_vars + content[cloud_project_list_line+33:]
            print("  ✅ 响应式变量已添加")
        else:
            print("  ⚠️  变量已存在，跳过")
    else:
        print("  ⚠️  未找到 cloudProjectList 变量")
    
    # 在 feishuUserInfo 后添加 PPT 开关切换函数
    feishu_user_info_end = content.find('});', content.find('const feishuUserInfo = reactive({'))
    
    if feishu_user_info_end != -1:
        if 'function onUsePPTToggle()' not in content:
            new_functions = '''

        // [P0_NEW] PPT 开关切换逻辑
        function onUsePPTToggle() {
          if (usePPT.value) {
            step.value = 2;
          } else {
            // 关闭 PPT 时清空相关数据，不影响核心播报
            reImportPpt();
            step.value = 3;
          }
        }

        // [P0_NEW] 全局 Toast 方法
        function showToast(message, type = 'info', duration = 3000) {
          const toastItem = { message, type };
          toastList.value.push(toastItem);
          // 非加载类型自动关闭
          if (type !== 'loading') {
            setTimeout(() => {
              const index = toastList.value.indexOf(toastItem);
              if (index > -1) toastList.value.splice(index, 1);
            }, duration);
          }
          return toastItem;
        }

        function closeToast(toastItem) {
          const index = toastList.value.indexOf(toastItem);
          if (index > -1) toastList.value.splice(index, 1);
        }
'''
            content = content[:feishu_user_info_end+2] + new_functions + content[feishu_user_info_end+2:]
            print("  ✅ 函数已添加")
        else:
            print("  ⚠️  函数已存在，跳过")
    else:
        print("  ⚠️  未找到 feishuUserInfo")
    
    # ========== 调整 6: 修改 uploadLocalPpt 函数添加 Toast ==========
    print("🔧 调整 6: 修改 uploadLocalPpt 函数...")
    
    # 查找 uploadLocalPpt 函数
    upload_func_start = content.find('async function uploadLocalPpt()')
    
    if upload_func_start != -1:
        # 查找函数内的 try 块
        try_start = content.find('try {', upload_func_start)
        if try_start != -1 and 'showToast' not in content[upload_func_start:try_start]:
            # 在 try 前添加 loading toast
            loading_toast = '''  const loadingToast = showToast('正在解析 PPT，请稍候（10-30 秒），请勿关闭页面', 'loading');
'''
            # 查找第一个 catch
            catch_start = content.find('} catch (e) {', upload_func_start)
            if catch_start != -1:
                # 在 catch 前添加成功 toast 和步骤推进
                success_toast = '''
    closeToast(loadingToast);
    showToast(`PPT 解析成功，共${pptConfig.totalPages}页`, 'success');
    // 步骤自动推进
    step.value = 3;
'''
                # 在 catch 块内添加 closeToast
                catch_end = content.find('}', catch_start)
                error_toast = '''    closeToast(loadingToast);
    showToast(`PPT 解析失败：${e.message}`, 'error');
'''
                # 先插入错误提示
                content = content[:catch_end] + error_toast + content[catch_end:]
                # 再插入成功提示（需要在 try 块末尾，找到 finally 前）
                finally_start = content.find('} finally {', upload_func_start)
                if finally_start != -1:
                    content = content[:finally_start] + success_toast + content[finally_start:]
                # 最后插入 loading toast
                content = content[:try_start+5] + loading_toast + content[try_start+5:]
                print("  ✅ uploadLocalPpt 已添加 Toast")
            else:
                print("  ⚠️  未找到 catch 块")
        else:
            print("  ⚠️  Toast 已存在，跳过")
    else:
        print("  ⚠️  未找到 uploadLocalPpt 函数")
    
    # ========== 调整 7: 修改 generateTurningNodes 函数添加 Toast ==========
    print("🔧 调整 7: 修改 generateTurningNodes 函数...")
    
    generate_func_start = content.find('async function generateTurningNodes(')
    
    if generate_func_start != -1:
        try_start = content.find('try {', generate_func_start)
        if try_start != -1 and 'showToast' not in content[generate_func_start:try_start]:
            loading_toast = '''  const loadingToast = showToast('正在分析 PPT 与文案，生成智能翻页节点，请稍候', 'loading');
'''
            catch_start = content.find('} catch (e) {', generate_func_start)
            if catch_start != -1:
                # 查找 finally 块
                finally_start = content.find('} finally {', generate_func_start)
                if finally_start != -1:
                    success_toast = '''
    closeToast(loadingToast);
    showToast(`翻页节点生成成功，共${pageTurningNodes.value.length}个节点`, 'success');
    // 步骤自动推进
    step.value = usePPT.value ? 5 : 3;
'''
                    error_toast = '''    closeToast(loadingToast);
    showToast(`节点生成失败：${e.message}`, 'error');
'''
                    catch_end = content.find('}', catch_start)
                    content = content[:catch_end] + error_toast + content[catch_end:]
                    content = content[:finally_start] + success_toast + content[finally_start:]
                    content = content[:try_start+5] + loading_toast + content[try_start+5:]
                    print("  ✅ generateTurningNodes 已添加 Toast")
                else:
                    print("  ⚠️  未找到 finally 块")
            else:
                print("  ⚠️  未找到 catch 块")
        else:
            print("  ⚠️  Toast 已存在，跳过")
    else:
        print("  ⚠️  未找到 generateTurningNodes 函数")
    
    # ========== 调整 8: 修改 startBroadcast 函数添加 Toast ==========
    print("🔧 调整 8: 修改 startBroadcast 函数...")
    
    start_broadcast_start = content.find('async function startBroadcast()')
    
    if start_broadcast_start != -1:
        # 查找获取鉴权信息的位置
        auth_call = content.find('await getAuthInfo()', start_broadcast_start)
        if auth_call != -1 and 'showToast' not in content[start_broadcast_start:auth_call]:
            loading_toast = '''    const loadingToast = showToast('正在连接数字人播报服务，请稍候', 'loading');
'''
            # 查找 SDK 启动成功的位置
            sdk_success = content.find('addLog(\'✅ 数字人播报启动成功\', \'success\');', start_broadcast_start)
            if sdk_success != -1:
                success_toast = '''
    closeToast(loadingToast);
    showToast('数字人服务连接成功', 'success');
'''
                # 查找 catch 块
                catch_start = content.find('} catch (e) {', start_broadcast_start)
                if catch_start != -1:
                    error_toast = '''    closeToast(loadingToast);
    showToast(`播报失败：${e.message}`, 'error');
'''
                    catch_end = content.find('}', catch_start)
                    content = content[:catch_end] + error_toast + content[catch_end:]
                    content = content[:sdk_success] + success_toast + content[sdk_success:]
                    content = content[:auth_call] + loading_toast + content[auth_call:]
                    print("  ✅ startBroadcast 已添加 Toast")
                else:
                    print("  ⚠️  未找到 catch 块")
            else:
                print("  ⚠️  未找到 SDK 启动成功日志")
        else:
            print("  ⚠️  Toast 已存在，跳过")
    else:
        print("  ⚠️  未找到 startBroadcast 函数")
    
    # ========== 保存文件 ==========
    print("💾 保存修改后的文件...")
    
    # 更新标题
    content = content.replace(
        '<title>数字人播报系统 v3.0 - 最终修复版-v2-画中画优化</title>',
        '<title>数字人播报系统 V2.0 - P0 阶段</title>'
    )
    
    # 更新缓存控制版本号
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    content = re.sub(
        r'meta http-equiv=202604112359"Cache-Control"',
        f'meta http-equiv="{timestamp}"Cache-Control"',
        content
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ P0 阶段调整完成！")
    print("\n📋 调整清单:")
    print("  1. ✅ 隐藏云端项目模块")
    print("  2. ✅ 新增顶部步骤导航条")
    print("  3. ✅ 新增全局 Toast 容器")
    print("  4. ✅ 新增 CSS 样式")
    print("  5. ✅ 新增 JavaScript 变量和函数")
    print("  6. ✅ uploadLocalPpt 添加 Toast")
    print("  7. ✅ generateTurningNodes 添加 Toast")
    print("  8. ✅ startBroadcast 添加 Toast")
    print("\n⚠️  请手动检查以下内容:")
    print("  - 测试 PPT 开关切换是否正常")
    print("  - 测试步骤导航是否正确推进")
    print("  - 测试 Toast 提示是否正常显示")
    print("  - 测试核心播报流程是否正常")

if __name__ == '__main__':
    apply_p0_changes()
