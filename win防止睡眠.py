# prevent_sleep_efficient.py
import ctypes
import time
import argparse

# 定义Windows API所需的常量
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
# ES_DISPLAY_REQUIRED = 0x00000002  # 如果需要防止熄屏，可以取消注释此常量

def prevent_sleep():
    """
    调用SetThreadExecutionState API防止系统进入睡眠模式。
    此调用会持续有效，直到程序退出。
    """
    print("✅ 开始阻止系统睡眠...（程序退出后自动恢复）")
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    )

def allow_sleep():
    """
    重置线程执行状态，允许系统正常睡眠。
    通常不需要手动调用，因为程序退出时会自动恢复。
    """
    print("✅ 已恢复系统正常睡眠模式。")
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='高效防止系统进入睡眠模式。')
    parser.add_argument('--minutes', '-m', type=int, default=None,
                        help='设置程序运行的超时时间（分钟），时间到后自动退出并恢复睡眠。如不设置，则一直运行。')

    args = parser.parse_args()
    timeout_seconds = args.minutes * 60 if args.minutes else None

    try:
        # 阻止睡眠
        prevent_sleep()
        start_time = time.time()

        # 主循环：保持程序运行，同时检查超时
        print(f"🚀 防睡眠程序已启动。CPU/内存占用极低。")
        if timeout_seconds:
            print(f"⏰ 程序将在 {args.minutes} 分钟后自动退出。")
        else:
            print("⏰ 程序将一直运行，按 Ctrl+C 手动退出。")

        while True:
            # 这里什么都不做，只是等待，是资源占用低的关键
            time.sleep(10)  # 每10秒检查一次，减少循环频率

            # 检查超时
            if timeout_seconds and (time.time() - start_time) > timeout_seconds:
                print("⏰ 预设时间已到，程序自动退出。")
                break

    except KeyboardInterrupt:
        # 捕获Ctrl+C信号，优雅退出
        print("\n🛑 用户手动中断程序。")
    finally:
        # 无论何种方式退出，都确保恢复系统睡眠功能
        allow_sleep()