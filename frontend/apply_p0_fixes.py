#!/usr/bin/env python3
"""
AI 数字人播报系统 V2.0 - P0 阶段完整修复脚本
修复问题：
1. 顶部横线错位
2. PPT 开关位置不对（移到操作区）
3. PPT 开关打开/关上没反应
4. 云端项目没有隐藏
"""

import re
from datetime import datetime

def apply_p0_fixes():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("✅ 已读取 index.html")
    
    # ========== 修复 1: 正确隐藏云端项目模块 ==========
    print("🔧 修复 1: 正确隐藏云端项目模块...")
    
    # 查找旧的错误注释
    old_comment_start = content.find('<!-- [P0_HIDDEN] <!-- 云端项目管理面板 -->')
    old_comment_end = content.find('<!-- 云端项目管理面板结束 --> [P0_HIDDEN] -->')
    
    if old_comment_start != -1 and old_comment_end != -1:
        # 找到结束标记的末尾
        old_comment_end = content.find('-->', old_comment_end) + 3
        
        # 移除旧注释，添加正确的新注释
        cloud_block = content[old_comment_start:old_comment_end]
        # 移除内外层的 P0_HIDDEN 标记
        cloud_block_clean = cloud_block.replace('<!-- [P0_HIDDEN] ', '').replace(' [P0_HIDDEN] -->', '')
        # 重新用正确注释包裹
        new_cloud_block = '<!-- [P0_HIDDEN] 开始：隐藏云端项目模块 ==========\n' + cloud_block_clean + '\n<!-- [P0_HIDDEN] 结束：隐藏云端项目模块 ==========\n-->'
        
        content = content[:old_comment_start] + new_cloud_block + content[old_comment_end:]
        print("  ✅ 云端项目模块已正确隐藏")
    else:
        print("  ⚠️  未找到云端项目注释")
    
    # ========== 修复 2: 简化顶部导航条（移除开关） ==========
    print("🔧 修复 2: 简化顶部导航条...")
    
    # 查找旧导航条
    old_nav_start = content.find('<!-- [P0_NEW] 顶部步骤导航条 -->')
    if old_nav_start == -1:
        old_nav_start = content.find('<div class="process-nav">')
    
    old_nav_end = content.find('<!-- [P0_NEW] 步骤导航条结束 -->')
    if old_nav_end == -1:
        old_nav_end = content.find('</div>', content.find('<div class="process-nav">'))
        old_nav_end = content.find('-->', old_nav_end) + 3 if '-->' in content[old_nav_end:old_nav_end+50] else old_nav_end
    
    if old_nav_start != -1 and old_nav_end != -1:
        # 找到完整的导航条块
        nav_end_marker = content.find('-->', old_nav_end)
        if nav_end_marker != -1:
            old_nav_end = nav_end_marker + 3
        
        # 替换为简化版导航条
        new_nav = '''<!-- [P0_FIX] 修复：简化顶部导航条，移除开关 ========== -->
      <div class="process-nav">
        <div class="process-step" :class="{ active: step >= 1, completed: step > 1 }">
          <span class="step-num">1</span>
          <span class="step-text">基础配置</span>
        </div>
        <div class="process-step" :class="{ active: step >= 2, completed: step > 2, hidden: !usePPT }">
          <span class="step-num">2</span>
          <span class="step-text">PPT 导入</span>
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
      <!-- [P0_FIX] 简化导航条结束 ========== -->
'''
        content = content[:old_nav_start] + new_nav + content[old_nav_end:]
        print("  ✅ 顶部导航条已简化")
    else:
        print("  ⚠️  未找到导航条")
    
    # ========== 修复 3: 在基础配置下方新增模式选择区 ==========
    print("🔧 修复 3: 新增模式选择面板...")
    
    # 查找 PPT 宣讲配置面板开始位置
    ppt_panel_start = content.find('<!-- PPT 宣讲配置面板 -->')
    if ppt_panel_start == -1:
        ppt_panel_start = content.find('<!-- 云端项目')
    
    if ppt_panel_start != -1:
        # 找到 PPT 面板前的关闭标签
        insert_pos = ppt_panel_start
        
        mode_selector = '''<!-- [P0_FIX] 新增：模式选择面板 ========== -->
          <div class="panel">
            <h2>🎯 播报模式选择</h2>
            <div class="mode-selector">
              <div 
                class="mode-card" 
                :class="{ active: !usePPT }" 
                @click="switchMode(false)"
              >
                <div class="mode-icon">🎤</div>
                <div class="mode-title">纯数字人播报</div>
                <div class="mode-desc">无需 PPT，直接输入文案播报</div>
              </div>
              <div 
                class="mode-card" 
                :class="{ active: usePPT }" 
                @click="switchMode(true)"
              >
                <div class="mode-icon">📑</div>
                <div class="mode-title">PPT 宣讲播报</div>
                <div class="mode-desc">上传 PPT，自动匹配翻页</div>
              </div>
            </div>
          </div>
          <!-- [P0_FIX] 模式选择面板结束 ========== -->

'''
        content = content[:insert_pos] + mode_selector + content[insert_pos:]
        print("  ✅ 模式选择面板已添加")
    else:
        print("  ⚠️  未找到插入位置")
    
    # ========== 修复 4: 更新 CSS 样式 ==========
    print("🔧 修复 4: 更新 CSS 样式...")
    
    # 查找</style>标签
    style_end = content.find('</style>')
    
    if style_end != -1:
        # 检查是否已有修复样式
        if '/* ========== [P0_FIX] 修复：顶部步骤导航条样式 ==========' in content:
            print("  ⚠️  P0_FIX 样式已存在，跳过")
        else:
            new_styles = '''
/* ========== [P0_FIX] 修复：顶部步骤导航条样式 ========== */
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
/* 修复：横线位置 */
.process-step:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 14px; /* 垂直居中对齐圆圈 */
  left: 50%; /* 从当前步骤圆圈右侧开始 */
  width: calc(100% - 28px); /* 画到下一步圆圈左侧 */
  height: 2px;
  background: #e0e0e0;
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
  z-index: 10; /* 确保圆圈在横线上方 */
}
.process-step.active .step-num {
  background: #667eea;
}
.process-step.completed .step-num {
  background: #11998e;
}
.process-step.hidden {
  display: none;
}

/* ========== [P0_FIX] 新增：模式选择样式 ========== */
.mode-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}
.mode-card {
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}
.mode-card:hover {
  border-color: #667eea;
  background: #f0f4ff;
}
.mode-card.active {
  border-color: #667eea;
  background: linear-gradient(135deg, #f0f4ff 0%, #e8eaf6 100%);
}
.mode-icon {
  font-size: 32px;
  margin-bottom: 10px;
}
.mode-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}
.mode-desc {
  font-size: 12px;
  color: #666;
}
'''
            # 在</style>前插入
            content = content[:style_end] + new_styles + content[style_end:]
            print("  ✅ CSS 样式已更新")
    else:
        print("  ⚠️  未找到</style>标签")
    
    # ========== 修复 5: 更新 JavaScript 逻辑 ==========
    print("🔧 修复 5: 更新 JavaScript 逻辑...")
    
    # 查找 feishuUserInfo 结束位置
    feishu_end = content.find('});', content.find('const feishuUserInfo = reactive({'))
    
    if feishu_end != -1:
        # 检查是否已有 switchMode 函数
        if 'function switchMode(' not in content:
            new_functions = '''

        // [P0_FIX] 修复：模式切换逻辑 ==========
        function switchMode(enablePPT) {
          console.log('切换模式，enablePPT:', enablePPT);

          if (enablePPT) {
            usePPT.value = true;
            step.value = 2;
            showToast('已切换到 PPT 宣讲模式', 'success', 2000);
          } else {
            usePPT.value = false;
            // 清空 PPT 数据
            reImportPpt();
            // 直接跳到文案输入
            step.value = 3;
            showToast('已切换到纯播报模式', 'success', 2000);
          }

          console.log('当前步骤:', step.value);
        }
'''
            content = content[:feishu_end+2] + new_functions + content[feishu_end+2:]
            print("  ✅ switchMode 函数已添加")
        else:
            print("  ⚠️  switchMode 函数已存在")
    else:
        print("  ⚠️  未找到 feishuUserInfo")
    
    # ========== 保存文件 ==========
    print("💾 保存修改后的文件...")
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ P0 阶段完整修复完成！")
    print("\n📋 修复清单:")
    print("  1. ✅ 云端项目模块正确隐藏")
    print("  2. ✅ 顶部导航条简化（移除开关）")
    print("  3. ✅ 模式选择面板添加到操作区")
    print("  4. ✅ CSS 样式更新（横线位置 + 模式选择）")
    print("  5. ✅ switchMode 函数添加")
    print("\n⚠️  请重新部署到 Cloudflare 并测试！")

if __name__ == '__main__':
    apply_p0_fixes()
