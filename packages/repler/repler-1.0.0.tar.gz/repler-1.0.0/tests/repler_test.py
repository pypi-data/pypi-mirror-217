#############################################
# version 1.0.0                             #
# Reportss handler self test                #
# author: Alexander Barzilai                #
#############################################
import os, sys
from os import listdir
from os.path import isfile, join
from zipfile import ZipFile

import logging as log
import logging.handlers
import random
import time
import shutil
cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(rf"{cwd}\..\src\repler")

def config_logger():
    if not os.path.exists(fr"{cwd}\Logs"):
            os.makedirs(fr"{cwd}\Logs")
    filename = rf'{cwd}\Logs\repler_test.log'
    rotating_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=100000,backupCount=1)
    #file_handler = log.FileHandler(filename=filename)
    stdout_handler = log.StreamHandler(stream=sys.stdout)
    #handlers = [file_handler, stdout_handler, rotating_handler]
    handlers = [stdout_handler, rotating_handler]
    log.basicConfig(
                    encoding='utf-8',
                    level=log.DEBUG, 
                    format='%(asctime)s[%(levelname)-5s] %(module)-15s:%(lineno)-3s %(funcName)-25s -> %(message)s',
                    datefmt='%I:%M:%S',
                    handlers=handlers)

config_logger()

from repler.repler import ReportHandler

