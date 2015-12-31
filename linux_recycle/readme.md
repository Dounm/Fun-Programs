#Linux Recycle Bin
this is an python scripts used for replace shell command *rm* which move files to recycle bin instead of removing files.

##Steps
1. add the command below to *~/.bashrc*
    `alias rm='python recycle_dir "deny_file_splited_by_blank"'`
    e.g.
    `alias rm='python /home/dounm/recycle_bin "/  /home/dounm /usr"'`
    the example above means that the all the files you removed will be sended to ***/home/dounm/recycle_bin*** and you cannot remove ***/***, ***/home/dounm*** and ***/usr***

2. let the new *~/.bashrc* takes effect
    `source ~/.bashrc`

3. modifiy the *crontab* file to clear recycle bin at regular time
