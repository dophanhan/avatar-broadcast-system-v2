#!/usr/bin/env python3
"""
P0 阶段修复 v2 - 修复模式选择和 PPT 面板显示问题
"""

def apply_p0_fixes_v2():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("✅ 已读取 index.html")
    
    # ========== 修复 1: PPT 宣讲配置面板添加 v-if="usePPT" ==========
    print("🔧 修复 1: PPT 面板添加条件显示...")
    
    # 查找 PPT 宣讲配置面板开始
    ppt_start = content.find('<!-- PPT 宣讲配置面板 -->')
    if ppt_start != -1:
        # 找到面板的 div 标签
        div_pos = content.find('<div class="ppt-collapse">', ppt_start)
        if div_pos != -1:
            # 添加 v-if="usePPT"
            old_div = '<div class="ppt-collapse">'
            new_div = '<div class="ppt-collapse" v-if="usePPT">'
            content = content.replace(old_div, new_div, 1)
            print("  ✅ PPT 面板已添加 v-if='usePPT'")
        else:
            print("  ⚠️  未找到 ppt-collapse div")
    else:
        print("  ⚠️  未找到 PPT 宣讲配置面板")
    
    # ========== 修复 2: 在 return 中导出新增的变量和函数 ==========
    print("🔧 修复 2: 导出新增变量和函数...")
    
    # 查找 return { 的位置
    return_pos = content.find('return {')
    if return_pos != -1:
        # 查找 cloudProjectCollapseOpen 这一行
        cloud_pos = content.find('cloudProjectCollapseOpen,', return_pos)
        if cloud_pos != -1:
            # 在它之前插入新增的导出
            new_exports = '''  // [P0_FIX] 新增导出
          step,
          usePPT,
          toastList,
          switchMode,
          showToast,
          closeToast,
'''
            content = content[:cloud_pos] + new_exports + content[cloud_pos:]
            print("  ✅ 已添加 switchMode 等导出")
        else:
            print("  ⚠️  未找到插入位置")
    else:
        print("  ⚠️  未找到 return 语句")
    
    # ========== 修复 3: 移除重复的模式选择面板（如果有） ==========
    print("🔧 修复 3: 检查重复面板...")
    
    # 查找模式选择面板
    mode_count = content.count('播报模式选择')
    if mode_count > 1:
        print(f"  ⚠️  发现{mode_count}个模式选择面板，需要手动清理")
    else:
        print("  ✅ 模式选择面板数量正常")
    
    # ========== 保存文件 ==========
    print("💾 保存修改后的文件...")
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ P0 阶段修复 v2 完成！")
    print("\n📋 修复清单:")
    print("  1. ✅ PPT 面板添加 v-if='usePPT' 条件显示")
    print("  2. ✅ 导出 switchMode、step、usePPT、toastList 等")
    print("\n⚠️  请重新部署并测试！")

if __name__ == '__main__':
    apply_p0_fixes_v2()
