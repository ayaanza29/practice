import os


def create_user(name):
    directory = "user_data/" + name + "/"
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
    # add_job(name, "Job1")
    return 42


def add_job(user_name, job_name = ""):
    directory = "user_data/" + user_name + "/"
    os.makedirs(directory + job_name + "/")
    os.makedirs(directory + job_name + "/fcs_files/")
    os.makedirs(directory + job_name + "/temporary_images/")
    with open(directory + job_name +'/job_description.txt', 'w') as f:
        f.write('')
    return 42


def rename_job(user_name, old_job_name, new_job_name):
    directory = "user_data/" + user_name + "/"
    os.rename(directory + old_job_name, directory + new_job_name)
    return 42


def modify_job():
    return 42


create_user("Jerry")
rename_job("Jerry", "Job1", "Fun_Job")