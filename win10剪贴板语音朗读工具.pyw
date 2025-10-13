#功能介绍：运行后检测剪贴板变化，如果剪贴板变化，则朗读其中复制的内容。
#欢迎赞助、打赏、捐点小钱至：https://mp.weixin.qq.com/s/Nc-cpQDkD6Vo-oLo5UXlTg
#                   （本人公众号文章）
import win32clipboard as clip
import pyperclip
import time
import subprocess
import os

class ClipboardTTS:
    def __init__(self):
        self.last_content = ""
        self.code=clip.GetClipboardSequenceNumber()
        self.current_process = None
        print("剪贴板语音朗读工具已启动")
        print("正在监控剪贴板...")
        print("按Ctrl+C停止程序")
        self.speak('工具启动！！欢迎使用windows剪贴板语音阅读辅助工具！让我们愉快的开始吧！')
    
    def clean_text(self, text):
        """清理文本内容，确保安全执行"""
        if not text or len(text.strip()) < 1:
            return None
        
        # 移除可能破坏PowerShell命令的特殊字符
        text = text.replace('"', '').replace("'", "").replace("`", "").replace("$", "")
        text = ' '.join(text.split())  # 标准化空格
        
        if len(text) > 1000:
            text = text[:1000] + "..."
        
        return text
    
    def stop_speech(self):
        """强制停止当前朗读进程"""
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate()
            self.current_process.wait()
            self.current_process = None
            print("已中断当前朗读")
    
    def speak(self, text):
        """使用系统原生语音引擎朗读文本"""
        cleaned_text = self.clean_text(text)
        if not cleaned_text:
            return False
        
        try:
            # 使用Windows原生Speech.Synthesizer（最稳定）
            ps_command = f'''
            Add-Type -AssemblyName System.Speech
            $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $speak.Speak("{cleaned_text}")
            '''
            
            # 启动独立进程执行朗读
            self.current_process = subprocess.Popen(
                ["powershell", "-Command", ps_command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return True
        except Exception as e:
            print(f"朗读启动失败: {e}")
            return False
    
    def monitor(self):
        """主监控循环"""
        try:
            while True:
                # 检查剪贴板内容
                try:
                    current_content = pyperclip.paste()
                    current_code=clip.GetClipboardSequenceNumber()
                except:
                    current_content = ""
                
                # 检测有效的内容变化
                if (current_content and 
                    self.code !=clip.GetClipboardSequenceNumber() and 
                    len(current_content.strip()) > 0):
                    
                    self.last_content = current_content
                    self.code=clip.GetClipboardSequenceNumber()
                    print(f"检测到新内容: {current_content[:100]}...")
                    
                    # 停止当前朗读并开始新的
                    self.stop_speech()
                    time.sleep(0.1)  # 确保完全停止
                    
                    # 在新进程中开始朗读
                    if self.speak(current_content):
                        print("开始朗读新内容")
                
                time.sleep(0.3)  # 监控间隔
                
        except KeyboardInterrupt:
            print("\n程序停止")
        except Exception as e:
            print(f"监控错误: {e}")
        finally:
            self.stop_speech()

def main():
    print("=" * 50)
    print("剪贴板语音朗读工具 - 系统级解决方案")
    print("特点: 使用Windows原生语音引擎，中断100%可靠")
    print("=" * 50)
    
    tts = ClipboardTTS()
    tts.monitor()

if __name__ == "__main__":
    main()