class SelfTest(object):
    

    def __init__(self):

        log.info("PIZDETZ")
        self.env_handler = ReportHandler()

        self.pre_test()
        self.test_cleaner_no_age()
       
        self.pre_test()
        self.env_handler._under_clean = []
        self.test_cleaner_age()

        self.pre_test()
        self.env_handler._under_clean = []
        self.env_handler._under_archive = []
        self.test_archive_single_sourse_single_destination_single_name()

        self.pre_test(test_folder="SelfTest1")
        self.pre_test(test_folder="SelfTest2")
        self.env_handler._under_clean = []
        self.env_handler._under_archive = []
        self.test_archive_two_sourse_two_destination_single_name()

        self.pre_test()
        self.env_handler._under_clean = []
        self.env_handler._under_archive = []
        self.test_archive_single_sourse_delete_arch_files()

        self.pre_test(test_folder="SelfTest")
        self.env_handler._under_clean = []
        self.env_handler._under_archive = []
        self.test_clean_and_archive()

        self.pre_test(test_folder="SelfTest")
        self.env_handler._under_clean = []
        self.env_handler._under_archive = []
        self.test_archive_and_clean()

       

    def pre_test(self, test_folder="SelfTest"):
        if not os.path.exists(test_folder):
            os.makedirs(test_folder)
        for ext in ["txt","log","blabla","ttxt"]:
            with open(rf"{test_folder}\file.{ext}", "w") as f:
                f.write(" ")

    def test_cleaner_no_age(self):
        self.test_cleaner(age_before_del_hour=0)
        l = listdir("SelfTest")
        assert "file.blabla" in l
        assert "file.ttxt" in l
        assert "file.txt" not in l
        assert "file.log" not in l

    def test_cleaner_age(self):
        self.test_cleaner(age_before_del_hour=1)
        l = listdir("SelfTest")
        assert "file.blabla" in l
        assert "file.ttxt" in l
        assert "file.txt" in l
        assert "file.log" in l

    def test_cleaner(self,age_before_del_hour):
        self.env_handler.set_cleaner("SelfTest",age_before_del_hour)
        l = listdir("SelfTest")
        for ext in ["txt","log","blabla","ttxt"]:
            assert f"file.{ext}" in l
        self.env_handler.clean()
        
    def test_archive_validate(self):
        
        for a in self.env_handler._under_archive:
            l = listdir(a.sourse_path)
            for ext in ["txt","log","blabla","ttxt"]:
                log.info(f"Cheking extention: '{ext}' in {l}[!n]")
                assert f"file.{ext}" in l
                log.info(" - PASS")              
        self.env_handler.archive()
        l = listdir(a.sourse_path)
        for a in self.env_handler._under_archive:
            zip_name = join(a.archivation_path, a.arch_file_name)
            with ZipFile(zip_name, 'r') as f:
                names = f.namelist()
            assert len(a.ext_to_arch) == len(names)
            for ext in a.ext_to_arch:
                assert f"file.{ext}" in names
                if a.delete_archived_files:
                    assert f"file.{ext}" not in l
                    log.info(f"Cheking extention: '{ext}' not in {l} - PASS")

    def test_archive_single_sourse_single_destination_single_name(self):
        log.info("-----TEST test_archive_single_sourse_single_destination_single_name-----")
        self.env_handler.set_archivator(archive_prefix="archive",
                                        sourse_folder="SelfTest",
                                        archive_folder=r"SelfTest\Archive")
        self.test_archive_validate()

    def test_archive_two_sourse_two_destination_single_name(self):
        log.info("-----TEST test_archive_two_sourse_two_destination_single_name-----")
        self.env_handler.set_archivator(archive_prefix="archive",
                                        sourse_folder="SelfTest1",
                                        archive_folder=r"SelfTest1\Archive1")
        self.env_handler.set_archivator(archive_prefix="archive",
                                        sourse_folder="SelfTest2",
                                        archive_folder=r"SelfTest2\Archive2")
        self.test_archive_validate()
        
    def test_archive_single_sourse_delete_arch_files(self):
        log.info("-----TEST test_archive_single_sourse_delete_arch_files-----")
        self.env_handler.set_archivator(archive_prefix="archive",
                                        sourse_folder="SelfTest",
                                        archive_folder=r"SelfTest\Archive")
        self.env_handler._under_archive[-1].delete_archived_files = True
        self.test_archive_validate()

    def test_clean_and_archive(self):
        log.info("-----TEST test_clean_and_archive-----")
        self.env_handler.set_archivator(archive_prefix="archive",
                                        sourse_folder="SelfTest",
                                        archive_folder=r"SelfTest\Archive")  
        self.env_handler._under_archive[-1].ext_to_arch = ["log"]
        self.env_handler.set_cleaner("SelfTest",age_before_del_hour=0)
        self.test_clean_and_archive_validate()

    def test_archive_and_clean(self):
        log.info("-----TEST test_archive_and_clean-----")
        self.env_handler.set_archivator(archive_prefix="archive",
                                        sourse_folder="SelfTest",
                                        archive_folder=r"SelfTest\Archive")  
        self.env_handler._under_archive[-1].ext_to_arch = ["log"]
        self.env_handler.set_cleaner("SelfTest",age_before_del_hour=0)
        self.test_archive_and_clean_validate()

    def test_archive_and_clean_validate(self):
        for a in self.env_handler._under_archive:
            l = listdir(a.sourse_path)
            for ext in ["txt","log","blabla","ttxt"]:
                assert f"file.{ext}" in l
                log.info(f"Cheking extention: '{ext}' in {l} - PASS")

        self.env_handler.archive()
        
        for arch_obj in self.env_handler._under_archive:
            self._zip_validate(arch_obj)

        l = listdir(a.sourse_path)
        assert "file.log" not in l
        log.info(f"Cheking file.log not_in {l} after archive - PASS")

        self.env_handler.clean()

        l = listdir(a.sourse_path)
        assert "file.txt" not in l
        log.info(f"Cheking file.txt not in {l} after cleaner - PASS")
          

    def test_clean_and_archive_validate(self):
        for a in self.env_handler._under_archive:
            l = listdir(a.sourse_path)
            for ext in ["txt","log","blabla","ttxt"]:
                assert f"file.{ext}" in l
                log.info(f"Cheking extention: '{ext}' in {l} - PASS")

        self.env_handler.clean()
        l = listdir(a.sourse_path)
        assert "file.log" in l
        log.info(f"Cheking file.log in {l} after cleaner - PASS")
        assert "file.txt" not in l
        log.info(f"Cheking file.txt not in {l} after cleaner - PASS")

        self.env_handler.archive()
        
        for arch_obj in self.env_handler._under_archive:
            self._zip_validate(arch_obj)
            
    
    def _zip_validate(self, arch_obj:object) -> None:
        l = listdir(arch_obj.sourse_path)
        zip_name = join(arch_obj.archivation_path, arch_obj.arch_file_name)
        with ZipFile(zip_name, 'r') as f:
            names = f.namelist()
        assert len(arch_obj.ext_to_arch) == len(names)
        for ext in arch_obj.ext_to_arch:
            assert f"file.{ext}" in names
            if arch_obj.delete_archived_files:
                assert f"file.{ext}" not in l
                log.info(f"Cheking extention: '{ext}' not in {l} - PASS")


