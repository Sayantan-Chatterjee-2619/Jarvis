"""
Browser and App Automation Controller
Supports opening/closing browsers and applications cross-platform
"""
import subprocess
import sys
import os
import platform
import time

class BrowserController:
    """Controls browser instances"""
    
    def __init__(self):
        self.platform = platform.system()
        self.processes = {}
    
    def open_browser(self, browser_name, url=None):
        """Open a browser with optional URL"""
        browser_name = browser_name.lower()
        cmd = []
        
        if self.platform == "Windows":
            if browser_name in ["chrome", "google chrome"]:
                cmd = ["start", "", "chrome", url] if url else ["start", "", "chrome"]
            elif browser_name in ["firefox", "mozilla"]:
                cmd = ["start", "", "firefox", url] if url else ["start", "", "firefox"]
            elif browser_name == "edge":
                cmd = ["start", "", "msedge", url] if url else ["start", "", "msedge"]
        elif self.platform == "Darwin":  # macOS
            if browser_name in ["chrome", "google chrome"]:
                cmd = ["open", "-a", "Google Chrome", url] if url else ["open", "-a", "Google Chrome"]
            elif browser_name in ["firefox", "mozilla"]:
                cmd = ["open", "-a", "Firefox", url] if url else ["open", "-a", "Firefox"]
            elif browser_name == "safari":
                cmd = ["open", "-a", "Safari", url] if url else ["open", "-a", "Safari"]
            elif browser_name == "edge":
                cmd = ["open", "-a", "Microsoft Edge", url] if url else ["open", "-a", "Microsoft Edge"]
        elif self.platform == "Linux":
            if browser_name in ["chrome", "google chrome"]:
                cmd = ["google-chrome", url] if url else ["google-chrome"]
            elif browser_name in ["firefox", "mozilla"]:
                cmd = ["firefox", url] if url else ["firefox"]
            elif browser_name == "chromium":
                cmd = ["chromium", url] if url else ["chromium"]
            elif browser_name == "edge":
                cmd = ["microsoft-edge", url] if url else ["microsoft-edge"]
        
        if cmd:
            proc = subprocess.Popen(cmd, shell=(self.platform == "Windows"), 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
            self.processes[browser_name] = proc
            return proc.pid
        return None
    
    def close_browser(self, browser_name=None):
        """Close browser(s). If browser_name is None, closes all tracked browsers"""
        if browser_name:
            browser_name = browser_name.lower()
            if browser_name in self.processes:
                proc = self.processes[browser_name]
                if self.platform == "Windows":
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], 
                                 capture_output=True)
                else:
                    proc.terminate()
                del self.processes[browser_name]
        else:
            # Close all browsers
            for name, proc in list(self.processes.items()):
                try:
                    if self.platform == "Windows":
                        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], 
                                     capture_output=True)
                    else:
                        proc.terminate()
                except:
                    pass
            self.processes.clear()


class AppController:
    """Controls application instances"""
    
    def __init__(self):
        self.platform = platform.system()
        self.processes = {}
    
    def open_app(self, app_name, app_path=None, args=None):
        """Open an application"""
        if app_path:
            cmd = [app_path]
        else:
            cmd = self._get_app_command(app_name)
        
        if cmd:
            if isinstance(cmd, str):
                cmd = [cmd]
            if args:
                cmd.extend(args)
            proc = subprocess.Popen(cmd, shell=(self.platform == "Windows"),
                                  stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)
            self.processes[app_name] = proc
            return proc.pid
        return None
    
    def _get_app_command(self, app_name):
        """Get command to open an application"""
        app_name = app_name.lower()
        
        if self.platform == "Windows":
            apps = {
                "calculator": "calc.exe",
                "notepad": "notepad.exe",
                "paint": "mspaint.exe",
                "wordpad": "wordpad.exe",
                "task manager": "taskmgr.exe",
                "control panel": "control.exe",
                "file explorer": "explorer.exe",
                "windows defender": "Windows Defender\shell\Application\mpcmdrun.exe",
            }
        elif self.platform == "Darwin":
            apps = {
                "textedit": "TextEdit",
                "calculator": "Calculator",
                "preview": "Preview",
                "photos": "Photos",
                "music": "Music",
                "reminders": "Reminders",
                "calendar": "Calendar",
            }
        elif self.platform == "Linux":
            apps = {
                "calculator": "gnome-calculator",
                "text editor": "gedit",
                "file manager": "nautilus",
                "terminal": "xterm",
                "system monitor": "gnome-system-monitor",
                "network settings": "nm-connection-editor",
            }
        return apps.get(app_name)
    
    def close_app(self, app_name=None):
        """Close app(s). If app_name is None, closes all tracked apps"""
        if app_name:
            app_name = app_name.lower()
            if app_name in self.processes:
                proc = self.processes[app_name]
                try:
                    proc.terminate()
                except:
                    pass
                del self.processes[app_name]
        else:
            # Close all apps
            for name, proc in list(self.processes.items()):
                try:
                    proc.terminate()
                except:
                    pass
            self.processes.clear()
    
    def list_running_processes(self):
        """List all tracked running processes"""
        running = []
        for name, proc in self.processes.items():
            if proc.poll() is None:  # Still running
                running.append(name)
            else:
                # Process ended but still in dict
                del self.processes[name]
        return running


