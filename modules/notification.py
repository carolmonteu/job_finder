import os
import subprocess

class Notifier:
    @staticmethod
    def send(message, enabled=True):
        if not enabled:
            return
            
        try:
            if os.name == 'posix':
                subprocess.run(['notify-send', '🛡️ CyberJob Notifier', message])
            elif os.name == 'nt':
                from win10toast import ToastNotifier
                ToastNotifier().show_toast("CyberJob Notifier", message, duration=10)
        except Exception as e:
            print(f"Notification error: {e}")