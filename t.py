import subprocess

def compile_java(java_file):
    cmd ='javac ' + java_file+'.java'
    proc = subprocess.Popen(cmd, shell=True)

def run_java(java_file, args):
    cmd = 'java ' + java_file +' ' + args
    proc = subprocess.Popen(cmd, shell=True)

compile_java("tw")
run_java("tw", "Donald")