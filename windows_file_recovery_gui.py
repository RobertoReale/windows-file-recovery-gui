import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import os
import win32api
import ctypes

class WindowsFileRecoveryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows File Recovery")
        self.root.geometry("900x750")
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create main tabs
        self.main_tab = ttk.Frame(self.notebook)
        self.help_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.main_tab, text='Recovery Tool')
        self.notebook.add(self.help_tab, text='Guide & Help')
        
        # Setup main recovery interface
        self.setup_recovery_interface()
        
        # Setup help interface
        self.setup_help_interface()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_recovery_interface(self):
        # Drive Selection Frame
        drive_frame = ttk.LabelFrame(self.main_tab, text="Step 1: Select Drives", padding="10")
        drive_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Get available drives
        drives = self.get_available_drives()
        
        # Source Drive
        ttk.Label(drive_frame, text="Source Drive (where files were lost):").pack(anchor=tk.W)
        self.source_drive = ttk.Combobox(drive_frame, values=drives)
        self.source_drive.pack(fill=tk.X, pady=(0,10))
        
        # Destination Drive
        ttk.Label(drive_frame, text="Destination Drive (where to save recovered files):").pack(anchor=tk.W)
        self.dest_drive = ttk.Combobox(drive_frame, values=drives)
        self.dest_drive.pack(fill=tk.X)
        ttk.Label(drive_frame, text="Note: Source and destination drives must be different!", 
                 foreground="red").pack(anchor=tk.W)

        # Recovery Mode Frame
        mode_frame = ttk.LabelFrame(self.main_tab, text="Step 2: Select Recovery Mode", padding="10")
        mode_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Mode selection
        self.recovery_mode = tk.StringVar(value="regular")
        
        ttk.Radiobutton(mode_frame, text="Regular Mode - For recently deleted files on NTFS drives", 
                       variable=self.recovery_mode, value="regular").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Extensive Mode - For older deleted files or formatted drives", 
                       variable=self.recovery_mode, value="extensive").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Segment Mode - For NTFS drives using file record segments", 
                       variable=self.recovery_mode, value="segment").pack(anchor=tk.W)

        # File Options Frame
        file_frame = ttk.LabelFrame(self.main_tab, text="Step 3: Specify File Details (Optional)", padding="10")
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # File Type
        ttk.Label(file_frame, text="File Type (e.g., pdf, docx, jpg):").pack(anchor=tk.W)
        self.file_type = ttk.Entry(file_frame)
        self.file_type.pack(fill=tk.X, pady=(0,10))
        
        # File Path
        ttk.Label(file_frame, text="Path where files were deleted from:").pack(anchor=tk.W)
        path_frame = ttk.Frame(file_frame)
        path_frame.pack(fill=tk.X, pady=(0,5))
        
        self.file_path = ttk.Entry(path_frame)
        self.file_path.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        ttk.Button(path_frame, text="Browse...", command=self.browse_path).pack(side=tk.LEFT, padx=(5,0))

        # Command Frame
        cmd_frame = ttk.LabelFrame(self.main_tab, text="Step 4: Generate and Execute Command", padding="10")
        cmd_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(cmd_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Generate Command", 
                  command=self.generate_command).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Execute Recovery", 
                  command=self.execute_command).pack(side=tk.LEFT)
        
        # Command Output
        ttk.Label(cmd_frame, text="Generated Command:").pack(anchor=tk.W)
        self.command_output = scrolledtext.ScrolledText(cmd_frame, height=3, wrap=tk.WORD)
        self.command_output.pack(fill=tk.X)

    def setup_help_interface(self):
        help_text = """Windows File Recovery Guide

Important Notes:
- You must run this application as administrator
- The tool can recover files from your local storage (internal drives, external drives, and USB devices)
- Recovery from cloud storage and network shares is not supported
- To increase recovery chances, minimize computer usage after file deletion

File System Support:
- NTFS: Most Windows computers (Regular, Extensive, and Segment modes supported)
- FAT and exFAT: USB drives < 4GB (Extensive mode only)

When to Use Each Mode:
1. Regular Mode:
   - Best for recently deleted files
   - Works only with NTFS drives
   - Fastest recovery option

2. Extensive Mode:
   - For older deleted files
   - Works with all file systems
   - Use after formatting a drive
   - More thorough but slower

3. Segment Mode:
   - Specifically for NTFS drives
   - Uses file record segments
   - Good for recovering specific file types

Best Practices:
- Always recover to a different drive than the source
- Don't create new files on the source drive before recovery
- Start with Regular mode for recent deletions
- Try Extensive mode if Regular mode doesn't find your files
- Use specific file types or paths to narrow down the search
"""
        help_scroll = scrolledtext.ScrolledText(self.help_tab, wrap=tk.WORD)
        help_scroll.pack(expand=True, fill='both', padx=10, pady=5)
        help_scroll.insert(tk.END, help_text)
        help_scroll.configure(state='disabled')

    def get_available_drives(self):
        drives = []
        for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
            drives.append(drive.strip('\\'))
        return drives

    def generate_command(self):
        try:
            source = self.source_drive.get()
            dest = self.dest_drive.get()
            
            if not source or not dest:
                messagebox.showerror("Error", "Please select both source and destination drives")
                return
                
            if source == dest:
                messagebox.showerror("Error", "Source and destination drives must be different")
                return
            
            # Build command
            command = f"winfr {source} {dest}"
            
            # Add mode
            mode = self.recovery_mode.get()
            command += f" /{mode}"
            
            # Add file type filter if specified
            if self.file_type.get().strip():
                command += f" /n *.{self.file_type.get().strip()}"
            
            # Add file path if specified
            if self.file_path.get().strip():
                path = self.file_path.get().strip()
                command += f' /n "{path}"'
            
            self.command_output.delete(1.0, tk.END)
            self.command_output.insert(tk.END, command)
            self.status_var.set("Command generated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating command: {str(e)}")
            self.status_var.set("Error generating command")

    def execute_command(self):
        command = self.command_output.get(1.0, tk.END).strip()
        if not command:
            messagebox.showerror("Error", "Please generate a command first")
            return
            
        try:
            # Check if running as administrator
            if not self.is_admin():
                messagebox.showerror("Error", 
                    "This program needs to be run as administrator to execute commands.\n"
                    "Please restart the application as administrator.")
                return
                
            # Confirm execution
            if not messagebox.askyesno("Confirm", 
                "Are you sure you want to start the recovery process?\n\n"
                "Note: This might take a while depending on the drive size and recovery mode."):
                return
                
            # Execute command
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo("Success", 
                    "Recovery process started successfully\n" + result.stdout)
                self.status_var.set("Recovery process started")
            else:
                messagebox.showerror("Error", 
                    f"Error executing command:\n{result.stderr}")
                self.status_var.set("Error executing command")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error executing command: {str(e)}")
            self.status_var.set("Error executing command")

    def browse_path(self):
        # Get the currently selected source drive
        source_drive = self.source_drive.get()
        if not source_drive:
            messagebox.showerror("Error", "Please select a source drive first")
            return
            
        # Set initial directory to the selected drive
        initial_dir = source_drive + "\\"
        
        # Open folder selection dialog
        folder_path = filedialog.askdirectory(
            initialdir=initial_dir,
            title="Select the folder where files were deleted from"
        )
        
        # Update entry if a folder was selected
        if folder_path:
            # Convert to Windows path format
            folder_path = folder_path.replace("/", "\\")
            self.file_path.delete(0, tk.END)
            self.file_path.insert(0, folder_path)

    def is_admin(self):
        try:
            return os.getuid() == 0
        except AttributeError:
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

def main():
    root = tk.Tk()
    app = WindowsFileRecoveryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
