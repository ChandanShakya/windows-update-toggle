import tkinter as tk
from tkinter import messagebox, ttk
import os
import ctypes
import subprocess
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

class WindowsUpdateToggle:
    def __init__(self, root):
        self.root = root
        root.title("Windows Update Toggle")
        root.geometry("400x250")
        root.resizable(False, False)
        
        # Style configuration
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 12, 'bold'))
        
        # Main frame
        mainframe = ttk.Frame(root, padding="20")
        mainframe.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(mainframe, text="Windows Update Controller", style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status display
        self.status_var = tk.StringVar()
        self.update_status()
        ttk.Label(mainframe, text="Current Status:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(mainframe, textvariable=self.status_var, foreground='blue').grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        ttk.Button(mainframe, text="Disable Windows Updates", command=self.disable_updates).grid(row=2, column=0, columnspan=2, pady=10, ipadx=10, ipady=5, sticky=tk.EW)
        ttk.Button(mainframe, text="Enable Windows Updates", command=self.enable_updates).grid(row=3, column=0, columnspan=2, pady=10, ipadx=10, ipady=5, sticky=tk.EW)
        
        # Advanced options
        self.remove_restart_var = tk.IntVar(value=1)
        ttk.Checkbutton(mainframe, text="Remove 'Update and restart' option", variable=self.remove_restart_var).grid(row=4, column=0, columnspan=2, pady=(15, 5), sticky=tk.W)
        
        # Footer
        ttk.Label(mainframe, text="Requires administrator privileges", foreground='gray').grid(row=5, column=0, columnspan=2, pady=(15, 0))
    
    def update_status(self):
        try:
            result = subprocess.run(
                ['reg', 'query', r'HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU', '/v', 'NoAutoUpdate'],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            if "0x1" in result.stdout:
                self.status_var.set("Updates DISABLED")
            else:
                self.status_var.set("Updates ENABLED")
        except:
            self.status_var.set("Status unknown")
    
    def disable_updates(self):
        try:
            # Disable automatic updates
            subprocess.run(
                ['reg', 'add', r'HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU', '/v', 'NoAutoUpdate', '/t', 'REG_DWORD', '/d', '1', '/f'],
                check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            subprocess.run(
                ['reg', 'add', r'HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU', '/v', 'AUOptions', '/t', 'REG_DWORD', '/d', '1', '/f'],
                check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if self.remove_restart_var.get():
                # Remove "Update and restart" option
                subprocess.run(
                    ['reg', 'add', r'HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate', '/v', 'DisableOSUpgrade', '/t', 'REG_DWORD', '/d', '1', '/f'],
                    check=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                subprocess.run(
                    ['reg', 'add', r'HKLM\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings', '/v', 'UxOption', '/t', 'REG_DWORD', '/d', '1', '/f'],
                    check=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
            
            # Stop Windows Update service
            subprocess.run(
                ['net', 'stop', 'wuauserv', '/y'],
                check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            subprocess.run(
                ['sc', 'config', 'wuauserv', 'start=', 'disabled'],
                check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            self.update_status()
            messagebox.showinfo("Success", "Windows Updates have been disabled successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to disable updates:\n{e}")
    
    def enable_updates(self):
        try:
            # Enable automatic updates
            subprocess.run(
                ['reg', 'delete', r'HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU', '/f'],
                check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            subprocess.run(
                ['reg', 'delete', r'HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate', '/v', 'DisableOSUpgrade', '/f'],
                check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            subprocess.run(
                ['reg', 'delete', r'HKLM\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings', '/v', 'UxOption', '/f'],
                check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Start Windows Update service
            subprocess.run(
                ['sc', 'config', 'wuauserv', 'start=', 'auto'],
                check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            subprocess.run(
                ['net', 'start', 'wuauserv'],
                check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            self.update_status()
            messagebox.showinfo("Success", "Windows Updates have been enabled successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to enable updates:\n{e}")

if __name__ == "__main__":
    run_as_admin()
    root = tk.Tk()
    app = WindowsUpdateToggle(root)
    root.mainloop()
