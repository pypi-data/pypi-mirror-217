# repler: report handler


The tool keeps you project envieronment clean by delete or archive files with specified extensions.
Every time your script run, it produces logs, reports and other auxiliary files
that relevant only for current execution.
Also you may want to save some logs for the future compare\analysis.
And obviously you will not think about to explode your hard with enormous bulk of old logs.
The idea is to define clean (the cleaner) and archive (archivator) policy on folders.
Running report handler at start of each test will clean unwanted files and
archive desired files for future use.

The tool keeps you project environment clean by delete or archive files with specified extensions.

# Installation:
pip install repler

# Usage:

# Create report handler with logging enable.
rh = ReportHandler(log_enable=True)

# Apply clean policiy (still not execute) on project folder:
# to delete all files with extentions txt and log.
# an age of deleted files should be greter then 0.
rh.set_cleaner(folder_path="\working directory",
               age_before_del_hour=0,
               ext_to_del=["log","txt"])

# Apply archive policiy (still not execute) on log folder:
# to archive all files with extention log.
rh.set_archivator(sourse_folder="\working directory\Logs",
                  archive_folder="\working directory\Logs\Archive",
                  archive_prefix="MyTest",
                  ext_to_arch=["log"],
                  delete_archived_files=True)

# Apply clean policiy (still not execute) on Archive folder:
# to delete all archives older then 24 hours.
rh.set_cleaner(folder_path="\working directory\Logs\Archive",
               age_before_del_hour=24,
               ext_to_del=["zip"])

# Prints all defined cleaners
rh.show_cleaner()

# Prints all defined archivators
rh.show_archivator()

# Run cleaning. Activate all defined cleaners.
rh.clean()

# Run archivation, Activate all defined archives.
rh.archive()

# Run both archive and clean. Activate all defined archives and cleaners.
rh.arcive_and_clean()

# Enable report handler logging, if initially it was defined with out the log enable.
rh.set_log_on()


