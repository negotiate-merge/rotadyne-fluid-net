import subprocess
import config

user = config.r_user
host = config.cloud_server
k = config.r_key_path

stop = 'sudo systemctl stop pump-controller'
start = 'sudo systemctl start pump-controller'
status = 'sudo systemctl status pump-controller'

def send(action):
	sp = subprocess.Popen(["ssh", "-i", k, "-p", "22", user + "@" + host, action],
					shell=True, 
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE)
	
	stdout, stderr = sp.communicate()

	# print(f"stdout: {stdout.decode('utf-8')}\n\nstderr: {stderr.decode('utf-8')}")

	if 'status' in action:
		if "Active: active" in stdout.decode('utf-8'): 
			# print("Active")
			return True
		if "Active: inactive" in stdout.decode('utf-8'): 
			# print("Inactive")
			return False
	


''' Useful for debugging
try:
    out = subprocess.check_output(["ssh", "-i", "C:\\Users\\nigel\\.ssh\\google_compute_engine", "-p", "22", "{}@{}".format(user, host), command])
    print(out)
except CalledProcessError as e:
    pass
'''