def main():
    """Main function demonstrating usage"""
    print("="*50)
    print("Browser and App Automation Controller")
    print("="*50)
    
    current_platform = platform.system()
    print(f"\nDetected platform: {current_platform}")
    
    controller = BrowserController()
    app_controller = AppController()
    
    print("\n--- Browser Operations ---")
    
    # Open browsers
    if current_platform == "Windows":
        pid = controller.open_browser("chrome", "https://www.google.com")
        print(f"Opened Chrome (PID: {pid})")
        pid = controller.open_browser("firefox")
        print(f"Opened Firefox (PID: {pid})")
    elif current_platform == "Darwin":
        pid = controller.open_browser("safari", "https://www.apple.com")
        print(f"Opened Safari (PID: {pid})")
        pid = controller.open_browser("chrome", "https://www.google.com")
        print(f"Opened Chrome (PID: {pid})")
    elif current_platform == "Linux":
        pid = controller.open_browser("firefox", "https://www.mozilla.org")
        print(f"Opened Firefox (PID: {pid})")
        pid = controller.open_browser("chromium")
        print(f"Opened Chromium (PID: {pid})")
    
    time.sleep(2)
    
    # Close specific browser
    if current_platform == "Windows":
        controller.close_browser("chrome")
        print("Closed Chrome")
    elif current_platform == "Darwin":
        controller.close_browser("safari")
        print("Closed Safari")
    
    time.sleep(2)
    
    # Close all browsers
    controller.close_browser()
    print("Closed all browsers")
    
    print("\n--- App Operations ---")
    
    # Open apps
    if current_platform == "Windows":
        pid = app_controller.open_app("Calculator", args=["/Scientific"])
        print(f"Opened Calculator (PID: {pid})")
        pid = app_controller.open_app("Notepad")
        print(f"Opened Notepad (PID: {pid})")
    elif current_platform == "Darwin":
        pid = app_controller.open_app("Calculator")
        print(f"Opened Calculator (PID: {pid})")
        pid = app_controller.open_app("TextEdit")
        print(f"Opened TextEdit (PID: {pid})")
    elif current_platform == "Linux":
        pid = app_controller.open_app("Calculator")
        print(f"Opened Calculator (PID: {pid})")
        pid = app_controller.open_app("Terminal")
        print(f"Opened Terminal (PID: {pid})")
    
    time.sleep(2)
    
    # Close specific app
    if platform == "Windows":
        app_controller.close_app("Notepad")
        print("Closed Notepad")
    elif platform == "Darwin":
        app_controller.close_app("TextEdit")
        print("Closed TextEdit")
    
    time.sleep(2)
    
    # Close all apps
    app_controller.close_app()
    print("Closed all apps")
    
    print("\n--- System Process Check ---")
    running = app_controller.list_running_processes()
    print(f"Running tracked processes: {running if running else 'None'}")
    
    running = app_controller.list_running_processes()
    print(f"Running tracked browsers: {running if running else 'None'}")
    
    print("\n" + "="*50)
    print("Automation complete!")
    print("="*50)


if __name__ == "__main__":
    main()