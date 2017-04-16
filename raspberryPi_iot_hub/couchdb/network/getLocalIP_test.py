from subprocess import check_output

localIP = check_output(['hostname', '-I'])

print localIP