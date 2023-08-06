import os
import platform
import subprocess
import zipfile

class AndroidSdkPlatformTools:
    def __init__(self, base_directory):
        super().__init__()
        self.base_directory = base_directory
        self.device = None
        self.ip = None

        if not os.path.exists(f"{self.base_directory}/platform-tools"):
            if platform.system() == 'Darwin': #맥
                from_zip = f"{self.base_directory}/platform-tools_r34.0.3-darwin.zip"
            elif platform.system() == 'Windows': #윈도우
                from_zip = f"{self.base_directory}/platform-tools_r34.0.3-windows.zip"
            elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
                from_zip = f"{self.base_directory}/platform-tools_r34.0.3-linux.zip"
            zip_file = zipfile.ZipFile(from_zip)
            zip_file.extractall(self.base_directory)
            zip_file.close()
        
    def check_devices(self):    
        cmd = f"{self.base_directory}/platform-tools/adb"
        outputs = subprocess.check_output([cmd, "devices"]).decode('utf-8')
        device = None
        for output in outputs.split("\n")[1:]:
            output = output.strip()
            #print(output) #R95RB00QRCY     device
            if output:
                output = output.split("\t")[0]
                device = output
                break
        self.device = device
        if device:
            return [device]
        else:
            return []
    
    def data_disable(self):
        cmd = f"{self.base_directory}/platform-tools/adb -s {self.device} shell svc data disable"
        os.system(cmd)

    def data_enable(self):
        cmd = f"{self.base_directory}/platform-tools/adb -s {self.device} shell svc data enable"
        os.system(cmd)
