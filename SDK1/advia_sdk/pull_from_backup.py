
import os
import shutil
import time

PROXY_BACKUP =r"C:\Users\WIN11 24H2\Desktop\Atomwalk\Advia_Interface\advia_proxy\backup"
SDK_INPUT =r"C:\Users\WIN11 24H2\Desktop\Atomwalk\Advia_Interface\SDK\input_files"
PROXY_PROCESSED =r"C:\Users\WIN11 24H2\Desktop\Atomwalk\Advia_Interface\advia_proxy\processed"

os.makedirs(SDK_INPUT, exist_ok=True)
os.makedirs(PROXY_PROCESSED, exist_ok=True)

def pull_from_proxy():
    try:
        print(f"Looking for .astm files in: {PROXY_BACKUP}")
        files = [f for f in os.listdir(PROXY_BACKUP) if f.endswith(".astm")]
        print(f"Found files: {files}")

        for filename in files:
            src = os.path.join(PROXY_BACKUP, filename)
            dst = os.path.join(SDK_INPUT, filename)
            archive = os.path.join(PROXY_PROCESSED, filename)

            print(f"Processing {filename}:")
            print(f"  Source:      {src}")
            print(f"  Destination: {dst}")
            print(f"  Archive:     {archive}")

            if not os.path.exists(dst):
                shutil.copy(src, dst)
                print(f"✅ Copied {filename} to SDK input")
            else:
                print(f"⚠️ Skipped {filename} (already exists in SDK input)")

            shutil.move(src, archive)
            print(f"📁 Archived {filename} to proxy processed folder")
    except Exception as e:
        print(f"❌ Error in pull_from_proxy: {e}")

if __name__ == "__main__":
    print(">>> About to call pull_from_proxy()")
    pull_from_proxy()
    print(">>> Finished pull_from_proxy(), about to start SDK")
    # Assuming start_sdk() is defined elsewhere or will be added.
    # For now, just adding the print to match the new_code.
    # result = start_sdk()
        
