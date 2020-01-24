import subprocess

def wifi_status():
    ps = subprocess.Popen(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
        print(output)
        return True
    except subprocess.CalledProcessError:
        # grep did not match any lines
        print("No wireless networks connected")
        return False