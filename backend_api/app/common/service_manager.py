from backend_api.app import logger
from backend_api.app.models.error_schema import ErrorObject
import subprocess
import os
import psutil
import time

class ServiceManager():
    def __init__(self, module_name):
        self.module_name = module_name

    def start_service(self, id, file_name):
        try:
            # subprocess.Popen(["cd", "{0}/{1}".format(str(os.getcwd()), self.module_name), "&&", 
            #     str(file_name), str(id)], shell=True)
            subprocess.Popen(["cd", str(os.getcwd()), "&&", "python",
                str(file_name), str(id)], shell=True)
            return True
        except Exception as err:
            logger.log("Encountered error : %s" % (err), log_type='ERROR')
            raise ValueError(ErrorObject(type="ServiceError", message="Error encountered while executing the service").to_json())

    def stop_service(self, pid=None):
        try:
            process = subprocess.check_output(["taskkill", "/PID", str(pid) ,"/F"])
            return process.decode('utf-8')
        except subprocess.CalledProcessError as called_error:
            logger.log("Encountered error : %s" % (called_error), log_type='ERROR')
            raise ValueError(ErrorObject(type="ServiceError", message="No tasks are running which match the specified criteria.").to_json())
        except Exception as err:
            logger.log("Encountered error : %s" % (err), log_type='ERROR')
            raise ValueError(ErrorObject(type="ServiceError", message="No tasks are running which match the specified criteria.").to_json())

    def check_service(self, pid=None, file_name=None):
        try:
            if pid is not None:
                #PROD
                # file_name = str(file_name).replace(".lnk", "")
                # tasklist = subprocess.check_output(['tasklist','/svc','/fi'
                #     ,"ImageName eq {0}".format(file_name),'/fi',"pid eq %s" % pid])
                #DEV
                tasklist = subprocess.check_output(['tasklist','/svc','/fi'
                    ,"ImageName eq python.exe",'/fi',"pid eq %s" % pid])
                    
                time.sleep(2)

                return tasklist
        except Exception as err:
            logger.log("Encountered error : %s" % (err), log_type='ERROR')
            raise ValueError(ErrorObject(type="ServiceError", message="Encountered error while checking the service").to_json())

    def is_pid_running(self, id ,pid, services):
        # check if pid exists
        if psutil.pid_exists(pid):
            process = psutil.Process(pid)
            if process:
                if process.name() == 'worker.exe' and (process.cmdline()[1] and process.cmdline()[1] in services):
                    return True
        # if pid does not exist, check if command exists
        for process in psutil.process_iter():
            try:
                if len(process.cmdline()) == 3:
                    if process.name() == 'worker.exe' and (process.cmdline()[1] and process.cmdline()[1] in services) and process.cmdline()[2] == id:
                        if process.pid != os.getpid():
                            self.save_pid(process.pid)
                            return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return False

    def restart_service(self, data, file):
        try:
            for service in data:
                service_tasklist = self.check_service(service['pid'], file)
                if 'image name' in str(service_tasklist.decode("utf-8")).lower():
                    pass
                else:
                    self.start_service(service['id'], file)
                    logger.log("Restarting the service: %s" % (service['id']))
        except Exception as err:
            return err
        