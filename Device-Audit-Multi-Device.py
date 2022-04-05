from paramiko import SSHClient
import paramiko
import csv
import time

#TO-DO#
# Command in the CSV
# Output in Audit folder with device-name and date-time-stamp

paramiko.util.log_to_file("main_paramiko_log.txt", level="INFO")

# open the device list in read mode
filename = open('device_list.csv', 'r')
# creating Dict-reader object
file = csv.DictReader(filename)

errorLog = open("error.txt", "w+")

cmd = "show bootvar"

for col in file:
    filename_postfix = time.strftime("%Y%m%d")
    log_filename = "[" + col['host-name'] + "] [" + col['device-ip'] + "] - " + filename_postfix

    outputFile = open("./logs/" + log_filename + ".log", "a")

    try:
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(col['device-ip'], port=22, username=col['user-name'], password=col['password'])
    except:
        errorLog.write(col['device-ip'] + "\n")
        print(col['device-ip'], "\t: unable to connect")
        continue

    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(col['command'])
    output = ssh_stdout.readlines()

    print(time.strftime("%H:%M:%S - %Y:%m:%d") + " - Output for Device [" + col['host-name'] + " - " + col['device-ip'] + "] \n")
    print("-------------------------------------------------------------------------")

    outputFile.write(time.strftime("%H:%M:%S - %Y:%m:%d") + " - Output for Device [" + col['host-name'] + " - " + col['device-ip'] + "] \n")
    outputFile.write("-------------------------------------------------------------------------")

    for i in output:
        print(i)
        outputFile.write(i + "\n")

    # for i in output:
    #     if "enabled" in i:
    #         print(router, "\t: bash is enabled")
    #         enabledFile.write(router + "\n")
    #     else:
    #         print(router, "\t: bash is disabled")
    #         disabledFile.write(router + "\n")

    client.close()
    outputFile.close()

errorLog.close()
filename.close()