class RandTest(object):

    def __init__(self,max_run_time_h=None,max_loop_count=None):
        self.max_run_time_h = max_run_time_h
        log.info(f"Maximum running time:{self.max_run_time_h}")
        self.max_loop_count = max_loop_count if max_loop_count else sys.maxsize
        log.info(f"Maximum iteration count:{self.max_loop_count}")
        self.start_time = time.time()
        log.info(f"Start time:{self.start_time}")
        self.report_handler = ReportHandler(log_enable=True)
        #self.is_archivator_already_run = False
        self.main_loop()

    def main_loop(self):
        loop = 0
        while not self.is_time_out() and loop < self.max_loop_count:
            self.clean_pre_test()
            loop+= 1   
            log.info(f"\n\nStart loop #{loop}")
            order:list = self.get_objects_order()
            log.info(f"Order: {order}")
            actions:list = self.get_actions_order()
            log.info(f"Actions: {actions}")
            self.apply_policy(order)
            self.report_handler.show_archivator()
            self.report_handler.show_cleaner()
            self.rand_pre_test()
            self.is_archivator_already_run = False
            for act in actions:
                log.info(f"Current action:{act}")
                expected = self.get_expected_FSM(act)
                log.info(f"Expected results:{expected}")
                if act == "clean":
                    self.report_handler.clean()                   
                else:
                    self.report_handler.archive()                    
                    if self.report_handler._under_archive:
                        # Check if exist at least one archivator.
                        self.is_archivator_already_run = True
                self.verify_expected(act, expected)

    def clean_pre_test(self):
        self.report_handler._under_archive = []
        self.report_handler._under_clean = []
        try:
            shutil.rmtree(rf'{cwd}\RandomTest')
        except:
            pass
        
    
    def rand_pre_test(self):
        log.info(f"Running pretest settings.")
        obj_list:list = []
        obj_list.extend(self.report_handler._under_archive)
        obj_list.extend(self.report_handler._under_clean)
        for o in obj_list:
            if o.__class__.__name__=="Archivator":
                path = o.sourse_path
               # _ext = o.ext_to_arch 
            else:
                path = o.path
               # _ext = o.ext_to_del
            if not os.path.exists(path):
                os.makedirs(path)
            # fill direction with rendom files.
            _ext = self.get_extentions()
            for ext in _ext:
                with open(rf"{path}\file.{ext}", "w") as f:
                    f.write(" ")
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
            log.info(f"Files generated for {path}: {onlyfiles}")
            
    
    def verify_expected(self, act, expected):
        log.info("Verifying results...")
        if act == "clean":
            for c in self.report_handler._under_clean:               
                onlyfiles = [f for f in listdir(c.path) if isfile(join(c.path, f))]
                onlyfiles.sort()
                expected["in_sourse"][c.path].sort()
                assert  onlyfiles == expected["in_sourse"][c.path]
        else:
            for a in self.report_handler._under_archive:               
                onlyfiles = [f for f in listdir(a.sourse_path) if isfile(join(a.sourse_path, f))]
                assert  onlyfiles == expected["in_sourse"][a.sourse_path]
                if expected["in_archive"][a.archivation_path]:
                    with ZipFile(join(a.archivation_path, a.arch_file_name), 'r') as f:
                        names = f.namelist()
                    names.sort()
                    expected["in_archive"][a.archivation_path].sort()
                    assert  names == expected["in_archive"][a.archivation_path]
                else:
                    assert not os.path.isfile(join(a.archivation_path, a.arch_file_name))
        log.info("==========PASS==========")


    def is_time_out(self):
        if self.max_run_time_h:
            return time.time() - self.start_time > self.max_run_time_h * 3600
        return False

    def _is_old(self,f_path, age) -> bool:
        f_age = self._get_file_age_hour(f_path)
        older = self._get_file_age_hour(f_path) >= age
        if older:
            log.info(f"The candidat for delition: {f_path}, age: {f_age}")
        else:
            log.info(f"The candidat for delition: {f_path} is too yong.")
        return older

    def _get_file_age_hour(self, path:str) -> int:       
        st=os.stat(path)
        h = int((time.time()-st.st_mtime) / 3600)
        log.info(f"Age of {path} is {h} hours.")
        return h

    def get_expected_FSM(self, act):
        INIT = "INIT"
        DEFINE_ACTION = "DEFINE_ACTION"
        EXPECT_ARCHIVE = "EXPECT_ARCHIVE"
        EXPECT_CLEAN = "EXPECT_CLEAN"
        EXPECT_CLEAN_AFTER_ARCHIVE = "EXPECT_CLEAN_AFTER_ARCHIVE"
        END = "END"

        next_state = INIT
        log.info("Starting expect results FSM")
        if next_state == INIT:
            log.info(f"--------------FSM state: {next_state}")
            assert act in ["archive", "clean"]
            # Expected files after an action
            expected = {"in_sourse":{}, "in_archive":{}}
            next_state = DEFINE_ACTION
            log.info(f"Next FSM state: {next_state}")
        if next_state == DEFINE_ACTION:
            log.info(f"--------------FSM state: {next_state}")
            if act == "archive":
                next_state = EXPECT_ARCHIVE
            elif act == "clean" and not self.is_archivator_already_run:
                next_state = EXPECT_CLEAN
            elif act == "clean" and self.is_archivator_already_run:
                next_state = EXPECT_CLEAN_AFTER_ARCHIVE
            else:
                raise Exception("Undefined action condition!")
            log.info(f"Next FSM state: {next_state}")
        if next_state == EXPECT_ARCHIVE:
            log.info(f"--------------FSM state: {next_state}")
            #clean_sourse = self.get_clean_sourses()
            for a in self.report_handler._under_archive:
                expected["in_archive"][a.archivation_path] = []
                onlyfiles = [f for f in listdir(a.sourse_path) if isfile(join(a.sourse_path, f))]
                expected["in_sourse"][a.sourse_path] = onlyfiles
                # Deside if the file should be archived
                for ext in a.ext_to_arch:
                    for f in onlyfiles:
                        if f.endswith(f".{ext}"):
                            expected["in_archive"][a.archivation_path].append(f)
                            if a.delete_archived_files:
                                expected["in_sourse"][a.sourse_path].remove(f)                
                if a.postpone_clean:
                    for c in self.report_handler._under_clean:
                        if c.path == a.sourse_path:
                            for ext in c.ext_to_del:
                                for f in onlyfiles:
                                    if f.endswith(f".{ext}") and self._is_old(join(c.path, f), c.age_before_del_hour):                                                                             
                                        expected["in_sourse"][a.sourse_path].remove(f)           
            next_state = END
            log.info(f"Next FSM state: {next_state}")
        if next_state == EXPECT_CLEAN:
            log.info(f"--------------FSM state: {next_state}")
            arc_sourse = self.get_archive_sourses()
            for c in self.report_handler._under_clean: 
                #expected["in_sourse"][c.path] = self.clean_extentions(c)
                onlyfiles = [f for f in listdir(c.path) if isfile(join(c.path, f))]
                expected["in_sourse"][c.path] = onlyfiles                
                for ext in c.ext_to_del:
                    for f in onlyfiles:
                        if c.path not in arc_sourse and f.endswith(f".{ext}"):
                             # no archivator defined on c.path
                            if self._is_old(join(c.path, f), c.age_before_del_hour):
                                expected["in_sourse"][c.path].remove(f)
            next_state = END
            log.info(f"Next FSM state: {next_state}")
        if next_state == EXPECT_CLEAN_AFTER_ARCHIVE:
            log.info(f"--------------FSM state: {next_state}")
            arc_sourse = self.get_archive_sourses()
            for c in self.report_handler._under_clean:
                expected["in_sourse"][c.path] = self.clean_extentions(c)                    
            next_state = END
            log.info(f"Next FSM state: {next_state}")
        if next_state == END:
            log.info(f"--------------FSM state: {next_state}")
            return expected

    def clean_extentions(self, c:object)->list:      
        onlyfiles = [f for f in listdir(c.path) if isfile(join(c.path, f))]
        expected = list(onlyfiles)               
        for ext in c.ext_to_del:
            for f in onlyfiles:
                if f.endswith(f".{ext}") and self._is_old(join(c.path, f), c.age_before_del_hour):
                    expected.remove(f)
        return expected

    def get_archive_sourses(self)-> list:
        arcs = self.report_handler._under_archive
        arc_sourse = [a.sourse_path for a in arcs]
        return arc_sourse

    def get_clean_sourses(self)-> list:
        clean = self.report_handler._under_clean
        clean_sourse = [c.path for c in clean]
        return clean_sourse 

    def apply_policy(self, order):
        log.info("Applying policys on folders.")
        for o in order:
            if o == "cleaner":
                folder_path = self.get_cleaner_folder_path()
                age_before_del_hour = self.get_age_before_del_hour()
                extentions = self.get_extentions()
                result = self.report_handler.set_cleaner(folder_path=folder_path,
                                                         age_before_del_hour=age_before_del_hour,
                                                         ext_to_del=extentions)
            else:
                sourse_folder = self.get_sourse_folder()
                archive_folder = rf"{sourse_folder}\Archive"
                archive_prefix = self.get_archive_prefix()
                ext_to_arch = self.get_extentions()
                delete_archived_files = self.get_delete_archived_files()
                result = self.report_handler.set_archivator(sourse_folder=sourse_folder,
                                                            archive_folder=archive_folder,
                                                            archive_prefix=archive_prefix,
                                                            ext_to_arch=ext_to_arch,
                                                            delete_archived_files=delete_archived_files)
                if result:
              
                    log.info(f"Aplying archivator on {sourse_folder}")
                    log.info(f"\tCreate archive in {archive_folder}")
                    log.info(f"\tArchive prefix: {archive_prefix}")
                    log.info(f"\tExtentions to archive: {self.report_handler._under_archive[-1].ext_to_arch}")
                    log.info(f"\tDelete archived files after succefull archivation:\
                    {self.report_handler._under_archive[-1].delete_archived_files}")

    def get_objects_order(self):
        policy_list = ["cleaner","archivator"]
        order = []
        length = random.randint(1,5)
        for _ in range(0,length):
            obj = random.choice(policy_list)
            order.append(obj)
        return order

    def get_delete_archived_files(self):
        return random.choice([True, False])

    def get_extentions(self):
        l = ["log", "txt", "zzz", "yyy"]
        n = random.randint(1,len(l))
        ext_list = random.sample(l, n)
        return ext_list

    def get_actions_order(self):
        return random.choice([("clean", "archive"),
                              ("archive", "clean"),
                              ("clean",),
                              ("archive",)])

    def get_path(self):
        l = ["SelfTest", "SelfTest1", "SelfTest2"]
        path = random.choice(l)
        return path

    def get_cleaner_folder_path(self):
        path = self.get_path()
        return rf"{cwd}\RandomTest\{path}"

    def get_age_before_del_hour(self):
        age = random.choice([0, 1])
        return age

    def get_sourse_folder(self):
        path = self.get_path()
        return rf"{cwd}\RandomTest\{path}"

    
    def get_archive_prefix(self):
        return "archive"




def self_test():
    SelfTest()
    print("\nSelf test - PASS.")

def rendom_test():
    log.info("Start random test.")
    RandTest()
    print("\nRandom test finished.")


if __name__ == "__main__":
    #self_test()
    rendom_test()


