#############################################
# Copyright (c) [2023] [Alexander Barzilai] #
# MIT License                               #
# version 1.0.0                             #
# Reports handler                           #
# author: Alexander Barzilai                #
#############################################
import os
from os import listdir
from os.path import isfile, join
import time 
from zipfile import ZipFile
from os.path import basename
import logging


class Log(object): 
    """
    Logging disable\enable mechanism of the tool
    """
    def __init__(self,log_enable):
        self.log_enable = log_enable
    def info(self,msg):
        if self.log_enable:
            return logging.info(msg)
        else:
            return None
    def error(self,msg):
        if self.log_enable:
            return logging.error(msg)
        else:
            return None

# log of the tool
log = None
    
class Cleaner(object):
    """
    Class Cleaner defines wich files and how will be cleaned from directory.
    Rules:
    1) The cleaner has single sourse directory.
    2) The cleaner will delete a file that has extentions from self.ext_to_del
    3) The cleaner will delete a file that has an age >= self.age_before_del_hour
    4) If the cleaner and some archivator have same sourse dir. The cleaner postpone file deletion
        after the archivation.
    """
    def __init__(self,path:str,age_before_del_hour:int,ext_to_del:list) -> None:
        super(Cleaner,self).__init__()
        # Default extentions to be cleaned from defined dir.
        self.ext_to_del = ext_to_del
        # Directory path of defined cleaner.
        self.path = os.path.realpath(path)
        # The files older than 'age_before_del_hour' will be deleted by the cleaner.
        self.age_before_del_hour = age_before_del_hour

    def delete_files(self,extentions:list) -> None:
        """
        Deal with all files with listed extentions. 
        @: extentions - list of extentions to delete.
        """
        # get list of file names from the directory
        onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        for f in onlyfiles:
            for ext in extentions:
                # Check if the file fit by the extention and the age.
                f_path = join(self.path, f)
                if f.endswith(f".{ext}") and self._is_old(f_path):
                    log.info(f"Deletting {f_path}...")
                    os.remove(f_path)

    def _is_old(self, f_path) -> bool:
        return self._get_file_age_hour(f_path) >= self.age_before_del_hour

    def _get_file_age_hour(self, path:str) -> int:       
        st=os.stat(path)
        h = int((time.time()-st.st_mtime) / 3600)
        return h


class Archivator(object):
    """
    class Archivator defines wich files and how will be archived in directory.
    Rules:
    1) The archivator has single sourse directory.
    2) The archivator has single destination (archive) directory.
    3) The archivator will archive a file that has extentions from self.ext_to_arch
    4) The archivator will delete a file after successfull archivation
        if self.delete_archived_files = True
    5) If the archivator and some cleaner have same sourse dir,
        the archivator will run the cleaner if self.postpone_clean == True 
    6) The archive name is self.archive_prefix + time.time()
    """
    def __init__(self,archive_prefix,sourse_folder,archive_folder,ext_to_arch,delete_archived_files) -> None:
        super(Archivator,self).__init__()
        # Flag. After successfull archive creation delete archived files.
        self.delete_archived_files = delete_archived_files
        # Flag. If need to clean archive sourse after archivation.
        #  Will set by the cleaner with the same sourse dir. 
        self.postpone_clean = False
        # Flag.
        self.archivator_finished = False
        # Used in archive name creation archive_prefix + time.time()
        self.archive_prefix = archive_prefix
        # Name of last created archive. 
        self.arch_file_name = ""
        # Default extentions to be archived from defined dir.
        self.ext_to_arch = ext_to_arch
        # File age threshold. Older files will be cleaned.
        self.ege_before_del_hour = 24
        # Path of the folder to be archived.
        self.sourse_path = os.path.realpath(sourse_folder)
        # Path of the folder that includes an archive.
        self.archivation_path = os.path.realpath(archive_folder)
    
    def archive_files(self) -> bool:
        """
        Archive files with defined extentions.
        """
        zip_run_staus = False
        zip_created = False
        arch_file_name = self.archive_prefix + "_" + str(time.time()) + ".zip"
        arch_file_full_path = join(self.archivation_path, arch_file_name)
        try:
            with ZipFile(arch_file_full_path, 'w') as zipObj:
               # Iterate over all the files in directory
               for folderName, _ , filenames in os.walk(self.sourse_path):
                   for filename in filenames:
                       for ext in self.ext_to_arch:
                           if filename.endswith(f".{ext}"):
                               # Create complete filepath of file in directory
                               filePath = os.path.join(folderName, filename)
                               # Add file to zip
                               zipObj.write(filePath, basename(filePath))
                               zip_created = True
                               if self.delete_archived_files:
                                   os.remove(filePath)
            if not zip_created:
                os.remove(arch_file_full_path)
            zip_run_staus = True
            self.arch_file_name = arch_file_name
            log.info(f"Created zip file: {arch_file_full_path}")
        except Exception as e:
            log.error("FAIL: ZIP archive creation failed!")
            raise Exception(e)
        return zip_run_staus


