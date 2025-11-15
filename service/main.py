import sys
import subprocess
import os
import json


DEVICE = os.getenv("DEVICE", "127.0.0.1:16384")

def adb_click(x, y):
    """通过ADB执行点击操作"""
    try:
        subprocess.run(
            ["adb", "-s", DEVICE, "shell", f"input tap {x} {y}"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"ADB点击成功：({x}, {y})")
    except subprocess.CalledProcessError as e:
        print(f"ADB点击失败：{e}")


name = '2.png'
os.environ['muban'] = name  # 传递模板名称给opencv.py

try:
    # 执行子进程，捕获标准输出和错误
    result = subprocess.run(
        [sys.executable, "opencv.py"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # 输出转为字符串（方便解析）
    )
    
    # 解析输出：最后一行是JSON格式的结果
    output_lines = result.stdout.strip().split('\n')
    results_json = output_lines[-1]  # 取最后一行JSON数据
    results = json.loads(results_json)  # 解析为字典
    
    # 获取当前模板的坐标
    coord = results.get(name)
    if coord:
        try:
            x, y = coord  # 从元组中提取x和y
            x = int(x)
            y = int(y)
            adb_click(x, y)
        except (ValueError, TypeError):
            print(f"坐标格式错误：{coord}")
    else:
        print(f"未获取到{name}的有效坐标")

except subprocess.CalledProcessError as e:
    print(f"opencv.py执行失败：{e.stderr}")
except json.JSONDecodeError:
    print("解析opencv.py输出失败，格式不正确")
except Exception as e:
    print(f"发生错误：{e}")