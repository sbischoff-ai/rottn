# -*- coding: utf-8 -*-
'''
A module that helps with running and maintaining bossfight.server processes.
'''

import threading
import subprocess
import netifaces
import bossfight.client.config as config

_RUNNING_PROCESSES = {}
_UPDATE_THREAD = threading.Thread()

def get_running_processes():
    '''
    Returns an iterable list of *pid*s of running server processes.
    '''
    return list(_RUNNING_PROCESSES.keys()).copy()

def _update_processes():
    while _RUNNING_PROCESSES:
        for pid in get_running_processes():
            try:
                if _RUNNING_PROCESSES[pid]['process'].wait(timeout=0.3) is not None:
                    del _RUNNING_PROCESSES[pid]
            except (subprocess.TimeoutExpired, KeyError):
                pass

def get_available_ip_addresses():
    '''
    Returns a list of all available IP addresses that the server can be bound to.
    Keep in mind that `127.0.0.1` is only suitable for local servers.
    '''
    addresses = []
    for interface in netifaces.interfaces():
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                addresses.append(link['addr'])
    addresses.reverse()
    return addresses

def run_server(ip_address='localhost', port=0):
    '''
    Starts a server bound to the specified address and return the process ID.
    '''
    global _UPDATE_THREAD
    cmd = config.get.local_server_exec.copy()
    cmd.extend([ip_address, str(port)])
    server_process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE
    )
    _RUNNING_PROCESSES[server_process.pid] = {
        'process': server_process,
        'ip_address': str(server_process.stdout.readline(), 'utf-8').strip(),
        'port': int(server_process.stdout.readline())
    }
    if not _UPDATE_THREAD.is_alive():
        _UPDATE_THREAD = threading.Thread(target=_update_processes)
        _UPDATE_THREAD.start()
    return server_process.pid

def get_ip_address(pid):
    '''
    Returns the the IP address of the server running under ther process ID *pid*.
    '''
    return _RUNNING_PROCESSES[pid]['ip_address']

def get_port(pid):
    '''
    Returns the the port of the server running under ther process ID *pid*.
    '''
    return _RUNNING_PROCESSES[pid]['port']

def shutdown(pid):
    '''
    Terminates the server process with process ID *pid*.
    '''
    _RUNNING_PROCESSES[pid]['process'].terminate()
    del _RUNNING_PROCESSES[pid]

def clean_up():
    '''
    Terminates all running server processes.
    '''
    for pid in get_running_processes():
        shutdown(pid)