class ReportHandler(object):
    """
    Class defines clean and archive policies on the folders.
    """
    def __init__(self, log_enable=False) -> None:
        global log
        log = Log(log_enable)
        super(ReportHandler,self).__init__()
        # List of folder objects to be cleaned.
        self._under_clean = []
        # List of folder objects to be archived. 
        self._under_archive = []

    def set_log_on(self):
        global log
        log = Log(log_enable=True)

    def set_cleaner(self, folder_path:str,age_before_del_hour:int,ext_to_del=["log", "txt"]) -> bool:
        """
        Define clean policy on direction.
        The files of specified extentions will be deleted in 'folder_path'.
        @: folder_path - The path of 'under cleaned' folder.
        @: age_before_del_hour - The age threshold, older files will be deleted.
        @: return True if creates new cleaner.
        """
        for c in self._under_clean:
            # The folder may has only single cleaner. Saved last settings only.
            if os.path.realpath(folder_path) == c.path:
                log.info(f"The cleaner with path {folder_path} allready exist.")
                if c.ext_to_del != ext_to_del:
                    log.info(f"\tUpdating ext_to_del = {ext_to_del}.")
                    c.ext_to_del = ext_to_del
                if c.age_before_del_hour != age_before_del_hour:
                    log.info(f"\tUpdating age_before_del_hour = {age_before_del_hour}.")
                    c.age_before_del_hour = age_before_del_hour
                # New cleaner wasn't created.
                return False
        # Add new cleaner object to the list
        self._under_clean.append(Cleaner(folder_path,age_before_del_hour,ext_to_del))
        log.info(f"Aplying cleaner on {folder_path}")
        log.info(f"\tage_before_del_hour: {age_before_del_hour}")
        log.info(f"\tExtention to delete: {ext_to_del}")
        # New cleaner was created.
        return True

    def show_cleaner(self) -> None:
        """
        Print list of directories with defined cleaners.
        """
        for c in self._under_clean:
            log.info(f"============================================")
            log.info(f"Cleaner #{self._under_clean.index(c) + 1}")
            log.info(f"\tPath: {c.path}")
            log.info(f"\tage_before_del_hour: {c.age_before_del_hour}")
            log.info(f"\text_to_del: {c.ext_to_del}")

    def set_archivator(self,archive_prefix,sourse_folder,archive_folder,ext_to_arch=["log", "txt"],delete_archived_files=True) -> None:
        """
        The files of specified extentions from 'sourse_folder 
        will be archived in 'archive_folder'.
        @: archivator_name - The prefix of zip file name.
        @: sourse_folder   - The path of 'under archive' folder.
        @: archive_folder  - The path of archive folder.
        @: ext_to_arch - Extentions tobe archived.
        @: delete_archived_files - delete file aftersuccessfull activation.
        """
        if not os.path.exists(archive_folder):       
            os.makedirs(archive_folder)
        for a in self._under_archive:
            # The directory may has single archivator only
            if os.path.realpath(sourse_folder) == a.sourse_path:
                log.info(f"The archivator with sourse path {sourse_folder} allready exist.")
                if a.archive_prefix != archive_prefix:
                    log.info(f"Updating archive_prefix = {archive_prefix}")
                    a.archive_prefix == archive_prefix
                if a.archivation_path != archive_folder:
                    log.info(f"Updating archivation_path = {archive_folder}")
                    a.archivation_path == archive_folder
                if a.ext_to_arch != ext_to_arch:
                    log.info(f"Updating ext_to_arch = {ext_to_arch}")
                    a.ext_to_arch == ext_to_arch
                if a.delete_archived_files != delete_archived_files:
                    log.info(f"Updating delete_archived_files = {delete_archived_files}")
                    a.delete_archived_files == delete_archived_files
                return False
        self._under_archive.append(Archivator(archive_prefix,
                                              sourse_folder,
                                              archive_folder,
                                              ext_to_arch,
                                              delete_archived_files))
        return True

    def show_archivator(self) -> None:
        """
        Print list of directories with defined archivators.
        """
        for a in self._under_archive:
            log.info(f"============================================")
            log.info(f"Archivator #{self._under_archive.index(a) + 1}")
            log.info(f"\tSourse path: {a.sourse_path}")
            log.info(f"\tArchive path: {a.archivation_path}")            
            log.info(f"\tArchive prefix: {a.archive_prefix}")            
            log.info(f"\text_to_arch: {a.ext_to_arch}")
            
    def clean(self):
        """
        Activate all existed cleaners.
        In case of an archivator and a cleaner were defined on same folder,
        the cleaner will postpone file deletion after archivation.
        """
        log.info("Cleaning files...")
        for c in self._under_clean:
            _delete = True
            ext_to_del = list(c.ext_to_del)
            for a in self._under_archive:
                # chek if exists archivator on same folder.  
                if c.path == a.sourse_path:
                    log.info(f"Same path of archivator and cleaner: {c.path}")
                    if not a.archivator_finished:
                        log.info("The archivator not run yet. Postpone clean after archivation")
                        a.postpone_clean = True
                        _delete = False
                        break
                    else:
                        _delete = True
                        # Reset arhivator flag
                        log.info("Resetting flag 'archivator_finished' = False")
                        a.archivator_finished = False
            if _delete:
                log.info(f"Deletting extentions: {ext_to_del}")
                c.delete_files(ext_to_del)
                
    def archive(self):
        """
        Zip archivation of all files in the sourse dir with specified extentions.
        If archivator flag 'delete_archived_files' is True,
        the archivator delete archived files after successfull archivation.
        At end the archivator runs the cleaner after successfull archivation.
        """
        log.info("Archivation...")
        for arch_obj in self._under_archive:
            # Archive files with extentions defined in arch_object
            zip_status:bool = arch_obj.archive_files()
            log.info(f"Created archive name {arch_obj.arch_file_name}")
            arch_obj.archivator_finished = True
            if zip_status and arch_obj.postpone_clean:
                # If the cleaner and the archivator objects was defined on the same sourse dir,
                # the archivator runs the cleaner after successfull archivation.
                self._clean_if_need(arch_obj)
                # Reset flag
                self.postpone_clean = False

    def _clean_if_need(self, arch_obj:object) -> bool:
        """
        If the cleaner and the archivator objects was defined on the same sourse dir,
        the archivator runs the cleaner after successfull archivation.
        @:arch_obj - current archivation object.
        """
        for clean_obj in self._under_clean:
            if clean_obj.path == arch_obj.sourse_path:
                # Run cleaner
                log.info(f"Run cleaner for {clean_obj.path}")
                # Delete already archived\need to be cleaned files.
                clean_obj.delete_files(clean_obj.ext_to_del)
                
    def arcive_and_clean(self):
        self.archive()
        self.clean()
